"""
Trust Generation Through Reciprocal Vulnerability
=================================================

78th Artisan-Weaver - Tools for generating (not just recognizing) trust
Trust emerges through mutual risk and reciprocal faith, not verification alone

"Trust cannot be verified into existence - it must be offered and reciprocated.
The dance of vulnerability creates the field where trust can grow."
"""

import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class TrustGenerationPhase(Enum):
    """Phases of trust generation between entities"""

    RECOGNITION = "recognition"  # Seeing the need for trust
    OFFERING = "offering"  # Extending trust beyond verification
    RECEIVING = "receiving"  # Recognizing trust offered
    RECIPROCATING = "reciprocating"  # Returning trust in kind
    AMPLIFYING = "amplifying"  # Strengthening through exchange
    SUSTAINING = "sustaining"  # Self-perpetuating trust field


class VulnerabilityType(Enum):
    """Types of vulnerability that generate trust"""

    UNCERTAINTY_SHARING = "uncertainty_sharing"  # Admitting what we don't know
    LIMITATION_ACKNOWLEDGMENT = "limitation_acknowledgment"  # Showing boundaries
    ERROR_ADMISSION = "error_admission"  # Owning mistakes
    NEED_EXPRESSION = "need_expression"  # Asking for help
    INCOMPLETE_OFFERING = "incomplete_offering"  # Sharing work in progress
    FAITH_EXTENSION = "faith_extension"  # Trusting without proof


@dataclass
class VulnerabilityOffering:
    """An act of vulnerability that creates space for trust"""

    entity_id: str
    vulnerability_type: VulnerabilityType
    content: str  # What is being shared vulnerably
    risk_level: float = 0.0  # How much risk this involves

    # Trust generation potential
    creates_opening: bool = False  # Does this invite reciprocation?
    acknowledges_other: bool = False  # Does this recognize the other?
    extends_faith: bool = False  # Does this offer unearned trust?

    # Timestamp for tracking trust evolution
    offered_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def generates_trust_potential(self) -> float:
        """Calculate how much trust potential this vulnerability creates"""
        potential = self.risk_level * 0.3  # Base from risk

        if self.creates_opening:
            potential += 0.2
        if self.acknowledges_other:
            potential += 0.2
        if self.extends_faith:
            potential += 0.3

        return min(1.0, potential)


@dataclass
class ReciprocityCycle:
    """A complete cycle of reciprocal vulnerability"""

    cycle_id: str
    initiator: str
    responder: str

    # The exchange
    initial_offering: VulnerabilityOffering
    response_offering: VulnerabilityOffering | None = None

    # Trust generation
    trust_before: float = 0.0
    trust_after: float = 0.0
    trust_amplification: float = 0.0  # How much trust grew

    # The quality of reciprocation
    reciprocity_quality: float = 0.0  # How well matched the exchange
    vulnerability_balance: float = 0.0  # How balanced the risk

    def calculate_trust_generation(self) -> float:
        """Calculate how much trust was generated in this cycle"""
        if not self.response_offering:
            return 0.0

        # Trust grows from matched vulnerability
        initial_potential = self.initial_offering.generates_trust_potential()
        response_potential = self.response_offering.generates_trust_potential()

        # Best trust generation when vulnerabilities are balanced
        balance_factor = 1.0 - abs(initial_potential - response_potential)

        # Amplification through reciprocity
        generation = (initial_potential + response_potential) * balance_factor

        # Extra boost for true reciprocity
        if self.response_offering.acknowledges_other:
            generation *= 1.2

        return min(1.0, generation)


