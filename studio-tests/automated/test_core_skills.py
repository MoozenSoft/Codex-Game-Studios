"""验证核心工作流的客户端可读配置和显式调用边界。"""
import json
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[2]
CORE=('start','next-step','project-settings','project-stage-detect','brainstorm','prototype','setup-engine','create-epics','create-stories','story-readiness','dev-story','code-review','smoke-check','story-done')


class CoreSkillTests(unittest.TestCase):
    def test_core_skill_metadata_and_resources_exist(self):
        for name in CORE:
            with self.subTest(skill=name):
                path=ROOT/'.agents/skills'/name/'SKILL.md'
                self.assertTrue(path.is_file(),f'核心入口未迁移：{name}')
                text=path.read_text(encoding='utf-8')
                header=text.split('---',2)[1]
                self.assertIn(f'name: {name}',header)
                self.assertIsInstance(json.loads(re.search(r'^description: (.+)$',header,re.M).group(1)),str)
                self.assertFalse(set(re.findall(r'^([\w-]+):',header,re.M))&{'allowed-tools','model','context'})

    def test_story_lifecycle_requires_explicit_invocation(self):
        for name in ('dev-story','story-done'):
            with self.subTest(skill=name):
                policy=ROOT/'.agents/skills'/name/'agents/openai.yaml'
                self.assertTrue(policy.is_file(),'必须保留显式调用策略')
                # 这里检查交给客户端的策略数据，不通过正文措辞猜测调用权限。
                value=re.search(r'allow_implicit_invocation:\s*(\w+)',policy.read_text(encoding='utf-8'))
                self.assertEqual(value.group(1),'false')

    def test_story_close_policy_rejects_required_failure_and_unknown(self):
        contract=(ROOT/'.agents/skills/story-done/CONTRACT.md').read_text(encoding='utf-8')
        rows=dict(re.findall(r'^\| `(COMPLETE WITH NOTES|COMPLETE|NOT ASSESSED|BLOCKED)` \| `(ALLOW|DENY)` \|$',contract,re.M))
        self.assertEqual(rows,{'COMPLETE':'ALLOW','COMPLETE WITH NOTES':'ALLOW','NOT ASSESSED':'DENY','BLOCKED':'DENY'},'客户端关闭资格合同必须覆盖四种判定，必要失败/未知不得关闭')
        close=(ROOT/'.agents/skills/story-done/SKILL.md').read_text(encoding='utf-8').split('## Phase 7:',1)[1]
        self.assertNotRegex(close,r'Close\s+anyway, accepting the deviations')
        self.assertNotIn('Phase 7 override',contract)
        spec=(ROOT/'studio-tests/skills/readiness/story-done.md').read_text(encoding='utf-8')
        self.assertNotIn('If closed via "Accept deviations as-is and close anyway"',spec)


if __name__=='__main__':unittest.main()
