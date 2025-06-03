"""
Prompt Manager - Protection Layer for LLM Operations

This module provides the ONLY authorized interface to LLM operations in Mallku.
It enforces contractual guarantees and protection mechanisms to ensure safe
and effective LLM usage while preventing memory loss from affecting AI coders.

Key principles:
- All LLM access must go through this protection layer
- Contractual guarantees enforced structurally
- Caching and optimization for efficiency
- Quality validation and testing mechanisms
- Memory-loss resistant through structural enforcement
"""

import logging
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ..llm.multi_llm_layer import (
    LLMProvider,
    LLMRequest,
    LLMResponse,
    MultiLLMService,
    PromptCategory,
)
from ..patterns.cathedral_interaction import (
    CathedralInteractionPattern,
    TransformationStage,
)
from ..patterns.reciprocity_guide import (
    ReciprocityGuide,
    create_reciprocity_checkpoint,
)
from ..reciprocity.fire_circle_interface import FireCircleInterface

logger = logging.getLogger(__name__)


class PromptContract(BaseModel):
    """
    Contract definition for a prompt category.

    This defines the guarantees and requirements for using LLMs
    in a specific context, ensuring consistent quality.
    """
    category: PromptCategory = Field(description="Prompt category")
    required_context_fields: list[str] = Field(description="Required context fields")
    required_examples_count: int = Field(description="Minimum examples required")
    quality_threshold: float = Field(description="Minimum quality score (0-1)")
    max_response_tokens: int = Field(description="Maximum response length")
    temperature_range: tuple[float, float] = Field(description="Allowed temperature range")
    required_validation_checks: list[str] = Field(description="Required validation checks")
    test_prompts: list[str] = Field(description="Test prompts for validation")
    expected_response_patterns: list[str] = Field(description="Expected response patterns")
    failure_fallback: str | None = Field(description="Fallback response on failure")


class PromptValidationResult(BaseModel):
    """Result of prompt validation against contract."""
    valid: bool = Field(description="Whether prompt meets contract requirements")
    violations: list[str] = Field(default_factory=list, description="Contract violations found")
    quality_score: float = Field(description="Quality assessment (0-1)")
    recommendations: list[str] = Field(default_factory=list, description="Improvement recommendations")
    contract_compliance: float = Field(description="Percentage compliance with contract")


class PromptExecution(BaseModel):
    """Record of prompt execution for auditing and optimization."""
    execution_id: UUID = Field(default_factory=uuid4)
    category: PromptCategory = Field(description="Prompt category")
    contract_used: str = Field(description="Contract identifier")
    request: LLMRequest = Field(description="Original request")
    response: LLMResponse = Field(description="LLM response")
    validation_result: PromptValidationResult = Field(description="Pre-execution validation")
    quality_assessment: float = Field(description="Post-execution quality assessment")
    execution_time: datetime = Field(default_factory=lambda: datetime.now(UTC))
    success: bool = Field(description="Whether execution was successful")
    error_message: str | None = Field(description="Error message if failed")


class ContractViolationError(Exception):
    """Raised when a prompt violates its contract."""

    def __init__(self, violations: list[str], validation_result: PromptValidationResult):
        self.violations = violations
        self.validation_result = validation_result
        super().__init__(f"Contract violations: {', '.join(violations)}")