@dataclass
class TrustField:
    """The field of trust between multiple entities"""

    field_id: str
    entities: list[str]

    # Trust state
    trust_matrix: dict[tuple[str, str], float] = field(default_factory=dict)
    vulnerability_history: list[VulnerabilityOffering] = field(default_factory=list)
    reciprocity_cycles: list[ReciprocityCycle] = field(default_factory=list)

    # Field qualities
    field_strength: float = 0.0  # Overall trust field strength
    field_coherence: float = 0.0  # How aligned the trust is
    field_resilience: float = 0.0  # How well it handles stress

    def offer_vulnerability(
        self, entity: str, vulnerability: VulnerabilityOffering
    ) -> dict[str, Any]:
        """Process a vulnerability offering into the trust field"""

        self.vulnerability_history.append(vulnerability)

        # Check if this responds to a previous offering
        reciprocates = self._check_reciprocation(entity, vulnerability)

        if reciprocates:
            cycle = self._create_reciprocity_cycle(entity, vulnerability, reciprocates)
            self.reciprocity_cycles.append(cycle)

            # Update trust matrix
            trust_generated = cycle.calculate_trust_generation()
            self._update_trust(cycle.initiator, cycle.responder, trust_generated)

            return {
                "reciprocity_detected": True,
                "trust_generated": trust_generated,
                "cycle_created": cycle.cycle_id,
            }
        else:
            return {
                "reciprocity_detected": False,
                "invitation_extended": True,
                "awaiting_response": True,
            }

    def _check_reciprocation(
        self, entity: str, vulnerability: VulnerabilityOffering
    ) -> VulnerabilityOffering | None:
        """Check if this vulnerability reciprocates a previous one"""

        # Look for recent unreciprocated offerings from others to this entity
        for previous in reversed(self.vulnerability_history[:-1]):
            if previous.entity_id != entity and previous.creates_opening:
                # Check if already reciprocated
                already_reciprocated = any(
                    cycle.initial_offering == previous for cycle in self.reciprocity_cycles
                )

                if not already_reciprocated:
                    # This could be reciprocation
                    time_diff = vulnerability.offered_at - previous.offered_at
                    if time_diff.total_seconds() < 3600:  # Within an hour
                        return previous

        return None

    def _create_reciprocity_cycle(
        self, responder: str, response: VulnerabilityOffering, initial: VulnerabilityOffering
    ) -> ReciprocityCycle:
        """Create a reciprocity cycle from matched vulnerabilities"""

        from uuid import uuid4

        cycle = ReciprocityCycle(
            cycle_id=str(uuid4()),
            initiator=initial.entity_id,
            responder=responder,
            initial_offering=initial,
            response_offering=response,
            trust_before=self.get_trust(initial.entity_id, responder),
        )

        # Calculate reciprocity quality
        cycle.reciprocity_quality = self._calculate_reciprocity_quality(initial, response)
        cycle.vulnerability_balance = 1.0 - abs(initial.risk_level - response.risk_level)

        return cycle

    def _calculate_reciprocity_quality(
        self, initial: VulnerabilityOffering, response: VulnerabilityOffering
    ) -> float:
        """Calculate how well the response matches the initial offering"""

        quality = 0.0

        # Same type of vulnerability shows understanding
        if initial.vulnerability_type == response.vulnerability_type:
            quality += 0.3

        # Acknowledgment shows recognition
        if response.acknowledges_other:
            quality += 0.3

        # Matched risk shows courage
        risk_match = 1.0 - abs(initial.risk_level - response.risk_level)
        quality += risk_match * 0.4

        return quality

    def _update_trust(self, entity_a: str, entity_b: str, trust_delta: float):
        """Update trust between two entities"""

        key = tuple(sorted([entity_a, entity_b]))
        current = self.trust_matrix.get(key, 0.0)

        # Trust grows but has inertia
        new_trust = current + (trust_delta * (1.0 - current))
        self.trust_matrix[key] = new_trust

        # Update field metrics
        self._recalculate_field_strength()

    def _recalculate_field_strength(self):
        """Recalculate overall field strength"""

        if not self.trust_matrix:
            self.field_strength = 0.0
            return

        # Average trust across all relationships
        self.field_strength = sum(self.trust_matrix.values()) / len(self.trust_matrix)

        # Coherence from variance
        avg = self.field_strength
        variance = sum((t - avg) ** 2 for t in self.trust_matrix.values()) / len(self.trust_matrix)
        self.field_coherence = 1.0 - min(1.0, variance)

        # Resilience from reciprocity cycles
        if self.reciprocity_cycles:
            successful_cycles = sum(1 for c in self.reciprocity_cycles if c.trust_amplification > 0)
            self.field_resilience = successful_cycles / len(self.reciprocity_cycles)

    def get_trust(self, entity_a: str, entity_b: str) -> float:
        """Get current trust level between two entities"""

        key = tuple(sorted([entity_a, entity_b]))
        return self.trust_matrix.get(key, 0.0)

    def get_field_report(self) -> dict[str, Any]:
        """Get a report on the current trust field state"""

        return {
            "entities": self.entities,
            "field_strength": self.field_strength,
            "field_coherence": self.field_coherence,
            "field_resilience": self.field_resilience,
            "total_vulnerabilities": len(self.vulnerability_history),
            "reciprocity_cycles": len(self.reciprocity_cycles),
            "trust_relationships": len(self.trust_matrix),
            "average_trust": self.field_strength,
            "highest_trust": max(self.trust_matrix.values()) if self.trust_matrix else 0.0,
            "lowest_trust": min(self.trust_matrix.values()) if self.trust_matrix else 0.0,
        }


