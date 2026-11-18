"""完整 YAML 语法检查与 Skill 元数据格式不依赖模型判断。"""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[2]

class YamlValidationTests(unittest.TestCase):
    def check(self,root):
        script=ROOT/'studio-tests/validate-yaml.py'
        self.assertTrue(script.is_file(),'缺少完整 YAML 校验入口')
        result=subprocess.run([sys.executable,str(script),'--root',str(root)],capture_output=True,text=True,encoding='utf-8',timeout=20)
        return result,json.loads(result.stdout)

    def test_malformed_yaml_is_not_reported_as_valid(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'project.yaml').write_text('modes: [unfinished\n',encoding='utf-8')
            result,report=self.check(root)
            self.assertEqual(result.returncode,1,result.stderr)
            self.assertEqual(report['checks'][0]['file'],'project.yaml')
            self.assertEqual(report['checks'][0]['id'],'yaml.syntax')

    def test_yaml_and_skill_frontmatter_are_both_parsed(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'project.yaml').write_text('schema_version: 1\n',encoding='utf-8')
            skill=root/'.agents/skills/sample';skill.mkdir(parents=True)
            (skill/'SKILL.md').write_text('---\nname: sample\ndescription: [invalid, list]\n---\n正文\n',encoding='utf-8')
            result,report=self.check(root)
            self.assertEqual(result.returncode,1,result.stderr)
            self.assertTrue(any(check['id']=='skill.yaml_schema' for check in report['checks']))
            (skill/'SKILL.md').write_text('---\nname: sample\ndescription: 正确描述\n---\n正文\n',encoding='utf-8')
            result,report=self.check(root)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(report['coverage'],{'yaml_files':1,'skill_frontmatters':1})

if __name__=='__main__':unittest.main()
