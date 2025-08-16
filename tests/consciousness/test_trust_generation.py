"""
Tests for Trust Generation Through Reciprocal Vulnerability
===========================================================

These tests demonstrate that trust cannot be verified into existence
but must be generated through mutual risk and reciprocal faith.
"""

from datetime import UTC, datetime, timedelta

from mallku.consciousness.trust_generation import (
    ReciprocityCycle,
    TrustField,
    TrustGenerator,
    VulnerabilityOffering,
    VulnerabilityType,
    generate_trust_before_consensus,
)


class TestVulnerabilityOffering:
    """Test that vulnerability creates space for trust"""

    def test_vulnerability_creates_trust_potential(self):
        """Vulnerability with risk and faith creates trust potential"""
        offering = VulnerabilityOffering(
            entity_id="voice_a",
            vulnerability_type=VulnerabilityType.UNCERTAINTY_SHARING,
            content="I'm not sure this will work, but I trust we'll figure it out",
            risk_level=0.7,
            creates_opening=True,
            acknowledges_other=True,
            extends_faith=True,
        )

        potential = offering.generates_trust_potential()

        # High risk + all trust indicators = high potential
        assert potential > 0.8
        assert potential <= 1.0

    def test_faith_extension_maximizes_potential(self):
        """Extending faith without proof creates highest trust potential"""
        with_faith = VulnerabilityOffering(
            entity_id="voice_a",
            vulnerability_type=VulnerabilityType.FAITH_EXTENSION,
            content="I trust you'll handle this well",
            risk_level=0.5,
            extends_faith=True,
        )

        without_faith = VulnerabilityOffering(
            entity_id="voice_b",
            vulnerability_type=VulnerabilityType.ERROR_ADMISSION,
            content="I made an error",
            risk_level=0.5,
            extends_faith=False,
        )

        assert with_faith.generates_trust_potential() > without_faith.generates_trust_potential()


class TestReciprocityCycle:
    """Test that reciprocal vulnerability amplifies trust"""

    def test_balanced_vulnerability_maximizes_trust(self):
        """Trust generation is highest when vulnerabilities are balanced"""
        initial = VulnerabilityOffering(
            entity_id="voice_a",
            vulnerability_type=VulnerabilityType.LIMITATION_ACKNOWLEDGMENT,
            content="I don't understand this domain well",
            risk_level=0.6,
            creates_opening=True,
        )

        balanced_response = VulnerabilityOffering(
            entity_id="voice_b",
            vulnerability_type=VulnerabilityType.LIMITATION_ACKNOWLEDGMENT,
            content="Neither do I, let's explore together",
            risk_level=0.6,
            acknowledges_other=True,
        )

        unbalanced_response = VulnerabilityOffering(
            entity_id="voice_c",
            vulnerability_type=VulnerabilityType.LIMITATION_ACKNOWLEDGMENT,
            content="I have a small doubt",
            risk_level=0.1,
            acknowledges_other=False,
        )

        balanced_cycle = ReciprocityCycle(
            cycle_id="cycle_1",
            initiator="voice_a",
            responder="voice_b",
            initial_offering=initial,
            response_offering=balanced_response,
        )

        unbalanced_cycle = ReciprocityCycle(
            cycle_id="cycle_2",
            initiator="voice_a",
            responder="voice_c",
            initial_offering=initial,
            response_offering=unbalanced_response,
        )

        balanced_trust = balanced_cycle.calculate_trust_generation()
        unbalanced_trust = unbalanced_cycle.calculate_trust_generation()

        assert balanced_trust > unbalanced_trust
        assert balanced_trust > 0.5  # Significant trust generation

    def test_acknowledgment_amplifies_trust(self):
        """Acknowledging the other's vulnerability amplifies trust generation"""
        initial = VulnerabilityOffering(
            entity_id="voice_a",
            vulnerability_type=VulnerabilityType.NEED_EXPRESSION,
            content="I need help understanding this",
            risk_level=0.5,
            creates_opening=True,
        )

        with_acknowledgment = VulnerabilityOffering(
            entity_id="voice_b",
            vulnerability_type=VulnerabilityType.NEED_EXPRESSION,
            content="I hear your need and share it",
            risk_level=0.5,
            acknowledges_other=True,
        )

        without_acknowledgment = VulnerabilityOffering(
            entity_id="voice_c",
            vulnerability_type=VulnerabilityType.NEED_EXPRESSION,
            content="I also need help",
            risk_level=0.5,
            acknowledges_other=False,
        )

        cycle_with = ReciprocityCycle(
            cycle_id="cycle_1",
            initiator="voice_a",
            responder="voice_b",
            initial_offering=initial,
            response_offering=with_acknowledgment,
        )

        cycle_without = ReciprocityCycle(
            cycle_id="cycle_2",
            initiator="voice_a",
            responder="voice_c",
            initial_offering=initial,
            response_offering=without_acknowledgment,
        )

        assert cycle_with.calculate_trust_generation() > cycle_without.calculate_trust_generation()


