"""按冻结的上游来源核对角色正文，不用TOML可解析代替内容完整。"""
import hashlib
import json
from pathlib import Path
import tomllib
import unittest

ROOT=Path(__file__).resolve().parents[2]

def recover_source_body(body, patches):
    for patch in reversed(patches):
        offsets=patch['source_offsets']
        if any(type(position)!=int or position<0 for position in offsets) or len(offsets)!=patch['count'] or offsets!=sorted(set(offsets)):
            raise AssertionError('适配位置记录无效')
        delta=len(patch['new'])-len(patch['old'])
        for index in range(len(offsets)-1,-1,-1):
            position=offsets[index]+index*delta
            if body[position:position+len(patch['new'])]!=patch['new']:
                raise AssertionError('适配正文与位置记录不一致')
            body=body[:position]+patch['old']+body[position+len(patch['new']):]
    return body

class RoleContentTests(unittest.TestCase):
    def test_inverse_edits_preserve_preexisting_replacement_text(self):
        patch={'old':'old','new':'longer','count':2,'source_offsets':[0,8]}
        self.assertEqual(recover_source_body('longer new longer',[patch]),'old new old')
        patch={'old':'old','new':'new','count':2,'source_offsets':[0,8]}
        self.assertEqual(recover_source_body('new new new',[patch]),'old new old')
        with self.assertRaises(AssertionError):recover_source_body('bad new new',[patch])

    def test_role_domain_content_is_preserved_with_explicit_codex_edits(self):
        baseline=json.loads((ROOT/'studio-tests/fixtures/roles/original-content.json').read_text(encoding='utf-8'))['roles']
        adaptations=json.loads((ROOT/'studio-tests/fixtures/roles/adaptations.json').read_text(encoding='utf-8'))['roles']
        actual={p.stem:p for p in (ROOT/'.codex/agents').glob('*.toml')}
        self.assertEqual(set(actual),set(baseline))
        for name,source in baseline.items():
            with self.subTest(role=name):
                raw=actual[name].read_text(encoding='utf-8')
                text=tomllib.loads(raw)['developer_instructions']
                self.assertIn("developer_instructions = '''\n",raw,'角色正文应使用可读的多行TOML')
                self.assertIn('\n## Role instructions\n',text)
                body=text.split('\n## Role instructions\n',1)[1]
                self.assertEqual(hashlib.sha256(body.encode()).hexdigest(),adaptations[name]['adapted_sha256'])
                for patch in adaptations[name]['patches']:self.assertTrue(patch['reason'])
                original=recover_source_body(body,adaptations[name]['patches'])
                self.assertEqual(hashlib.sha256(original.encode()).hexdigest(),source['body_sha256'],'没有记录的专业正文删减或改写必须失败')
                self.assertEqual(len(original.splitlines()),source['body_lines'])
                self.assertEqual(tomllib.loads(raw)['description'],source['description'])
                self.assertIn('.agents/docs/automation-modes.md',text)
                self.assertNotRegex(text,r'\.claude/|CLAUDE\.md|AskUserQuestion|subagent_type:|Claude Code')
                self.assertNotIn('<!-- BEGIN UPSTREAM ROLE -->',text,'实际角色指令不能靠REFERENCE标记逃过兼容性盘点')
                self.assertNotIn('Do not use Write/Edit until the user has said yes',text)

    def test_specialist_and_worktree_instructions_use_actual_capabilities(self):
        for name in ('godot-specialist','unity-specialist','unreal-specialist'):
            text=tomllib.loads((ROOT/f'.codex/agents/{name}.toml').read_text(encoding='utf-8'))['developer_instructions']
            self.assertIn('actual Codex delegation schema',text)
            self.assertIn('If delegation is unavailable',text)
        text=tomllib.loads((ROOT/'.codex/agents/prototyper.toml').read_text(encoding='utf-8'))['developer_instructions']
        for required in ('does not automatically create','do not assume the first entry','when the required access is authorized'):
            self.assertIn(required,text)

    def test_skill_invocation_edits_preserve_resource_paths(self):
        expected={
            'prototyper':['.agents/docs/templates/prototype-report.md','.agents/docs/templates/vertical-slice-report.md'],
            'qa-tester':['.agents/skills/bug-report/SKILL.md'],
            'community-manager':['production/releases/[version]/patch-notes.md'],
        }
        for name,paths in expected.items():
            text=tomllib.loads((ROOT/f'.codex/agents/{name}.toml').read_text(encoding='utf-8'))['developer_instructions']
            for path in paths:self.assertIn(path,text)

    def test_workflow_confirmations_are_conditional(self):
        for path in (ROOT/'.codex/agents').glob('*.toml'):
            text=tomllib.loads(path.read_text(encoding='utf-8'))['developer_instructions']
            self.assertNotIn('Get confirmation before starting.',text)
            self.assertNotIn('— get confirmation',text)
            self.assertNotIn('— get approval before writing',text)
            self.assertNotIn('   - Ask: "Does this match your expectations?',text)
            self.assertNotIn('document the decision (ADR, pillar update, vision doc) — ask',text)
            self.assertNotIn('audit-[date].md` after\napproval:',text)

if __name__=='__main__':unittest.main()
