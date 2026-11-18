"""检查交给 Codex 客户端的角色配置与依赖，不将正文指令当成权限沙箱。"""
from pathlib import Path
import importlib.util
import tempfile
import tomllib
import unittest

ROOT=Path(__file__).resolve().parents[2]
CORE=('prototyper','gameplay-programmer','lead-programmer','qa-tester','technical-director')


class AgentTests(unittest.TestCase):
    def test_core_roles_are_valid_codex_configs(self):
        for name in CORE:
            with self.subTest(role=name):
                path=ROOT/'.codex/agents'/f'{name}.toml'
                self.assertTrue(path.is_file(),f'缺少核心角色 {name}')
                data=tomllib.loads(path.read_text(encoding='utf-8'))
                self.assertEqual(data['name'],name)
                self.assertNotIn('model_reasoning_effort',data)
                self.assertTrue(data['description'])
                self.assertTrue(data['developer_instructions'])
                self.assertFalse(set(data)&{'tools','disallowedTools','maxTurns','memory','isolation','sandbox_mode','approval_policy'})

    def test_project_leaves_session_and_subagent_model_choices_unset(self):
        path=ROOT/'.codex/config.toml'
        self.assertTrue(path.is_file())
        data=tomllib.loads(path.read_text(encoding='utf-8'))
        self.assertNotIn('model',data)
        self.assertNotIn('model_reasoning_effort',data)
        self.assertNotIn('default_subagent_model',data.get('agents',{}))
        self.assertNotIn('default_subagent_reasoning_effort',data.get('agents',{}))

    def test_validator_accepts_inheritance_and_user_model_override(self):
        spec=importlib.util.spec_from_file_location('inherit_validation',ROOT/'.agents/scripts/framework_validation.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        for override in ('','model = "user-selected-model"\nmodel_reasoning_effort = "high"\n'):
            with self.subTest(override=override), tempfile.TemporaryDirectory() as temporary:
                root=Path(temporary);roles=root/'.codex/agents';roles.mkdir(parents=True)
                (roles/'reader.toml').write_text('name = "reader"\ndescription = "只读检查"\ndeveloper_instructions = "读取指定文件"\n'+override,encoding='utf-8')
                self.assertEqual(module.validate(root)['exit_code'],0)

    def test_lead_required_skill_is_available(self):
        self.assertTrue((ROOT/'.agents/skills/tech-debt/SKILL.md').is_file(),'lead-programmer 的必需 Skill 必须随角色迁移')


if __name__=='__main__': unittest.main()