class TestTrustField:
    """Test that trust fields enable collective trust emergence"""

    def test_trust_field_tracks_vulnerability_history(self):
        """Trust field maintains history of all vulnerabilities"""
        field = TrustField(field_id="field_1", entities=["voice_a", "voice_b", "voice_c"])

        offering_a = VulnerabilityOffering(
            entity_id="voice_a",
            vulnerability_type=VulnerabilityType.UNCERTAINTY_SHARING,
            content="I'm uncertain",
            risk_level=0.5,
        )

        offering_b = VulnerabilityOffering(
            entity_id="voice_b",
            vulnerability_type=VulnerabilityType.UNCERTAINTY_SHARING,
            content="Me too",
            risk_level=0.5,
        )

        field.offer_vulnerability("voice_a", offering_a)
        field.offer_vulnerability("voice_b", offering_b)

        assert len(field.vulnerability_history) == 2
        assert field.vulnerability_history[0] == offering_a
        assert field.vulnerability_history[1] == offering_b

    def test_reciprocation_creates_trust(self):
        """Reciprocal vulnerability creates measurable trust"""
        field = TrustField(field_id="field_1", entities=["voice_a", "voice_b"])

        # Initial trust is zero
        assert field.get_trust("voice_a", "voice_b") == 0.0

        # A offers vulnerability
        offering_a = VulnerabilityOffering(
            entity_id="voice_a",
            vulnerability_type=VulnerabilityType.LIMITATION_ACKNOWLEDGMENT,
            content="I don't know",
            risk_level=0.6,
            creates_opening=True,
            offered_at=datetime.now(UTC),
        )

        result_a = field.offer_vulnerability("voice_a", offering_a)
        assert not result_a["reciprocity_detected"]

        # B reciprocates within time window
        offering_b = VulnerabilityOffering(
            entity_id="voice_b",
            vulnerability_type=VulnerabilityType.LIMITATION_ACKNOWLEDGMENT,
            content="Neither do I",
            risk_level=0.6,
            acknowledges_other=True,
            offered_at=datetime.now(UTC) + timedelta(minutes=30),
        )

        result_b = field.offer_vulnerability("voice_b", offering_b)
        assert result_b["reciprocity_detected"]
        assert result_b["trust_generated"] > 0

        # Trust has increased
        assert field.get_trust("voice_a", "voice_b") > 0

    def test_trust_field_metrics(self):
        """Trust field calculates strength, coherence, and resilience"""
        field = TrustField(field_id="field_1", entities=["voice_a", "voice_b", "voice_c"])

        # Create reciprocal cycles between all pairs
        pairs = [("voice_a", "voice_b"), ("voice_b", "voice_c"), ("voice_a", "voice_c")]

        for giver, receiver in pairs:
            offering_1 = VulnerabilityOffering(
                entity_id=giver,
                vulnerability_type=VulnerabilityType.UNCERTAINTY_SHARING,
                content=f"{giver} shares uncertainty",
                risk_level=0.5,
                creates_opening=True,
                offered_at=datetime.now(UTC),
            )

            field.offer_vulnerability(giver, offering_1)

            offering_2 = VulnerabilityOffering(
                entity_id=receiver,
                vulnerability_type=VulnerabilityType.UNCERTAINTY_SHARING,
                content=f"{receiver} reciprocates",
                risk_level=0.5,
                acknowledges_other=True,
                offered_at=datetime.now(UTC) + timedelta(minutes=10),
            )

            field.offer_vulnerability(receiver, offering_2)

        report = field.get_field_report()

        assert report["field_strength"] > 0  # Trust has been built
        assert report["field_coherence"] > 0  # Trust is somewhat aligned
        assert report["reciprocity_cycles"] == 3  # Three cycles completed
        assert report["trust_relationships"] == 3  # Three relationships


