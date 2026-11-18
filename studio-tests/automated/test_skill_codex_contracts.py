"""验证 Skills 的 Codex 交互合同；真实客户端行为仍需单独记证。"""

import json
from pathlib import Path
import re
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / ".agents/skills"


def read(relative):
    return (ROOT / relative).read_text(encoding="utf-8")


class SkillCodexContracts(unittest.TestCase):
    def test_question_examples_fit_single_selection_schema(self):
        for relative in (
            ".agents/skills/smoke-check/references/4-manual-checks.md",
            ".agents/skills/qa-plan/SKILL.md",
            ".agents/skills/design-review/SKILL.md",
        ):
            body = read(relative)
            with self.subTest(path=relative):
                self.assertFalse("multiSelect" in body, relative)
                examples = re.findall(r"```json\s*\n(.*?)\n```", body, re.S)
                self.assertTrue(examples, "至少给出一个实际 schema 的提问示例")
                adapters = set()
                for example in examples:
                    payload = json.loads(example)
                    self.assertEqual(set(payload), {"questions"})
                    self.assertTrue(1 <= len(payload["questions"]) <= 3)
                    for question in payload["questions"]:
                        self.assertTrue(2 <= len(question["options"]) <= 3)
                        if "title" in question:
                            adapters.add("async")
                            self.assertEqual(set(question), {"title", "options"})
                            self.assertTrue(all(isinstance(option, str) for option in question["options"]))
                        else:
                            adapters.add("sync")
                            self.assertEqual(set(question), {"id", "header", "question", "options"})
                            self.assertLessEqual(len(question["header"]), 12)
                            for option in question["options"]:
                                self.assertEqual(set(option), {"label", "description"})
                self.assertEqual(adapters, {"sync", "async"}, "按实际工具选择不同schema")

    def test_async_question_receipts_remain_pending_until_user_answers(self):
        for relative in (
            ".agents/skills/smoke-check/references/4-manual-checks.md",
            ".agents/skills/qa-plan/SKILL.md",
            ".agents/skills/design-review/SKILL.md",
        ):
            body = read(relative)
            rows = dict(re.findall(r"^\| `(ASYNC SUBMITTED|USER ANSWER RECEIVED|NO USER ANSWER)` \| ([^|]+) \|", body, re.M))
            with self.subTest(path=relative):
                self.assertEqual(set(rows), {"ASYNC SUBMITTED", "USER ANSWER RECEIVED", "NO USER ANSWER"})
                self.assertIn("WAITING", rows["ASYNC SUBMITTED"])
                self.assertIn("UNANSWERED", rows["NO USER ANSWER"])
                self.assertTrue("Plan" in body and "request_user_input_async" in body)

    def test_manual_checks_define_non_permissive_response_mapping(self):
        body = read(".agents/skills/smoke-check/references/4-manual-checks.md")
        rows = dict(re.findall(r"^\| `(PASS|FAIL|NOT TESTED|UNANSWERED)` \| ([^|]+) \|", body, re.M))
        self.assertEqual(set(rows), {"PASS", "FAIL", "NOT TESTED", "UNANSWERED"})
        self.assertIn("NOT ASSESSED", rows["NOT TESTED"])
        self.assertIn("NOT ASSESSED", rows["UNANSWERED"])
        self.assertNotRegex(body, r"leave all unselected|at most 3 calls")

    def test_report_verdict_covers_all_manual_batches_and_platforms(self):
        body = read(".agents/skills/smoke-check/references/5-report.md")
        failures = body.split("**FAIL** if ANY of:", 1)[1].split("**NOT ASSESSED**", 1)[0]
        warnings = body.split("**PASS WITH WARNINGS** if ALL of:", 1)[1].split("**PASS** if ALL of:", 1)[0]
        self.assertIn("Any required manual or platform check returned FAIL", failures)
        self.assertIn("Batch 3", failures)
        self.assertIn("All required manual and platform checks PASS or N/A", warnings)
        platform = body.split("### Platform-Specific Results", 1)[1].split("### Verdict:", 1)[0]
        self.assertIn("Not Assessed", platform)
        self.assertIn("PASS / NOT ASSESSED / FAIL", platform)
        self.assertNotRegex(body, r"any verdict carries the label: `PASS")

    def test_qa_output_outcomes_include_both_choices_and_unanswered_state(self):
        body = read(".agents/skills/qa-plan/SKILL.md")
        rows = {(plan, stories): outcome for plan, stories, outcome in re.findall(
            r"^\| `(yes|no|pending)` \| `(yes|no|pending)` \| ([^|]+) \|", body, re.M
        )}
        self.assertEqual(set(rows), {("yes", "yes"), ("yes", "no"), ("no", "yes"), ("no", "no"), ("pending", "pending")})
        self.assertIn("NOT ASSESSED", rows[("pending", "pending")])
        self.assertNotIn("The only other outcome", body)
        self.assertNotRegex(body, r"ask once to\s+approve the write")

    def test_template_remote_classifier_handles_transports_and_forks(self):
        script = SKILLS / "start/scripts/template-remote.py"
        self.assertTrue(script.is_file())
        for url, expected in (
            ("https://github.com/MoozenSoft/Codex-Game-Studios.git", "TEMPLATE"),
            ("git@github.com:MoozenSoft/Codex-Game-Studios.git", "TEMPLATE"),
            ("ssh://git@github.com/MoozenSoft/Codex-Game-Studios", "TEMPLATE"),
            ("https://github.com/donchitos/claude-code-game-studios.git", "TEMPLATE"),
            ("git@github.com:DONCHITOS/CLAUDE-CODE-GAME-STUDIOS.git", "TEMPLATE"),
            ("https://github.com/my-team/Codex-Game-Studios.git", "OTHER"),
            ("https://github.com/other/MoozenSoft/Codex-Game-Studios.git", "OTHER"),
            ("https://github.com.evil.example/MoozenSoft/Codex-Game-Studios.git", "OTHER"),
            ("", "UNKNOWN"),
        ):
            with self.subTest(url=url):
                result = subprocess.run([sys.executable, str(script), url], capture_output=True, text=True, check=True)
                self.assertEqual(result.stdout.strip(), expected)

    def test_formal_specs_require_codex_invocation_policy(self):
        for name in ("hotfix", "day-one-patch", "launch-checklist"):
            body = read(f"studio-tests/skills/utility/{name}.md")
            self.assertFalse("disable-model-invocation" in body, name)
            self.assertIn("agents/openai.yaml", body)
            self.assertIn("allow_implicit_invocation: false", body)

    def test_client_mechanisms_do_not_claim_implicit_execution_or_grants(self):
        forbidden = {
            ".agents/skills/start/SKILL.md": ("not this skill's",),
            ".agents/skills/dev-story/SKILL.md": ("runs\nnothing",),
            ".agents/skills/asset-audit/SKILL.md": ("pre-approved above", "no\n  pre-approved tool here"),
            ".agents/skills/project-settings/SKILL.md": ("This skill pre-approves",),
            ".agents/skills/project-stage-detect/SKILL.md": ("This skill's permission grant",),
            ".agents/skills/perf-profile/SKILL.md": ("this skill pre-approves",),
            ".agents/skills/write-changelog/SKILL.md": ("auto-resolved", "injected", "resolved before this skill runs"),
            ".agents/skills/code-review/SKILL.md": ("25k-token read cap",),
            ".agents/skills/design-review/SKILL.md": ("Never plain text", "this session has used X%"),
        }
        for relative, phrases in forbidden.items():
            for phrase in phrases:
                with self.subTest(path=relative, phrase=phrase):
                    self.assertFalse(phrase in read(relative), f"{relative}: {phrase!r}")

    def test_specs_and_handoffs_do_not_assign_separate_skill_models(self):
        paths = list((ROOT / "studio-tests/skills").rglob("*.md")) + [
            SKILLS / "brainstorm/SKILL.md", SKILLS / "brainstorm/references/full-concept.md",
        ]
        for path in paths:
            body = path.read_text(encoding="utf-8")
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertIsNone(re.search(r"Sol-tier|skill's own model|turn on this skill's model|model: opus", body))

    def test_formal_question_specs_preserve_actual_single_selection_protocol(self):
        for relative in (
            "studio-tests/skills/review/design-review.md",
            "studio-tests/skills/utility/qa-plan.md",
            "studio-tests/skills/utility/cut.md",
            ".agents/skills/cut/SKILL.md",
        ):
            body = read(relative)
            with self.subTest(path=relative):
                self.assertIsNone(re.search(r"multiSelect|multi-select", body))
        self.assertNotRegex(read("studio-tests/skills/utility/smoke-check.md"), r'nothing selected|selects only|selects "|empty failure list|selects no FAILED')


if __name__ == "__main__":
    unittest.main()
