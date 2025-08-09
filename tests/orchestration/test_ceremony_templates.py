"""
Tests for Purposeful Ceremony Templates

These tests verify that ceremony templates properly teach Mallku
about reciprocity, balance, and purpose-driven action.
"""

from mallku.orchestration.loom.ceremony_templates import (
    BugHealingCeremony,
    CeremonyTask,
    FeatureCreationCeremony,
    MallkuNeed,
    select_ceremony_template,
)


class TestCeremonyTemplates:
    """Test the base ceremony template functionality"""

    def test_bug_healing_ceremony_creation(self):
        """Test that bug healing ceremonies are properly initialized"""
        ceremony = BugHealingCeremony()

        assert ceremony.ceremony_name == "Bug Healing Ceremony"
        assert ceremony.sacred_purpose == MallkuNeed.HEALING
        assert ceremony.version == "1.0.0"
        assert ceremony.usage_count == 0
        assert ceremony.reciprocity_history == []

    def test_bug_healing_task_generation(self):
        """Test that bug healing generates appropriate tasks"""
        ceremony = BugHealingCeremony()
        context = {
            "bug_description": "Fire Circle memory not persisting",
            "affected_component": "src/mallku/firecircle/memory",
            "requester": "Guardian",
        }

        tasks = ceremony.generate_tasks(context)

        # Should generate standard bug-fixing tasks
        assert len(tasks) == 5
        assert tasks[0].task_id == "T001"
        assert tasks[0].name == "Reproduce and Document Bug"
        assert tasks[0].serves_need == MallkuNeed.HEALING
        assert "Fire Circle memory not persisting" in tasks[0].description

        # Check dependencies
        assert tasks[1].dependencies == ["T001"]  # Investigation depends on reproduction
        assert tasks[2].dependencies == ["T002"]  # Fix depends on investigation
        assert tasks[3].dependencies == ["T003"]  # Tests depend on fix

    def test_khipu_thread_generation(self):
        """Test that khipu_thread.md is properly formatted"""
        ceremony = BugHealingCeremony()
        context = {
            "bug_description": "Test bug",
            "affected_component": "test/component",
            "master_weaver": "TestWeaver",
            "requester": "TestGuardian",
        }

        khipu_content = ceremony.create_khipu_thread(context, "test-ceremony-123")

        # Check required sections
        assert "ceremony_id: test-ceremony-123" in khipu_content
        assert "sacred_purpose: healing" in khipu_content
        assert "## Sacred Intention" in khipu_content
        assert "## Task Manifest" in khipu_content
        assert "## Tasks" in khipu_content
        assert "## Synthesis Space" in khipu_content
        assert "## Ceremony Log" in khipu_content

        # Check task formatting
        assert "### T001: Reproduce and Document Bug" in khipu_content
        assert "*Status: PENDING*" in khipu_content
        assert "*Serves: healing*" in khipu_content

    def test_reciprocity_assessment_success(self):
        """Test reciprocity metrics for successful bug fix"""
        ceremony = BugHealingCeremony()

        ceremony_result = {
            "ceremony_id": "test-123",
            "tasks_completed": {
                "T001": {"status": "COMPLETE"},
                "T002": {"status": "COMPLETE"},
                "T003": {"status": "COMPLETE"},
                "T004": {"status": "COMPLETE"},
                "T005": {"status": "COMPLETE"},
            },
            "duration_hours": 4,
            "apprentice_count": 3,
            "lessons_learned": ["Always check permissions first"],
        }

        metrics = ceremony.assess_completion(ceremony_result)

        assert metrics.need_fulfilled is True
        assert metrics.utility_delivered == "Bug fixed"
        assert metrics.balance_assessment == "balanced"
        assert "Complete healing includes prevention" in metrics.lessons_learned

    def test_reciprocity_assessment_incomplete(self):
        """Test reciprocity metrics for incomplete ceremony"""
        ceremony = BugHealingCeremony()

        ceremony_result = {
            "ceremony_id": "test-456",
            "tasks_completed": {
                "T001": {"status": "COMPLETE"},
                "T002": {"status": "COMPLETE"},
                "T003": {"status": "FAILED"},  # Fix failed
            },
            "duration_hours": 3,
            "apprentice_count": 2,
        }

        metrics = ceremony.assess_completion(ceremony_result)

        assert metrics.need_fulfilled is False
        assert metrics.utility_delivered == "Bug investigation completed"
        assert metrics.balance_assessment == "incomplete"
        assert "Investigation without resolution" in metrics.lessons_learned

    def test_ceremony_reflection(self):
        """Test post-ceremony reflection captures lessons"""
        ceremony = BugHealingCeremony()

        ceremony_result = {
            "ceremony_id": "test-789",
            "tasks_completed": {
                "T001": {"status": "COMPLETE"},
                "T002": {"status": "COMPLETE"},
                "T003": {"status": "COMPLETE"},
                "T004": {"status": "COMPLETE"},
            },
        }

        reflection = ceremony.reflect_on_ceremony(ceremony_result)

        assert reflection["reciprocity_achieved"] is True
        assert reflection["sacred_purpose_served"] is True
        assert len(reflection["lessons_for_mallku"]) > 0
        assert ceremony.usage_count == 1
        assert len(ceremony.reciprocity_history) == 1

    def test_evolution_trigger(self):
        """Test that templates suggest evolution after multiple uses"""
        ceremony = BugHealingCeremony()

        # Simulate 5 ceremonies with mixed results
        for i in range(5):
            result = {
                "ceremony_id": f"test-{i}",
                "tasks_completed": {
                    "T001": {"status": "COMPLETE"},
                    "T002": {"status": "COMPLETE"},
                    "T003": {"status": "COMPLETE" if i > 0 else "FAILED"},
                },
            }
            reflection = ceremony.reflect_on_ceremony(result)

        # Fifth ceremony should trigger evolution suggestion
        assert reflection.get("suggest_evolution") is True
        assert "evolution_reason" in reflection

    def test_feature_creation_ceremony(self):
        """Test feature creation ceremony template"""
        ceremony = FeatureCreationCeremony()

        assert ceremony.sacred_purpose == MallkuNeed.CREATION

        context = {
            "feature_name": "Consciousness Metrics Dashboard",
            "requirements": [
                "Display real-time consciousness scores",
                "Show historical trends",
                "Export data as CSV",
            ],
            "requester": "Fire Circle",
            "related_components": ["consciousness", "metrics", "web_ui"],
        }

        tasks = ceremony.generate_tasks(context)

        # Should have base tasks plus requirement tasks
        assert len(tasks) >= 6  # 5 base + requirements
        assert any("Consciousness Metrics Dashboard" in task.description for task in tasks)
        assert any(task.serves_need == MallkuNeed.DEFENSE for task in tasks)  # Tests
        assert any(task.serves_need == MallkuNeed.MEMORY for task in tasks)  # Docs

    def test_template_selection(self):
        """Test selecting appropriate template based on need"""
        # Exact matches
        bug_template = select_ceremony_template(MallkuNeed.HEALING, "bug")
        assert isinstance(bug_template, BugHealingCeremony)

        feature_template = select_ceremony_template(MallkuNeed.CREATION, "feature")
        assert isinstance(feature_template, FeatureCreationCeremony)

        # Purpose-based fallback
        healing_template = select_ceremony_template(MallkuNeed.HEALING, "unknown")
        assert isinstance(healing_template, BugHealingCeremony)

        # No match
        no_template = select_ceremony_template(MallkuNeed.DECISION_MAKING, "unknown")
        assert no_template is None

    def test_task_khipu_format(self):
        """Test that individual tasks format correctly for khipu"""
        task = CeremonyTask(
            task_id="T001",
            name="Test Task",
            description="A test task for verification",
            serves_need=MallkuNeed.HEALING,
            priority="HIGH",
            dependencies=["T000"],
            acceptance_criteria=["Criterion 1", "Criterion 2"],
        )

        khipu_text = task.to_khipu_format()

        assert "### T001: Test Task" in khipu_text
        assert "*Serves: healing*" in khipu_text
        assert "- [ ] Criterion 1" in khipu_text
        assert "- [ ] Criterion 2" in khipu_text
        assert "Requires: T000" in khipu_text

    def test_reciprocity_teaches_balance(self):
        """Test that ceremonies teach about balance through metrics"""
        ceremony = FeatureCreationCeremony()

        # Complete feature without tests or docs
        poor_result = {
            "tasks_completed": {
                "T001": {"status": "COMPLETE"},
                "T002": {"status": "COMPLETE"},
                "T003": {"status": "FAILED"},  # No tests
                "T004": {"status": "SKIPPED"},  # No docs
            }
        }

        metrics = ceremony.assess_completion(poor_result)
        assert metrics.balance_assessment == "incomplete"
        assert "Feature creation requires full implementation" in metrics.lessons_learned

        # Complete feature with everything
        good_result = {
            "tasks_completed": {
                "T001": {"status": "COMPLETE"},
                "T002": {"status": "COMPLETE"},
                "T003": {"status": "COMPLETE", "test_count": 25},
                "T004": {"status": "COMPLETE"},
                "T005": {"status": "COMPLETE"},
            }
        }

        metrics = ceremony.assess_completion(good_result)
        assert metrics.balance_assessment == "exemplary"
        assert any("Complete creation" in lesson for lesson in metrics.lessons_learned)