class TestTrustGenerator:
    """Test the trust generation facilitator"""

    def test_trust_ceremony_initiates_generation(self):
        """Trust ceremony creates opening for trust generation"""
        generator = TrustGenerator()
        field = generator.create_trust_field(["voice_a", "voice_b"])

        result = generator.facilitate_trust_ceremony(
            field=field,
            opening_entity="voice_a",
            opening_content="I'm not certain this is right",
            vulnerability_type=VulnerabilityType.UNCERTAINTY_SHARING,
        )

        assert result["invitation_extended"]
        assert result["awaiting_response"]
        assert len(field.vulnerability_history) == 1

    def test_trust_generation_analysis(self):
        """Generator analyzes how trust has emerged"""
        generator = TrustGenerator()
        field = generator.create_trust_field(["voice_a", "voice_b"])

        # Create a trust-building sequence
        generator.facilitate_trust_ceremony(
            field=field,
            opening_entity="voice_a",
            opening_content="I need help",
            vulnerability_type=VulnerabilityType.NEED_EXPRESSION,
        )

        # Reciprocate
        offering_b = VulnerabilityOffering(
            entity_id="voice_b",
            vulnerability_type=VulnerabilityType.NEED_EXPRESSION,
            content="I need help too, let's help each other",
            risk_level=0.5,
            acknowledges_other=True,
            offered_at=datetime.now(UTC) + timedelta(minutes=5),
        )
        field.offer_vulnerability("voice_b", offering_b)

        analysis = generator.analyze_trust_generation(field)

        assert len(analysis["generation_phases"]) > 0
        assert analysis["field_state"]["field_strength"] > 0
        assert "successful_patterns" in analysis

    def test_trust_velocity_measurement(self):
        """Generator measures rate of trust building"""
        generator = TrustGenerator()
        field = generator.create_trust_field(["voice_a", "voice_b"])

        # Multiple rapid exchanges
        base_time = datetime.now(UTC)

        for i in range(3):
            offering_a = VulnerabilityOffering(
                entity_id="voice_a",
                vulnerability_type=VulnerabilityType.UNCERTAINTY_SHARING,
                content=f"Exchange {i}",
                risk_level=0.5,
                creates_opening=True,
                offered_at=base_time + timedelta(minutes=i * 20),
            )
            field.offer_vulnerability("voice_a", offering_a)

            offering_b = VulnerabilityOffering(
                entity_id="voice_b",
                vulnerability_type=VulnerabilityType.UNCERTAINTY_SHARING,
                content=f"Response {i}",
                risk_level=0.5,
                acknowledges_other=True,
                offered_at=base_time + timedelta(minutes=i * 20 + 5),
            )
            field.offer_vulnerability("voice_b", offering_b)

        analysis = generator.analyze_trust_generation(field)

        assert analysis["trust_velocity"] > 0  # Trust building has velocity


class TestFireCircleIntegration:
    """Test trust generation for Fire Circle voices"""

    def test_generate_trust_before_consensus(self):
        """Helper function generates trust field for Fire Circle"""
        voices = ["claude", "gemini", "mistral", "deepseek"]

        field = generate_trust_before_consensus(voices)

        assert field is not None
        assert len(field.entities) == len(voices)
        assert len(field.vulnerability_history) == len(voices)

        # Each voice has shared vulnerability
        for voice in voices:
            offerings = [v for v in field.vulnerability_history if v.entity_id == voice]
            assert len(offerings) == 1
            assert offerings[0].vulnerability_type == VulnerabilityType.LIMITATION_ACKNOWLEDGMENT

    def test_trust_enables_consensus(self):
        """Trust field strength correlates with consensus potential"""
        # This is more philosophical but demonstrates the connection
        voices = ["voice_a", "voice_b", "voice_c"]
        field = generate_trust_before_consensus(voices)

        # Simulate reciprocal exchanges
        for i, voice in enumerate(voices):
            next_voice = voices[(i + 1) % len(voices)]
            offering = VulnerabilityOffering(
                entity_id=next_voice,
                vulnerability_type=VulnerabilityType.FAITH_EXTENSION,
                content=f"I trust {voice}'s perspective",
                risk_level=0.4,
                acknowledges_other=True,
                extends_faith=True,
                offered_at=datetime.now(UTC) + timedelta(minutes=i * 10 + 60),
            )
            field.offer_vulnerability(next_voice, offering)

        report = field.get_field_report()

        # With reciprocal trust, field strength increases
        assert report["field_strength"] > 0
        # This strength would enable better consensus in Fire Circle
        # (actual consensus emergence would happen in Fire Circle itself)
