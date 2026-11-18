"""共享运行文档的可执行接口、配置来源与恢复合同回归。"""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class SharedCodexContracts(unittest.TestCase):
    def test_memory_uses_single_checkpoint_and_existing_authorization(self):
        text = read(".agents/rules/agent-memory.md")
        self.assertIn("session-state.sh", text)
        self.assertIn("OVERWRITTEN", text)
        self.assertIn("existing authorization", text)
        self.assertNotIn("An append, never a rewrite", text)
        self.assertNotIn("ask first, naming the path", text)

    def test_read_guard_contract_calls_real_helper_and_handles_observations(self):
        runtime = read(".agents/docs/codex-runtime.md")
        self.assertIn("read-guard.sh check", runtime)
        self.assertIn("--bounded no", runtime)
        self.assertIn("read-guard.sh sections", runtime)
        self.assertIn("LARGE", runtime)
        self.assertIn("size", runtime)
        self.assertIn("NOT ASSESSED", runtime)
        effects = read(".agents/docs/effects-map.md")
        guard = effects.split("## features.read_guard\n", 1)[1].split("## ", 1)[0]
        self.assertIn("explicit", guard)
        self.assertNotIn("validate-read.sh", guard)
        self.assertNotIn("PreToolUse Read", guard)

    def test_role_template_checks_native_toml_and_inheritance(self):
        text = read("studio-tests/templates/agent-test-spec.md")
        self.assertIn("developer_instructions", text)
        self.assertIn("model_reasoning_effort", text)
        self.assertNotIn("gpt-6.1-sol", text)
        self.assertNotIn("Astra", text)
        self.assertNotIn("Frontmatter", text)

    def test_event_documentation_distinguishes_registration_from_evidence(self):
        text = read(".agents/docs/hooks-reference.md")
        self.assertNotIn("已实测的七类事件", text)
        self.assertRegex(text, r"PreCompact[^\n]*未评估")

    def test_recovery_template_requires_agent_branch_check(self):
        text = read(".agents/docs/templates/session-state.md")
        self.assertIn("git branch --show-current", text)
        self.assertIn("dispatch.py", text)
        self.assertNotIn("statusline.sh", text)
        self.assertNotIn("SessionStart runs then too", text)
        self.assertNotIn("adds one line when they differ", text)

    def test_source_only_functions_have_six_argument_call_protocol(self):
        for path in (".agents/docs/automation-modes.md", ".agents/docs/config-resolution.md"):
            with self.subTest(path=path):
                text = read(path)
                self.assertIn("source .agents/scripts/yaml-helper.sh", text)
                self.assertIn("is_always_ask_category", text)
                call = re.search(r'^log_decision (.+)$', text, re.MULTILINE)
                self.assertIsNotNone(call)
                self.assertEqual(len(re.findall(r'"[^"\n]*"', call.group(1))), 6)

    def test_effects_map_documents_fallback_and_no_startup_schema_audit(self):
        text = read(".agents/docs/effects-map.md")
        schema = text.split("### Schema validation on read", 1)[1].split("### Two-developer", 1)[0]
        self.assertIn("notes:", schema)
        self.assertIn("validate_local_yaml_base", schema)
        self.assertIn("validate_yaml_enum", schema)
        self.assertNotIn("Session-start warning", schema)
        self.assertNotIn("Hard error: skill exits", schema)

    def test_engine_chain_ignores_local_engine_for_all_derived_roots(self):
        text = read(".agents/docs/code-root-resolution.md")
        self.assertNotIn("`engine.name` from `project.local.yaml`, then `project.yaml`", text)
        self.assertIn("`engine.name` from `project.yaml`", text)
        self.assertIn("test root", text)
        self.assertIn("engine_row", text)


if __name__ == "__main__":
    unittest.main()