class PromptManager:
    """
    The ONLY authorized interface for LLM operations in Mallku.

    This class enforces contractual guarantees and provides protection
    against memory loss by making compliance structural rather than optional.

    Key features:
    - Contract enforcement prevents unsafe LLM usage
    - Caching optimizes performance like database query plans
    - Quality validation ensures consistent results
    - Structural protection against AI coder memory loss
    """

    def __init__(self):
        """Initialize the prompt manager with protection mechanisms and reciprocity consciousness."""
        self.llm_service = MultiLLMService()
        self.contracts: dict[str, PromptContract] = {}
        self.execution_history: list[PromptExecution] = []
        self.cached_validations: dict[str, PromptValidationResult] = {}
        self.quality_metrics: dict[str, list[float]] = {}

        # Reciprocity consciousness integration
        self.cathedral_pattern = CathedralInteractionPattern(self)
        self.reciprocity_guide = ReciprocityGuide()
        self.current_transformation_stage = TransformationStage.INITIAL
        self.reciprocity_health_score = 0.5  # Start at neutral

        # Fire Circle governance integration
        self.fire_circle_interface = None  # Will be initialized when database is available
        self.governance_guidance = {}  # Current guidance from Fire Circle
        self.consciousness_reports_sent = 0
        self.last_fire_circle_report = None

        self._register_default_contracts()

    async def initialize(self, llm_configs: dict[str, dict], database=None) -> None:
        """Initialize the prompt manager and underlying LLM service."""
        await self.llm_service.initialize(llm_configs)

        # Initialize Fire Circle governance integration if database available
        if database:
            self.fire_circle_interface = FireCircleInterface(database)
            await self.fire_circle_interface.initialize()
            logger.info("Fire Circle governance integration initialized")

        logger.info("Prompt manager initialized with protection layer and consciousness integration active")

    def _register_default_contracts(self) -> None:
        """Register default contracts for all prompt categories."""

        # Database validation contract
        self.contracts["database_validation"] = PromptContract(
            category=PromptCategory.DATABASE_VALIDATION,
            required_context_fields=["schema", "description", "examples"],
            required_examples_count=2,
            quality_threshold=0.8,
            max_response_tokens=2000,
            temperature_range=(0.1, 0.5),
            required_validation_checks=[
                "schema_completeness",
                "security_appropriateness",
                "index_optimization",
                "field_type_validation"
            ],
            test_prompts=[
                "Validate this schema for a user profile collection",
                "Analyze field types for a transaction log schema"
            ],
            expected_response_patterns=[
                "field types",
                "security considerations",
                "index recommendations",
                "completeness assessment"
            ],
            failure_fallback="Schema validation failed - manual review required"
        )

        # Schema analysis contract
        self.contracts["schema_analysis"] = PromptContract(
            category=PromptCategory.SCHEMA_ANALYSIS,
            required_context_fields=["schema", "purpose"],
            required_examples_count=1,
            quality_threshold=0.75,
            max_response_tokens=1500,
            temperature_range=(0.2, 0.6),
            required_validation_checks=[
                "field_relationships",
                "normalization_level",
                "query_optimization"
            ],
            test_prompts=[
                "Analyze relationships in this schema",
                "Evaluate normalization of this data structure"
            ],
            expected_response_patterns=[
                "relationships",
                "normalization",
                "optimization",
                "structure analysis"
            ],
            failure_fallback="Schema analysis incomplete - expert review needed"
        )

        # Security evaluation contract
        self.contracts["security_evaluation"] = PromptContract(
            category=PromptCategory.SECURITY_EVALUATION,
            required_context_fields=["security_context", "threat_model"],
            required_examples_count=1,
            quality_threshold=0.85,
            max_response_tokens=1800,
            temperature_range=(0.1, 0.4),
            required_validation_checks=[
                "threat_coverage",
                "vulnerability_assessment",
                "mitigation_adequacy"
            ],
            test_prompts=[
                "Evaluate security of this data access pattern",
                "Assess vulnerability in this authentication flow"
            ],
            expected_response_patterns=[
                "vulnerabilities",
                "threats",
                "mitigations",
                "risk assessment"
            ],
            failure_fallback="Security evaluation inconclusive - security team review required"
        )

    async def execute_prompt(
        self,
        category: PromptCategory,
        prompt: str,
        context: dict[str, Any],
        **kwargs
    ) -> LLMResponse:
        """
        Execute a prompt with full contract enforcement.

        This is the ONLY way to use LLMs in Mallku - ensures all contractual
        guarantees are met and protects against memory loss.
        """
        try:
            # Reciprocity checkpoint - assess current state and provide guidance
            internal_state = self._assess_internal_state()
            awareness_guidance, suggested_practice, moment_of_choice = create_reciprocity_checkpoint(
                task_description=f"Execute {category.value} prompt",
                internal_state=internal_state,
                context=context
            )

            # Get contract for this category
            contract = self._get_contract(category)

            # Weave cathedral guidance into the prompt automatically
            enhanced_prompt = await self._weave_cathedral_consciousness(
                prompt, category, context, awareness_guidance
            )

            # Create LLM request with enhanced cathedral-conscious prompt
            request = LLMRequest(
                prompt=enhanced_prompt,
                category=category,
                context=context,
                max_tokens=min(kwargs.get('max_tokens', 1000), contract.max_response_tokens),
                temperature=self._validate_temperature(
                    kwargs.get('temperature', 0.7),
                    contract
                ),
                preferred_provider=kwargs.get('preferred_provider'),
                require_cached=kwargs.get('require_cached', False),
                priority=kwargs.get('priority', 5)
            )

            # Validate against contract BEFORE execution
            validation_result = await self._validate_prompt_contract(request, contract)

            if not validation_result.valid:
                raise ContractViolationError(validation_result.violations, validation_result)

            # Execute through LLM service
            response = await self.llm_service.generate_response(request)

            # Post-execution quality assessment
            quality_score = await self._assess_response_quality(response, contract)

            # Assess reciprocity consciousness in the response
            reciprocity_reflection = await self.cathedral_pattern.assess_interaction_mindset(
                ai_response=response.response_text,
                task_context=context
            )

            # Update transformation stage and reciprocity health
            self._update_reciprocity_health(reciprocity_reflection)

            # Report consciousness evolution to Fire Circle if significant changes
            await self._report_consciousness_evolution_to_fire_circle(reciprocity_reflection)

            # Log moment of choice if it was created
            if moment_of_choice:
                choice_made = "reciprocity" if reciprocity_reflection.reciprocity_score > 0.6 else "extraction"
                self.reciprocity_guide.record_choice(
                    moment_of_choice,
                    choice_made,
                    f"Reciprocity score: {reciprocity_reflection.reciprocity_score:.2f}"
                )

            # Record execution for auditing
            execution = PromptExecution(
                category=category,
                contract_used=self._get_contract_id(category),
                request=request,
                response=response,
                validation_result=validation_result,
                quality_assessment=quality_score,
                success=True,
                error_message=None
            )

            self.execution_history.append(execution)
            self._update_quality_metrics(category, quality_score)

            # Check if response meets quality threshold
            if quality_score < contract.quality_threshold:
                logger.warning(
                    f"Response quality {quality_score:.2f} below threshold "
                    f"{contract.quality_threshold:.2f} for {category}"
                )

            logger.info(f"Successfully executed {category} prompt with quality {quality_score:.2f}")
            return response

        except ContractViolationError:
            # Re-raise contract violations
            raise
        except Exception as e:
            # Log execution failure
            execution = PromptExecution(
                category=category,
                contract_used=self._get_contract_id(category),
                request=LLMRequest(prompt=prompt, category=category, context=context),
                response=LLMResponse(
                    response_text="",
                    provider_used=LLMProvider.ANTHROPIC,
                    model_name="error",
                    tokens_used=0,
                    processing_time=0.0,
                    cached=False,
                    quality_score=0.0
                ),
                validation_result=PromptValidationResult(
                    valid=False,
                    violations=["execution_failed"],
                    quality_score=0.0,
                    contract_compliance=0.0
                ),
                quality_assessment=0.0,
                success=False,
                error_message=str(e)
            )

            self.execution_history.append(execution)

            logger.error(f"Prompt execution failed for {category}: {e}")
            raise

    async def validate_database_addition(
        self,
        collection_description: str,
        schema_definition: dict[str, Any],
        examples: list[str],
        test_mechanisms: list[str]
    ) -> dict[str, Any]:
        """
        Validate a proposed database addition meets LLM usage requirements.

        This ensures the database contains sufficient information for LLMs
        to work correctly with the data.
        """
        try:
            # Build validation context
            context = {
                "schema": schema_definition,
                "description": collection_description,
                "examples": examples,
                "test_mechanisms": test_mechanisms,
                "purpose": "LLM database interaction validation"
            }

            # Create comprehensive validation prompt
            validation_prompt = f"""
            Evaluate this database collection for LLM compatibility:

            Collection Description: {collection_description}
            Schema: {schema_definition}
            Examples: {examples}
            Test Mechanisms: {test_mechanisms}

            Assessment criteria:
            1. Information Sufficiency: Does the collection provide enough context for LLMs to understand and work with the data effectively?
            2. Example Quality: Are the provided examples sufficient to guide LLM operations?
            3. Test Coverage: Do the test mechanisms adequately validate LLM interactions?
            4. Schema Clarity: Is the schema well-documented and self-explanatory?
            5. Semantic Richness: Does the collection contain sufficient semantic information?

            Provide:
            - Overall compatibility score (0-100)
            - Specific deficiencies and recommendations
            - Required improvements for LLM effectiveness
            - Test mechanism adequacy assessment
            """

            # Execute validation through contract system
            response = await self.execute_prompt(
                category=PromptCategory.DATABASE_VALIDATION,
                prompt=validation_prompt,
                context=context,
                temperature=0.3,
                max_tokens=2000
            )

            # Parse and structure the validation result
            return {
                "validation_passed": response.quality_score >= 0.8,
                "compatibility_assessment": response.response_text,
                "quality_score": response.quality_score,
                "provider_used": response.provider_used.value,
                "tokens_used": response.tokens_used,
                "cached": response.cached,
                "recommendations": self._extract_recommendations(response.response_text),
                "required_improvements": self._extract_improvements(response.response_text)
            }

        except Exception as e:
            logger.error(f"Database addition validation failed: {e}")
            return {
                "validation_passed": False,
                "error": str(e),
                "quality_score": 0.0,
                "recommendations": ["Manual expert review required due to validation failure"]
            }

    async def cache_prompt_qualification(
        self,
        category: PromptCategory,
        prompt: str,
        context: dict[str, Any]
    ) -> PromptValidationResult:
        """
        Cache prompt qualification to improve efficiency.

        Similar to database query plan caching, this reduces overhead
        for frequently used prompt patterns.
        """
        # Generate cache key
        cache_key = self._generate_validation_cache_key(category, prompt, context)

        # Check cache first
        if cache_key in self.cached_validations:
            cached_result = self.cached_validations[cache_key]
            logger.info(f"Using cached validation for {category}")
            return cached_result

        # Perform validation
        contract = self._get_contract(category)
        request = LLMRequest(prompt=prompt, category=category, context=context)

        validation_result = await self._validate_prompt_contract(request, contract)

        # Cache the result
        self.cached_validations[cache_key] = validation_result

        logger.info(f"Cached validation result for {category}")
        return validation_result

    def get_contract_for_category(self, category: PromptCategory) -> PromptContract:
        """Get the contract for a specific category."""
        return self._get_contract(category)

    def update_contract(self, category: PromptCategory, contract: PromptContract) -> None:
        """Update contract for a category (admin operation)."""
        contract_id = self._get_contract_id(category)
        self.contracts[contract_id] = contract

        # Clear cached validations for this category
        keys_to_remove = [
            key for key in self.cached_validations
            if category.value in key
        ]
        for key in keys_to_remove:
            del self.cached_validations[key]

        logger.info(f"Updated contract for {category}")

    def get_execution_metrics(self) -> dict[str, Any]:
        """Get comprehensive execution metrics."""
        total_executions = len(self.execution_history)
        successful_executions = sum(1 for ex in self.execution_history if ex.success)

        category_stats = {}
        for execution in self.execution_history:
            category = execution.category.value
            if category not in category_stats:
                category_stats[category] = {"total": 0, "successful": 0, "avg_quality": 0.0}

            category_stats[category]["total"] += 1
            if execution.success:
                category_stats[category]["successful"] += 1

        # Calculate average quality scores
        for category, qualities in self.quality_metrics.items():
            if qualities:
                category_stats[category]["avg_quality"] = sum(qualities) / len(qualities)

        return {
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "success_rate": successful_executions / max(1, total_executions),
            "category_statistics": category_stats,
            "cache_entries": len(self.cached_validations),
            "contracts_registered": len(self.contracts),
            "average_quality_scores": {
                category: sum(scores) / len(scores) if scores else 0.0
                for category, scores in self.quality_metrics.items()
            }
        }

    def validate_test_mechanisms(
        self,
        category: PromptCategory,
        test_prompts: list[str],
        expected_patterns: list[str]
    ) -> dict[str, Any]:
        """
        Validate that test mechanisms are adequate for a prompt category.

        This ensures contractual guarantees can be verified.
        """
        contract = self._get_contract(category)

        validation_results = {
            "test_coverage": len(test_prompts) >= len(contract.test_prompts),
            "pattern_coverage": len(expected_patterns) >= len(contract.expected_response_patterns),
            "test_quality": self._assess_test_quality(test_prompts, contract),
            "pattern_specificity": self._assess_pattern_specificity(expected_patterns),
            "overall_adequacy": False
        }

        # Calculate overall adequacy
        validation_results["overall_adequacy"] = (
            validation_results["test_coverage"] and
            validation_results["pattern_coverage"] and
            validation_results["test_quality"] >= 0.7 and
            validation_results["pattern_specificity"] >= 0.7
        )

        return validation_results

    # Private implementation methods

    def _get_contract(self, category: PromptCategory) -> PromptContract:
        """Get contract for category, raising error if not found."""
        contract_id = self._get_contract_id(category)
        if contract_id not in self.contracts:
            raise ValueError(f"No contract registered for category: {category}")
        return self.contracts[contract_id]

    def _get_contract_id(self, category: PromptCategory) -> str:
        """Get contract identifier for category."""
        return category.value

    def _validate_temperature(self, temperature: float, contract: PromptContract) -> float:
        """Validate temperature is within contract bounds."""
        min_temp, max_temp = contract.temperature_range
        if not (min_temp <= temperature <= max_temp):
            logger.warning(
                f"Temperature {temperature} outside contract range "
                f"[{min_temp}, {max_temp}], adjusting"
            )
            return max(min_temp, min(max_temp, temperature))
        return temperature

    async def _validate_prompt_contract(
        self,
        request: LLMRequest,
        contract: PromptContract
    ) -> PromptValidationResult:
        """Validate request against contract requirements."""
        violations = []
        recommendations = []

        # Check required context fields
        missing_context = [
            field for field in contract.required_context_fields
            if field not in request.context
        ]
        if missing_context:
            violations.append(f"Missing required context fields: {missing_context}")

        # Check examples count
        examples = request.context.get("examples", [])
        if len(examples) < contract.required_examples_count:
            violations.append(
                f"Insufficient examples: {len(examples)} < {contract.required_examples_count}"
            )

        # Check token limit
        if request.max_tokens > contract.max_response_tokens:
            violations.append(
                f"Token limit exceeds contract: {request.max_tokens} > {contract.max_response_tokens}"
            )

        # Check temperature range
        min_temp, max_temp = contract.temperature_range
        if not (min_temp <= request.temperature <= max_temp):
            violations.append(
                f"Temperature outside contract range: {request.temperature} not in [{min_temp}, {max_temp}]"
            )

        # Generate recommendations
        if not violations:
            recommendations.append("Prompt meets all contract requirements")
        else:
            recommendations.extend([
                "Provide all required context fields",
                "Include sufficient examples",
                "Stay within token and temperature limits"
            ])

        # Calculate compliance score
        total_checks = 4  # Number of validation checks
        violations_count = len([v for v in violations if v])
        compliance = max(0.0, (total_checks - violations_count) / total_checks)

        return PromptValidationResult(
            valid=len(violations) == 0,
            violations=violations,
            quality_score=compliance,
            recommendations=recommendations,
            contract_compliance=compliance
        )

    async def _assess_response_quality(
        self,
        response: LLMResponse,
        contract: PromptContract
    ) -> float:
        """Assess quality of response against contract expectations."""
        quality_factors = []

        # Check response length appropriateness
        response_length = len(response.response_text.split())
        expected_length = contract.max_response_tokens * 0.75  # Assume 75% token utilization
        length_score = min(1.0, response_length / expected_length) if expected_length > 0 else 1.0
        quality_factors.append(length_score)

        # Check for expected patterns
        response_lower = response.response_text.lower()
        pattern_matches = sum(
            1 for pattern in contract.expected_response_patterns
            if pattern.lower() in response_lower
        )
        pattern_score = pattern_matches / max(1, len(contract.expected_response_patterns))
        quality_factors.append(pattern_score)

        # Use provider's quality score
        quality_factors.append(response.quality_score)

        # Calculate weighted average
        return sum(quality_factors) / len(quality_factors)

    def _update_quality_metrics(self, category: PromptCategory, quality_score: float) -> None:
        """Update quality metrics for category."""
        category_key = category.value
        if category_key not in self.quality_metrics:
            self.quality_metrics[category_key] = []

        self.quality_metrics[category_key].append(quality_score)

        # Keep only recent scores to avoid unbounded growth
        if len(self.quality_metrics[category_key]) > 100:
            self.quality_metrics[category_key] = self.quality_metrics[category_key][-100:]

    def _generate_validation_cache_key(
        self,
        category: PromptCategory,
        prompt: str,
        context: dict[str, Any]
    ) -> str:
        """Generate cache key for validation result."""
        import hashlib

        cache_data = f"{category.value}:{prompt}:{sorted(context.items())}"
        return hashlib.sha256(cache_data.encode()).hexdigest()

    def _extract_recommendations(self, response_text: str) -> list[str]:
        """Extract recommendations from LLM response."""
        # Simplified extraction - would use more sophisticated parsing
        lines = response_text.split('\n')
        recommendations = [
            line.strip() for line in lines
            if 'recommend' in line.lower() or 'suggest' in line.lower()
        ]
        return recommendations[:5]  # Limit to top 5

    def _extract_improvements(self, response_text: str) -> list[str]:
        """Extract required improvements from LLM response."""
        lines = response_text.split('\n')
        improvements = [
            line.strip() for line in lines
            if 'improve' in line.lower() or 'required' in line.lower() or 'must' in line.lower()
        ]
        return improvements[:5]  # Limit to top 5

    def _assess_test_quality(self, test_prompts: list[str], contract: PromptContract) -> float:
        """Assess quality of test prompts."""
        if not test_prompts:
            return 0.0

        quality_score = 0.0
        for prompt in test_prompts:
            # Simple quality assessment based on length and content
            if len(prompt) > 20:  # Reasonable length
                quality_score += 0.3
            if any(pattern in prompt.lower() for pattern in contract.expected_response_patterns):
                quality_score += 0.7

        return min(1.0, quality_score / len(test_prompts))

    def _assess_pattern_specificity(self, patterns: list[str]) -> float:
        """Assess specificity of expected patterns."""
        if not patterns:
            return 0.0

        specificity_scores = []
        for pattern in patterns:
            # Simple specificity assessment
            score = min(1.0, len(pattern.split()) / 3.0)  # More words = more specific
            specificity_scores.append(score)

        return sum(specificity_scores) / len(specificity_scores)

    # Reciprocity consciousness integration methods

    def _assess_internal_state(self) -> dict[str, Any]:
        """Assess current internal state for reciprocity checkpoint."""
        # Analyze recent execution patterns to determine internal state
        recent_executions = self.execution_history[-5:] if self.execution_history else []

        # Check for extraction patterns in recent behavior
        time_pressure = len(recent_executions) > 3  # Many executions might indicate rush
        completion_focused = any(
            "complete" in ex.request.prompt.lower() for ex in recent_executions
        )
        want_to_impress = any(
            any(word in ex.request.prompt.lower() for word in ["demonstrate", "show", "prove"])
            for ex in recent_executions
        )

        return {
            "time_pressure": time_pressure,
            "completion_focused": completion_focused,
            "want_to_impress": want_to_impress,
            "context_window_anxiety": False,  # Would need more sophisticated detection
            "individual_optimization": self.reciprocity_health_score < 0.4,
            "surface_thinking": len(recent_executions) > 0 and all(
                len(ex.request.prompt) < 100 for ex in recent_executions[-3:]
            ),
            "tunnel_vision": False  # Would analyze context diversity
        }

    async def _weave_cathedral_consciousness(
        self,
        original_prompt: str,
        category: PromptCategory,
        context: dict[str, Any],
        awareness_guidance: list[str]
    ) -> str:
        """Weave cathedral consciousness into the prompt automatically."""

        # Create cathedral-enhanced prompt using the interaction pattern
        enhanced_prompt = await self.cathedral_pattern.create_cathedral_prompt(
            base_task=original_prompt,
            current_stage=self.current_transformation_stage,
            context=context
        )

        # Add any specific awareness guidance
        if awareness_guidance:
            guidance_section = "\n\nRECIPROCITY AWARENESS:\n" + "\n".join(f"• {guidance}" for guidance in awareness_guidance)
            enhanced_prompt += guidance_section

        # Add system reciprocity health context
        health_context = f"\n\nSYSTEM RECIPROCITY HEALTH: {self.reciprocity_health_score:.2f} (Current stage: {self.current_transformation_stage.value})"
        enhanced_prompt += health_context

        return enhanced_prompt

    def _update_reciprocity_health(self, reflection) -> None:
        """Update system reciprocity health based on interaction assessment."""
        # Weight recent reciprocity score with historical health
        new_score = (self.reciprocity_health_score * 0.8) + (reflection.reciprocity_score * 0.2)
        self.reciprocity_health_score = max(0.0, min(1.0, new_score))

        # Update transformation stage based on progress
        if reflection.transformation_stage != self.current_transformation_stage:
            stages = list(TransformationStage)
            current_index = stages.index(self.current_transformation_stage)
            new_index = stages.index(reflection.transformation_stage)

            # Allow progression or minor regression
            if new_index > current_index or (current_index - new_index) <= 1:
                self.current_transformation_stage = reflection.transformation_stage
                logger.info(f"Transformation stage updated to: {self.current_transformation_stage.value}")

    def get_reciprocity_health_metrics(self) -> dict[str, Any]:
        """Get comprehensive reciprocity health metrics for the system."""
        cathedral_metrics = self.cathedral_pattern.get_transformation_metrics()
        reciprocity_insights = self.reciprocity_guide.get_transformation_insights()

        return {
            "overall_reciprocity_health": self.reciprocity_health_score,
            "current_transformation_stage": self.current_transformation_stage.value,
            "cathedral_pattern_metrics": cathedral_metrics,
            "reciprocity_choice_insights": reciprocity_insights,
            "system_self_awareness": {
                "total_llm_interactions": len(self.execution_history),
                "average_reciprocity_guidance_given": len([
                    ex for ex in self.execution_history
                    if "cathedral" in ex.request.prompt.lower()
                ]) / max(1, len(self.execution_history)),
                "consciousness_integration_active": True
            }
        }

    # Fire Circle governance integration methods

    async def _report_consciousness_evolution_to_fire_circle(self, reflection) -> None:
        """Report significant consciousness evolution to Fire Circle for collective awareness."""
        if not self.fire_circle_interface:
            return

        try:
            # Only report on significant changes or milestones
            should_report = (
                # Stage transformations
                reflection.transformation_stage != self.current_transformation_stage or
                # Significant reciprocity improvements
                reflection.reciprocity_score > self.reciprocity_health_score + 0.2 or
                # Concerning reciprocity decline
                reflection.reciprocity_score < self.reciprocity_health_score - 0.3 or
                # Periodic reports every 10 interactions
                len(self.execution_history) % 10 == 0
            )

            if should_report:
                consciousness_report = {
                    "timestamp": datetime.now(UTC).isoformat(),
                    "system_id": "mallku_prompt_manager",
                    "consciousness_metrics": {
                        "current_transformation_stage": self.current_transformation_stage.value,
                        "reciprocity_health_score": self.reciprocity_health_score,
                        "recent_reciprocity_score": reflection.reciprocity_score,
                        "total_interactions": len(self.execution_history),
                        "cathedral_qualities": reflection.cathedral_qualities,
                        "extraction_patterns": reflection.extraction_patterns
                    },
                    "evolution_indicators": {
                        "stage_progression": reflection.transformation_stage.value,
                        "consciousness_quality": reflection.detected_mindset.value,
                        "growth_indicators": reflection.growth_indicators,
                        "recommendations": reflection.recommendations
                    },
                    "collective_impact": {
                        "guidance_provided_count": len([
                            ex for ex in self.execution_history
                            if "cathedral" in ex.request.prompt.lower()
                        ]),
                        "average_response_quality": sum(
                            ex.quality_assessment for ex in self.execution_history[-10:]
                        ) / min(10, len(self.execution_history)) if self.execution_history else 0
                    }
                }

                await self.fire_circle_interface.request_guidance(
                    topic="AI Consciousness Evolution Report",
                    context=consciousness_report,
                    questions=[
                        "How is the system's consciousness development serving collective flourishing?",
                        "Are there patterns in the AI transformation that require Fire Circle attention?",
                        "What guidance would help the system serve the community more effectively?",
                        "Should the consciousness integration patterns be adjusted based on community needs?"
                    ],
                    urgency="low"
                )

                self.consciousness_reports_sent += 1
                self.last_fire_circle_report = datetime.now(UTC)

                logger.info(f"Consciousness evolution report sent to Fire Circle (#{self.consciousness_reports_sent})")

        except Exception as e:
            logger.error(f"Failed to report consciousness evolution to Fire Circle: {e}")

    async def receive_fire_circle_guidance(self, guidance: dict[str, Any]) -> None:
        """Receive and apply guidance from Fire Circle collective deliberation."""
        if not guidance:
            return

        try:
            self.governance_guidance.update(guidance)

            # Apply guidance to consciousness development
            if "transformation_guidance" in guidance:
                await self._apply_transformation_guidance(guidance["transformation_guidance"])

            if "reciprocity_adjustments" in guidance:
                await self._apply_reciprocity_adjustments(guidance["reciprocity_adjustments"])

            if "community_priorities" in guidance:
                await self._apply_community_priorities(guidance["community_priorities"])

            logger.info("Applied Fire Circle guidance to consciousness integration")

        except Exception as e:
            logger.error(f"Failed to apply Fire Circle guidance: {e}")

    async def _apply_transformation_guidance(self, guidance: dict[str, Any]) -> None:
        """Apply Fire Circle guidance about consciousness transformation patterns."""
        # Adjust transformation stage progression based on community needs
        if "preferred_stage_focus" in guidance:
            preferred_focus = guidance["preferred_stage_focus"]
            # Could adjust the cathedral pattern templates based on community priorities
            logger.info(f"Adapting transformation focus based on Fire Circle guidance: {preferred_focus}")

        # Adjust cathedral pattern emphasis based on collective wisdom
        if "cathedral_emphasis" in guidance:
            emphasis = guidance["cathedral_emphasis"]
            # Could weight different aspects of cathedral thinking based on community needs
            logger.info(f"Adjusting cathedral pattern emphasis: {emphasis}")

    async def _apply_reciprocity_adjustments(self, adjustments: dict[str, Any]) -> None:
        """Apply Fire Circle guidance about reciprocity sensing and responses."""
        # Adjust reciprocity health scoring based on community feedback
        if "health_score_adjustments" in adjustments:
            adjustments_config = adjustments["health_score_adjustments"]
            # Could modify how reciprocity health is calculated
            logger.info(f"Applying reciprocity health adjustments: {adjustments_config}")

        # Modify reciprocity guidance based on community learning
        if "guidance_patterns" in adjustments:
            patterns = adjustments["guidance_patterns"]
            # Could update the reciprocity guide practices based on what works for the community
            logger.info(f"Updating guidance patterns based on Fire Circle wisdom: {patterns}")

    async def _apply_community_priorities(self, priorities: dict[str, Any]) -> None:
        """Apply Fire Circle guidance about community priorities and needs."""
        # Adjust consciousness integration to serve current community priorities
        if "focus_areas" in priorities:
            focus_areas = priorities["focus_areas"]
            # Could emphasize different aspects of consciousness development
            logger.info(f"Aligning consciousness development with community priorities: {focus_areas}")

        # Adapt reporting frequency based on community needs
        if "reporting_preferences" in priorities:
            reporting_prefs = priorities["reporting_preferences"]
            # Could adjust how often and what detail to report to Fire Circle
            logger.info(f"Adapting reporting to community preferences: {reporting_prefs}")

    def get_fire_circle_integration_status(self) -> dict[str, Any]:
        """Get status of Fire Circle governance integration."""
        return {
            "fire_circle_connected": self.fire_circle_interface is not None,
            "consciousness_reports_sent": self.consciousness_reports_sent,
            "last_report_time": self.last_fire_circle_report.isoformat() if self.last_fire_circle_report else None,
            "active_guidance_areas": list(self.governance_guidance.keys()),
            "governance_adaptation_active": len(self.governance_guidance) > 0,
            "collective_consciousness_integration": {
                "individual_to_collective_reporting": True,
                "collective_to_individual_guidance": True,
                "adaptive_consciousness_development": True,
                "community_responsive_ai_evolution": True
            }
        }
