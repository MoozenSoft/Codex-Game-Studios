"""核对上游模型指定点及其 Codex 运行入口。"""
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[2]
SOURCE = json.loads((ROOT / 'studio-tests/fixtures/model-routing.json').read_text(encoding='utf-8'))
FAMILIES = {'opus': 'astra', 'sonnet': 'sol'}
REQUIREMENT = re.compile(r'^\*\*会话模型要求\*\* 使用 `([^`]+)`', re.M)
ROLE_FAMILY = re.compile(r'^\*\*Model family\*\* `([^`]+)`', re.M)
SCRIPT = ROOT / '.agents/scripts/model-routing.py'


def active_models(kind):
    return {
        row['target']: FAMILIES[row['source_model']]
        for row in SOURCE['declarations']
        if row['status'] == 'active' and row['source'].split('/')[1] == kind
    }


class ModelRoutingTests(unittest.TestCase):
    def test_role_families_match_upstream_without_pinning_a_version(self):
        expected = active_models('agents')
        actual = {}
        for path in (ROOT / '.codex/agents').glob('*.toml'):
            role = tomllib.loads(path.read_text(encoding='utf-8'))
            self.assertNotIn('model_reasoning_effort', role)
            self.assertNotIn('model', role, path)
            families = ROLE_FAMILY.findall(role['developer_instructions'])
            if families:
                self.assertEqual(len(families), 1, path)
                actual[path.relative_to(ROOT).as_posix()] = families[0]
        self.assertEqual(actual, expected)

    def test_skill_session_requirements_match_the_active_upstream_pins(self):
        expected = active_models('skills')
        actual = {}
        for path in (ROOT / '.agents/skills').glob('*/SKILL.md'):
            _, header, body = path.read_text(encoding='utf-8').split('---', 2)
            self.assertNotRegex(header, r'(?m)^model:')
            models = REQUIREMENT.findall(body)
            if models:
                self.assertEqual(len(models), 1, path)
                self.assertIn('`.agents/docs/model-tiers.md`', body)
                actual[path.relative_to(ROOT).as_posix()] = models[0]
        self.assertEqual(actual, expected)

    def test_one_shot_sets_the_model_at_build_time(self):
        pin = SOURCE['prototype_build']
        model = FAMILIES[pin['source_model']]
        card = (ROOT / pin['target']).read_text(encoding='utf-8')
        build = (ROOT / '.agents/skills/prototype/references/one-shot-2-build.md').read_text(encoding='utf-8')
        self.assertIn(f'`{model}`', card.split('## 6. On Build it', 1)[0])
        self.assertIn(f'`{model}`', build.split('## 2. The rules', 1)[0])

    def resolve(self, family, catalog):
        return subprocess.run(
            [sys.executable, str(SCRIPT), family, '--catalog-stdin'],
            input=json.dumps(catalog), text=True, encoding='utf-8', capture_output=True,
            timeout=20,
        )

    def test_resolver_chooses_the_highest_visible_stable_version_numerically(self):
        rows = [
            {'model': 'gpt-8.9-astra', 'hidden': False},
            {'model': 'gpt-8.10-astra', 'hidden': False},
            {'model': 'gpt-9-astra', 'hidden': True},
            {'model': 'gpt-10-astra-preview', 'hidden': False},
            {'model': 'gpt-11-sol', 'hidden': False},
        ]
        for family, expected in (('astra', 'gpt-8.10-astra'), ('sol', 'gpt-11-sol')):
            with self.subTest(family=family):
                query = self.resolve(family, {'data': rows, 'nextCursor': None})
                self.assertEqual(query.returncode, 0, query.stderr)
                self.assertEqual(json.loads(query.stdout)['model'], expected)

    def test_resolver_does_not_substitute_another_family_or_accept_partial_catalog(self):
        rows = [{'model': 'gpt-8-sol', 'hidden': False}]
        for cursor in (None, 'next'):
            with self.subTest(cursor=cursor):
                query = self.resolve('astra', {'data': rows, 'nextCursor': cursor})
                self.assertEqual(query.returncode, 2)
                result = json.loads(query.stdout)
                self.assertEqual(result['status'], 'not_assessed')
                self.assertNotIn('model', result)

    def test_resolver_accepts_model_ids_advertised_by_the_active_client(self):
        query = subprocess.run(
            [sys.executable, str(SCRIPT), 'sol', '--available-stdin'],
            input=json.dumps(['gpt-8-sol', 'gpt-8.2-sol', 'gpt-9-astra']),
            text=True, encoding='utf-8', capture_output=True, timeout=20,
        )
        self.assertEqual(query.returncode, 0, query.stderr)
        self.assertEqual(json.loads(query.stdout)['model'], 'gpt-8.2-sol')

    def test_app_server_resolver_follows_pagination_and_rejects_refresh_fallback(self):
        protocol = r'''
import json, sys
for line in sys.stdin:
    msg = json.loads(line)
    method = msg['method']
    if method == 'initialize':
        result = {}
    elif method == 'initialized':
        continue
    elif method == 'model/list':
        assert msg['params']['includeHidden'] is False
        cursor = msg['params'].get('cursor')
        result = {'data': [{'model': 'gpt-8.1-sol' if cursor else 'gpt-8-sol', 'hidden': False}],
                  'nextCursor': None if cursor else 'next'}
        if 'failing-refresh' in sys.argv:
            print('failed to refresh available models: request timed out', file=sys.stderr, flush=True)
    print(json.dumps({'id': msg['id'], 'result': result}), flush=True)
'''
        spec = importlib.util.spec_from_file_location('model_routing', SCRIPT)
        resolver = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(resolver)
        command = [sys.executable, '-u', '-c', protocol]
        self.assertEqual(resolver.select_model(resolver.read_catalog(command), 'sol'), 'gpt-8.1-sol')
        with self.assertRaises(resolver.CatalogError):
            resolver.read_catalog(command + ['failing-refresh'])


if __name__ == '__main__':
    unittest.main()