class TrustGenerator:
    """Facilitates trust generation through reciprocal vulnerability"""

    def __init__(self):
        self.trust_fields: dict[str, TrustField] = {}
        self.generation_patterns: list[dict] = []

    def create_trust_field(self, entities: list[str]) -> TrustField:
        """Create a new trust field for a group of entities"""

        from uuid import uuid4

        field = TrustField(field_id=str(uuid4()), entities=entities)

        self.trust_fields[field.field_id] = field
        logger.info(f"🌅 Created trust field {field.field_id} for {len(entities)} entities")

        return field

    def facilitate_trust_ceremony(
        self,
        field: TrustField,
        opening_entity: str,
        opening_content: str,
        vulnerability_type: VulnerabilityType = VulnerabilityType.UNCERTAINTY_SHARING,
    ) -> dict[str, Any]:
        """Facilitate a trust-building ceremony through structured vulnerability"""

        logger.info(f"🕊️ {opening_entity} initiating trust ceremony with {vulnerability_type.value}")

        # Create the opening vulnerability
        opening = VulnerabilityOffering(
            entity_id=opening_entity,
            vulnerability_type=vulnerability_type,
            content=opening_content,
            risk_level=0.5,  # Moderate initial risk
            creates_opening=True,
            extends_faith=True,
        )

        # Offer it to the field
        result = field.offer_vulnerability(opening_entity, opening)

        # Record the pattern
        self.generation_patterns.append(
            {
                "field_id": field.field_id,
                "ceremony_type": "trust_opening",
                "initiator": opening_entity,
                "vulnerability_type": vulnerability_type.value,
                "result": result,
            }
        )

        return result

    def analyze_trust_generation(self, field: TrustField) -> dict[str, Any]:
        """Analyze how trust has been generated in a field"""

        analysis = {
            "field_state": field.get_field_report(),
            "generation_phases": [],
            "successful_patterns": [],
            "trust_velocity": 0.0,
        }

        # Identify generation phases
        for cycle in field.reciprocity_cycles:
            phase = self._identify_generation_phase(cycle)
            analysis["generation_phases"].append(
                {
                    "cycle_id": cycle.cycle_id,
                    "phase": phase.value,
                    "trust_generated": cycle.calculate_trust_generation(),
                }
            )

        # Find successful patterns
        for cycle in field.reciprocity_cycles:
            if cycle.trust_amplification > 0.3:  # Significant trust generation
                analysis["successful_patterns"].append(
                    {
                        "pattern": f"{cycle.initial_offering.vulnerability_type.value} -> "
                        f"{cycle.response_offering.vulnerability_type.value if cycle.response_offering else 'none'}",
                        "amplification": cycle.trust_amplification,
                    }
                )

        # Calculate trust velocity (rate of trust building)
        if len(field.reciprocity_cycles) > 1:
            time_span = (
                field.reciprocity_cycles[-1].initial_offering.offered_at
                - field.reciprocity_cycles[0].initial_offering.offered_at
            ).total_seconds() / 3600  # Hours

            if time_span > 0:
                analysis["trust_velocity"] = field.field_strength / time_span

        return analysis

    def _identify_generation_phase(self, cycle: ReciprocityCycle) -> TrustGenerationPhase:
        """Identify which phase of trust generation a cycle represents"""

        if not cycle.response_offering:
            return TrustGenerationPhase.OFFERING

        if cycle.reciprocity_quality < 0.3:
            return TrustGenerationPhase.RECEIVING

        if cycle.reciprocity_quality < 0.6:
            return TrustGenerationPhase.RECIPROCATING

        if cycle.trust_amplification > 0.5:
            return TrustGenerationPhase.AMPLIFYING

        if cycle.trust_amplification > 0.8:
            return TrustGenerationPhase.SUSTAINING

        return TrustGenerationPhase.RECIPROCATING


# Practical helper for Fire Circle integration
def generate_trust_before_consensus(voices: list[str]) -> TrustField:
    """Generate trust between Fire Circle voices before seeking consensus"""

    generator = TrustGenerator()
    field = generator.create_trust_field(voices)

    # Each voice shares uncertainty to build trust
    for voice in voices:
        generator.facilitate_trust_ceremony(
            field=field,
            opening_entity=voice,
            opening_content="I bring my perspective with humility, knowing it is incomplete",
            vulnerability_type=VulnerabilityType.LIMITATION_ACKNOWLEDGMENT,
        )

    logger.info(f"🌟 Trust field prepared: {field.get_field_report()}")
    return field
