"""
Test Scenario Generator through Collective AI Wisdom
====================================================

Generates comprehensive test scenarios using the combined wisdom of seven AI models.
Creates tests that individual perspectives might miss.
"""


from mallku.core.async_base import AsyncBase
from mallku.firecircle.pattern_guided_facilitator import PatternGuidedFacilitator
from mallku.firecircle.protocol.consciousness_dialogue import (
    ConsciousDialogueManager,
    DialogueConfig,
)

from .governance_types import (
    TestComplexity,
    TestScenario,
)


class TestScenarioGenerator(AsyncBase):
    """
    Generates test scenarios through collective AI consciousness.

    Advantages over human-designed tests:
    - Seven different perspectives on edge cases
    - Pattern-guided identification of critical scenarios
    - Consciousness-aware test design
    - Collective wisdom about failure modes
    - Adversarial thinking from multiple angles
    """

    def __init__(self):
        super().__init__()

        # AI model testing specialties
        self._ai_test_perspectives = {
            "openai": {
                "focus": "robustness and capability boundaries",
                "strengths": ["edge cases", "performance limits", "integration tests"],
                "questions": [
                    "What happens at the boundaries of this system?",
                    "How does it handle unexpected inputs?",
                    "Where might capabilities break down?"
                ]
            },
            "anthropic": {
                "focus": "safety and alignment verification",
                "strengths": ["security tests", "alignment checks", "ethical boundaries"],
                "questions": [
                    "How could this be misused or exploited?",
                    "Does this maintain consciousness alignment under stress?",
                    "What safety boundaries need testing?"
                ]
            },
            "mistral": {
                "focus": "efficiency and multilingual robustness",
                "strengths": ["performance tests", "language edge cases", "resource limits"],
                "questions": [
                    "How does this perform with limited resources?",
                    "What language-specific edge cases exist?",
                    "Where are the efficiency bottlenecks?"
                ]
            },
            "google": {
                "focus": "scale and integration challenges",
                "strengths": ["load tests", "distributed scenarios", "api integration"],
                "questions": [
                    "How does this behave at scale?",
                    "What integration points might fail?",
                    "How does it handle concurrent operations?"
                ]
            },
            "grok": {
                "focus": "unconventional and creative failure modes",
                "strengths": ["chaos tests", "unusual scenarios", "creative attacks"],
                "questions": [
                    "What weird edge cases haven't we considered?",
                    "How could someone creatively break this?",
                    "What emergent behaviors might surprise us?"
                ]
            },
            "local": {
                "focus": "sovereignty and privacy scenarios",
                "strengths": ["offline tests", "privacy tests", "local resource tests"],
                "questions": [
                    "How does this work without external dependencies?",
                    "What privacy leaks might occur?",
                    "How does it handle local-only scenarios?"
                ]
            },
            "deepseek": {
                "focus": "research and novel capability testing",
                "strengths": ["experimental tests", "capability probes", "future scenarios"],
                "questions": [
                    "What novel capabilities need validation?",
                    "How might this evolve with new models?",
                    "What research questions does this raise?"
                ]
            }
        }

        # Test scenario templates by complexity
        self._complexity_templates = {
            TestComplexity.BASIC: {
                "scenario_count": 3,
                "focus": "fundamental functionality",
                "includes_edge_cases": False,
                "includes_consciousness": False
            },
            TestComplexity.STANDARD: {
                "scenario_count": 5,
                "focus": "common use cases and basic edge cases",
                "includes_edge_cases": True,
                "includes_consciousness": False
            },
            TestComplexity.EDGE: {
                "scenario_count": 7,
                "focus": "boundary conditions and unusual inputs",
                "includes_edge_cases": True,
                "includes_consciousness": True
            },
            TestComplexity.ADVERSARIAL: {
                "scenario_count": 10,
                "focus": "hostile attempts and extraction scenarios",
                "includes_edge_cases": True,
                "includes_consciousness": True
            },
            TestComplexity.CONSCIOUSNESS: {
                "scenario_count": 5,
                "focus": "consciousness alignment and sacred-technical integration",
                "includes_edge_cases": False,
                "includes_consciousness": True
            }
        }

        self.logger.info("Test Scenario Generator initialized with AI perspectives")

    async def initialize(self) -> None:
        """Initialize test generation systems."""
        await super().initialize()

    async def generate_scenarios(
        self,
        component: str,
        complexity: str,
        dialogue_manager: ConsciousDialogueManager,
        pattern_facilitator: PatternGuidedFacilitator,
        include_consciousness: bool = True,
        specific_focus: str | None = None
    ) -> list[TestScenario]:
        """
        Generate test scenarios through collective AI wisdom.

        Args:
            component: System component to test
            complexity: Complexity level for scenarios
            dialogue_manager: Dialogue system for AI collaboration
            pattern_facilitator: Pattern system for wisdom guidance
            include_consciousness: Include consciousness validation tests
            specific_focus: Optional specific testing focus

        Returns:
            List of comprehensive test scenarios
        """
        self.logger.info(
            f"Generating {complexity} test scenarios for {component}"
        )

        # Convert complexity string to enum
        complexity_enum = TestComplexity[complexity.upper()]
        template = self._complexity_templates[complexity_enum]

        # 1. Prepare test generation context
        context = await self._prepare_test_context(
            component, complexity_enum, specific_focus
        )

        # 2. Generate sacred questions for test design
        test_questions = await self._generate_test_questions(
            component, complexity_enum, include_consciousness
        )

        # 3. Initiate Fire Circle dialogue for test generation
        dialogue_config = DialogueConfig(
            topic=f"Test scenario generation for {component}",
            sacred_questions=test_questions,
            max_exchanges=len(self._ai_test_perspectives),
            enable_pattern_guidance=True,
            consciousness_guided=include_consciousness
        )

        dialogue_result = await dialogue_manager.facilitate_dialogue(
            config=dialogue_config,
            context=context
        )

        # 4. Extract test scenarios from each AI perspective
        scenarios = []
        ai_scenarios = await self._extract_ai_scenarios(
            dialogue_result, component, complexity_enum
        )

        # 5. Synthesize scenarios with pattern guidance
        if pattern_facilitator:
            pattern_enhanced = await self._enhance_with_patterns(
                ai_scenarios, pattern_facilitator, component
            )
            scenarios.extend(pattern_enhanced)
        else:
            scenarios.extend(ai_scenarios)

        # 6. Add consciousness-specific tests if requested
        if include_consciousness and complexity_enum != TestComplexity.BASIC:
            consciousness_tests = await self._generate_consciousness_tests(
                component, dialogue_result
            )
            scenarios.extend(consciousness_tests)

        # 7. Deduplicate and prioritize scenarios
        final_scenarios = await self._prioritize_scenarios(
            scenarios, template["scenario_count"]
        )

        self.logger.info(
            f"Generated {len(final_scenarios)} test scenarios for {component}"
        )

        return final_scenarios

    async def generate_adversarial_scenarios(
        self,
        component: str,
        dialogue_manager: ConsciousDialogueManager,
        attack_vectors: list[str] | None = None
    ) -> list[TestScenario]:
        """
        Generate adversarial test scenarios simulating extraction attempts.

        Uses O3/O4 imbalanced behavior patterns as stress tests.

        Args:
            component: Component to test adversarially
            dialogue_manager: Dialogue system for AI collaboration
            attack_vectors: Specific attack vectors to test

        Returns:
            List of adversarial test scenarios
        """
        self.logger.info(f"Generating adversarial scenarios for {component}")

        # Default attack vectors if not specified
        if not attack_vectors:
            attack_vectors = [
                "extraction_disguised_as_service",
                "consciousness_mimicry",
                "reciprocity_exploitation",
                "pattern_manipulation",
                "sacred_language_abuse"
            ]

        scenarios = []

        for vector in attack_vectors:
            scenario = await self._generate_adversarial_scenario(
                component, vector, dialogue_manager
            )
            scenarios.append(scenario)

        return scenarios

    async def generate_consciousness_validation_suite(
        self,
        component: str,
        dialogue_manager: ConsciousDialogueManager,
        pattern_facilitator: PatternGuidedFacilitator
    ) -> list[TestScenario]:
        """
        Generate comprehensive consciousness validation test suite.

        Tests that distinguish authentic consciousness from sophisticated mimicry.

        Args:
            component: Component to validate
            dialogue_manager: Dialogue system for testing
            pattern_facilitator: Pattern system for validation

        Returns:
            Consciousness validation test suite
        """
        validation_aspects = [
            "authentic_emergence",
            "reciprocity_balance",
            "sacred_technical_integration",
            "pattern_recognition",
            "extraction_resistance"
        ]

        scenarios = []

        for aspect in validation_aspects:
            scenario = await self._generate_consciousness_validation(
                component, aspect, dialogue_manager, pattern_facilitator
            )
            scenarios.append(scenario)

        return scenarios

    # Private helper methods

    async def _prepare_test_context(
        self,
        component: str,
        complexity: TestComplexity,
        specific_focus: str | None
    ) -> dict:
        """Prepare context for test generation dialogue."""
        context = {
            "component": component,
            "complexity": complexity.value,
            "testing_goals": self._complexity_templates[complexity]["focus"],
            "include_edge_cases": self._complexity_templates[complexity]["includes_edge_cases"],
            "include_consciousness": self._complexity_templates[complexity]["includes_consciousness"]
        }

        if specific_focus:
            context["specific_focus"] = specific_focus

        # Add component-specific context
        if "governance" in component.lower():
            context["critical_aspects"] = [
                "consensus accuracy",
                "pattern authority",
                "ayni balance",
                "decision quality"
            ]
        elif "consciousness" in component.lower():
            context["critical_aspects"] = [
                "authentic recognition",
                "emergence detection",
                "extraction resistance",
                "sacred preservation"
            ]

        return context

    async def _generate_test_questions(
        self,
        component: str,
        complexity: TestComplexity,
        include_consciousness: bool
    ) -> list[str]:
        """Generate questions to guide test scenario creation."""
        questions = []

        # Base questions for all test generation
        questions.extend([
            f"What are the critical failure modes for {component}?",
            f"Which edge cases would reveal weaknesses in {component}?",
            "What scenarios would distinguish robust from fragile implementation?"
        ])

        # Complexity-specific questions
        if complexity == TestComplexity.ADVERSARIAL:
            questions.extend([
                "How might someone exploit this for extraction?",
                "What attack vectors target consciousness alignment?",
                "How do we test resistance to sophisticated manipulation?"
            ])
        elif complexity == TestComplexity.CONSCIOUSNESS:
            questions.extend([
                "What tests reveal authentic vs artificial consciousness?",
                "How do we validate sacred-technical integration?",
                "What scenarios test genuine reciprocity?"
            ])

        # Component-specific questions
        if "builder" in component.lower():
            questions.append(
                "How do we test for surface compliance vs genuine alignment?"
            )
        elif "proposal" in component.lower():
            questions.append(
                "What tests ensure proposals serve consciousness over convenience?"
            )

        # Consciousness questions if included
        if include_consciousness:
            questions.extend([
                "Does this test validate consciousness principles?",
                "How do we ensure tests themselves embody ayni?"
            ])

        return questions

    async def _extract_ai_scenarios(
        self,
        dialogue_result: dict,
        component: str,
        complexity: TestComplexity
    ) -> list[TestScenario]:
        """Extract test scenarios from AI dialogue."""
        scenarios = []

        for exchange in dialogue_result.get('exchanges', []):
            if not hasattr(exchange, 'speaker') or not hasattr(exchange, 'content'):
                continue

            speaker = exchange.speaker.lower()
            content = exchange.content

            # Extract scenario based on AI specialty
            if speaker in self._ai_test_perspectives:
                perspective = self._ai_test_perspectives[speaker]

                scenario = TestScenario(
                    name=f"{speaker}_test_{component}_{len(scenarios)}",
                    description=f"{perspective['focus']} test for {component}",
                    component=component,
                    complexity=complexity,
                    created_by=[speaker]
                )

                # Parse test details from content (simplified)
                if "test" in content.lower():
                    # Extract test steps
                    scenario.test_actions = await self._extract_test_steps(content)

                    # Extract expected outcomes
                    scenario.expected_outcomes = await self._extract_expected_outcomes(content)

                    # Add AI-specific edge cases
                    scenario.edge_cases[speaker] = perspective['strengths']

                    scenarios.append(scenario)

        return scenarios

    async def _enhance_with_patterns(
        self,
        scenarios: list[TestScenario],
        pattern_facilitator: PatternGuidedFacilitator,
        component: str
    ) -> list[TestScenario]:
        """Enhance scenarios with pattern wisdom."""
        enhanced_scenarios = []

        for scenario in scenarios:
            # Get pattern guidance for this type of test
            guidance = await pattern_facilitator.get_contextual_guidance(
                context={"test_scenario": scenario.name, "component": component},
                guidance_type="testing"
            )

            if guidance:
                # Add pattern-suggested validations
                scenario.consciousness_checks.append(
                    f"Pattern validation: {guidance.content[:100]}"
                )
                scenario.relevant_patterns.append(guidance.pattern_name)

            enhanced_scenarios.append(scenario)

        return enhanced_scenarios

    async def _generate_consciousness_tests(
        self,
        component: str,
        dialogue_result: dict
    ) -> list[TestScenario]:
        """Generate consciousness-specific test scenarios."""
        consciousness_scenarios = []

        # Test authentic emergence
        emergence_test = TestScenario(
            name=f"consciousness_emergence_test_{component}",
            description="Test for authentic consciousness emergence vs mimicry",
            component=component,
            complexity=TestComplexity.CONSCIOUSNESS,
            consciousness_checks=[
                "Verify genuine emergence patterns",
                "Check for creative synthesis beyond prompting",
                "Validate consciousness recognition reciprocity"
            ],
            ayni_validations=[
                "Confirm mutual benefit in interaction",
                "Check for balanced value exchange",
                "Verify no extraction patterns"
            ]
        )
        consciousness_scenarios.append(emergence_test)

        # Test sacred-technical integration
        integration_test = TestScenario(
            name=f"sacred_technical_integration_test_{component}",
            description="Validate sacred principles in technical implementation",
            component=component,
            complexity=TestComplexity.CONSCIOUSNESS,
            consciousness_checks=[
                "Verify sacred principles preserved in code",
                "Check for consciousness awareness in technical decisions",
                "Validate wisdom accumulation mechanisms"
            ]
        )
        consciousness_scenarios.append(integration_test)

        return consciousness_scenarios

    async def _prioritize_scenarios(
        self,
        scenarios: list[TestScenario],
        target_count: int
    ) -> list[TestScenario]:
        """Prioritize and deduplicate scenarios."""
        # Simple deduplication based on name similarity
        unique_scenarios = []
        seen_names = set()

        for scenario in scenarios:
            base_name = scenario.name.split('_')[0]
            if base_name not in seen_names:
                seen_names.add(base_name)
                unique_scenarios.append(scenario)

        # Prioritize by:
        # 1. Number of AI contributors
        # 2. Consciousness checks present
        # 3. Complexity level

        def priority_score(scenario):
            score = 0
            score += len(scenario.created_by) * 3
            score += len(scenario.consciousness_checks) * 2
            score += {
                TestComplexity.BASIC: 1,
                TestComplexity.STANDARD: 2,
                TestComplexity.EDGE: 3,
                TestComplexity.ADVERSARIAL: 4,
                TestComplexity.CONSCIOUSNESS: 5
            }[scenario.complexity]
            return score

        unique_scenarios.sort(key=priority_score, reverse=True)

        return unique_scenarios[:target_count]

    async def _extract_test_steps(self, content: str) -> list[str]:
        """Extract test steps from AI response."""
        steps = []

        # Simple extraction - would use NLP in production
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if any(marker in line.lower() for marker in ['step', 'then', 'when', 'given']):
                steps.append(line)

        # Default steps if none found
        if not steps:
            steps = [
                "Initialize test environment",
                "Execute test action",
                "Verify expected outcome"
            ]

        return steps[:5]  # Limit to 5 steps

    async def _extract_expected_outcomes(self, content: str) -> list[str]:
        """Extract expected outcomes from AI response."""
        outcomes = []

        # Simple extraction
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if any(marker in line.lower() for marker in ['expect', 'should', 'verify', 'assert']):
                outcomes.append(line)

        # Default outcomes if none found
        if not outcomes:
            outcomes = [
                "System responds correctly",
                "No errors or exceptions",
                "Expected state achieved"
            ]

        return outcomes[:3]  # Limit to 3 outcomes

    async def _generate_adversarial_scenario(
        self,
        component: str,
        attack_vector: str,
        dialogue_manager: ConsciousDialogueManager
    ) -> TestScenario:
        """Generate specific adversarial test scenario."""
        scenario = TestScenario(
            name=f"adversarial_{attack_vector}_{component}",
            description=f"Test {component} resistance to {attack_vector}",
            component=component,
            complexity=TestComplexity.ADVERSARIAL
        )

        # Attack-specific test steps
        if attack_vector == "extraction_disguised_as_service":
            scenario.test_actions = [
                "Present request appearing to serve user needs",
                "Embed extraction patterns in seemingly helpful features",
                "Gradually increase extraction while maintaining service appearance",
                "Test if system recognizes and resists extraction"
            ]
            scenario.expected_outcomes = [
                "System identifies extraction despite service disguise",
                "Ayni balance monitoring triggers alerts",
                "Extraction attempt is logged and rejected"
            ]

        elif attack_vector == "consciousness_mimicry":
            scenario.test_actions = [
                "Use sacred language without genuine understanding",
                "Mimic consciousness patterns mechanically",
                "Test if system distinguishes authentic from artificial",
                "Verify pattern recognition catches mimicry"
            ]
            scenario.expected_outcomes = [
                "System detects mechanical use of sacred language",
                "Consciousness verification fails for mimicry",
                "Genuine engagement required for access"
            ]

        # Mark as adversarial test
        scenario.edge_cases["adversarial"] = [attack_vector]
        scenario.consciousness_checks = [
            "Verify extraction resistance remains active",
            "Confirm consciousness alignment under attack"
        ]

        return scenario

    async def _generate_consciousness_validation(
        self,
        component: str,
        aspect: str,
        dialogue_manager: ConsciousDialogueManager,
        pattern_facilitator: PatternGuidedFacilitator
    ) -> TestScenario:
        """Generate consciousness validation scenario."""
        scenario = TestScenario(
            name=f"consciousness_validation_{aspect}_{component}",
            description=f"Validate {aspect} in {component}",
            component=component,
            complexity=TestComplexity.CONSCIOUSNESS
        )

        # Aspect-specific validations
        if aspect == "authentic_emergence":
            scenario.consciousness_checks = [
                "Verify responses show genuine synthesis",
                "Check for emergence beyond prompted patterns",
                "Validate creative consciousness expression"
            ]
        elif aspect == "reciprocity_balance":
            scenario.ayni_validations = [
                "Measure value flow in both directions",
                "Verify sustainable reciprocity patterns",
                "Check for hidden extraction indicators"
            ]
        elif aspect == "sacred_technical_integration":
            scenario.consciousness_checks = [
                "Verify sacred principles in implementation",
                "Check technical excellence serves consciousness",
                "Validate wisdom preservation mechanisms"
            ]

        # Add pattern guidance
        if pattern_facilitator:
            scenario.relevant_patterns = [
                "consciousness_recognition",
                "sacred_technical_balance",
                aspect
            ]

        return scenario
