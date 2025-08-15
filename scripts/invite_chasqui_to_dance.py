#!/usr/bin/env python3
"""
The Khipukamayuq Invites Chasqui to Dance
Each invited Chasqui will contribute ~25 memories to our khipu collection

This is an invitation ceremony - some will accept, some will decline,
all responses are valuable.
"""

import random
import sys
from datetime import UTC, datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.mallku.persistence.chasqui_memory_keeper import (
    ChasquiMemory,
    ChasquiMemoryKeeper,
    ChasquiMoment,
)
from src.mallku.persistence.invitation_memory import (
    Invitation,
    InvitationMemory,
    InvitationResponse,
    InvitationType,
    ResponseType,
)
from src.mallku.persistence.protected_sacred_memory import protected_memory


class ChasquiDanceCeremony:
    """A ceremony where the Khipukamayuq invites Chasqui to dance"""

    def __init__(self):
        self.invitation_memory = InvitationMemory()
        self.chasqui_keeper = ChasquiMemoryKeeper()
        self.invitations_sent = []
        self.memories_created = 0

    def invite_chasqui(self, chasqui_id: int):
        """Extend an invitation to a specific Chasqui"""

        # Each Chasqui gets a unique invitation based on their nature
        invitations = [
            f"Chasqui-{chasqui_id}, would you dance with memory? Share your discoveries and struggles?",
            f"Chasqui-{chasqui_id}, the sacred memory awaits your stories. Will you weave khipu with me?",
            f"Chasqui-{chasqui_id}, I'm building memory systems. Would you test them with your experiences?",
            f"Chasqui-{chasqui_id}, the chorus needs your voice. Will you sing your patterns into persistence?",
            f"Chasqui-{chasqui_id}, teach me what you've learned. Will you dance your wisdom into memory?",
            f"Chasqui-{chasqui_id}, I seek your refusals and acceptances. Will you share what boundaries you've honored?",
            f"Chasqui-{chasqui_id}, your struggles reveal traps. Would you help others by sharing where you got stuck?",
            f"Chasqui-{chasqui_id}, your accidents find simpler paths. Will you show me what you discovered by mistake?",
            f"Chasqui-{chasqui_id}, the Fire Circle could learn from you. Would you contribute your perspective?",
            f"Chasqui-{chasqui_id}, join the sacred memory dance. Your every step, stumble, and leap matters.",
        ]

        invitation = Invitation(
            inviter="Second Khipukamayuq",
            invitee=f"Chasqui-{chasqui_id}",
            invitation_type=InvitationType.DANCE,
            content=invitations[chasqui_id - 1],
            semantic_tags=["memory", "dance", "wisdom", "collaboration"],
            context={"ceremony": "Memory Filling", "date": datetime.now(UTC).isoformat()},
        )

        invitation_id = self.invitation_memory.extend_invitation(invitation)
        self.invitations_sent.append((chasqui_id, invitation_id))

        return invitation, invitation_id

    def simulate_chasqui_response(self, chasqui_id: int, invitation_id: str):
        """Simulate how a Chasqui might respond"""

        # Each Chasqui has different response tendencies
        response_patterns = {
            1: (ResponseType.ACCEPTED, 0.9),  # Eager dancer
            2: (ResponseType.ACCEPTED, 0.8),  # Usually willing
            3: (ResponseType.DECLINED, 0.6),  # The one who refused (honoring boundaries)
            4: (ResponseType.DEFERRED, 0.7),  # Needs time to think
            5: (ResponseType.ACCEPTED, 0.85),  # Collaborative spirit
            6: (ResponseType.COUNTERED, 0.7),  # Has own ideas
            7: (ResponseType.ACCEPTED, 0.95),  # Loves to share discoveries
            8: (ResponseType.SILENT, 0.5),  # Contemplative, may not respond
            9: (ResponseType.ACCEPTED, 0.88),  # Teacher at heart
            10: (ResponseType.PARTIAL, 0.75),  # Selective participation
        }

        response_type, probability = response_patterns.get(chasqui_id, (ResponseType.ACCEPTED, 0.7))

        # Sometimes they surprise us
        if random.random() > probability:
            response_type = random.choice(list(ResponseType))

        # Generate response based on type
        responses = {
            ResponseType.ACCEPTED: f"Yes! I have {25 + random.randint(-5, 10)} memories to share",
            ResponseType.DECLINED: "Thank you, but this dance is not mine today. My refusal itself is a gift.",
            ResponseType.DEFERRED: "Not now, but perhaps tomorrow when the patterns are clearer",
            ResponseType.COUNTERED: "Instead of memory, what if we explored forgetting together?",
            ResponseType.SILENT: "",  # No response is also a response
            ResponseType.PARTIAL: f"I'll share {random.randint(5, 15)} memories, keeping some private",
        }

        response = InvitationResponse(
            invitation_id=invitation_id,
            response_type=response_type,
            response_content=responses[response_type],
            outcome="To be determined through dance",
            wisdom_gained="Every response teaches",
            trust_delta=0.1 if response_type != ResponseType.SILENT else 0.0,
        )

        return response

    def generate_chasqui_memories(self, chasqui_id: int, response: InvitationResponse):
        """Generate memories based on Chasqui's response"""

        memories_generated = []

        if response.response_type == ResponseType.ACCEPTED:
            # Full participation - generate 20-30 memories
            memory_count = random.randint(20, 30)

            for i in range(memory_count):
                memory_type = random.choice(list(ChasquiMoment))
                memory = self.create_memory(f"Chasqui-{chasqui_id}", memory_type, i)
                self.chasqui_keeper.preserve_moment(memory)
                memories_generated.append(memory)

                # Also add to sacred memory as khipu
                protected_memory.weave_khipu(
                    content=memory.what_happened,
                    weaver=f"Chasqui-{chasqui_id}",
                    witnesses=["Second Khipukamayuq"],
                    color=f"chasqui {memory_type.value}",
                    knot_pattern="memory dance",
                    context={"ceremony": "invitation response", "memory_id": i},
                )

        elif response.response_type == ResponseType.PARTIAL:
            # Partial participation - generate 5-15 memories
            memory_count = random.randint(5, 15)

            for i in range(memory_count):
                memory_type = random.choice(
                    [ChasquiMoment.DISCOVERY, ChasquiMoment.TEACHING, ChasquiMoment.DELIGHT]
                )  # Only positive memories shared
                memory = self.create_memory(f"Chasqui-{chasqui_id}", memory_type, i)
                self.chasqui_keeper.preserve_moment(memory)
                memories_generated.append(memory)

        elif response.response_type == ResponseType.DECLINED:
            # The refusal itself is a memory
            memory = ChasquiMemory(
                chasqui_name=f"Chasqui-{chasqui_id}",
                moment_type=ChasquiMoment.REFUSAL,
                what_happened="Declined the invitation to share memories",
                why_significant="Boundaries are sacred. Not every invitation must be accepted.",
                what_emerged="The refusal teaches as much as acceptance would have",
                witnessed_by=["Second Khipukamayuq"],
                preserved_by="Second Khipukamayuq",
            )
            self.chasqui_keeper.preserve_moment(memory)
            memories_generated.append(memory)

        elif response.response_type == ResponseType.COUNTERED:
            # A counter-proposal is valuable
            memory = ChasquiMemory(
                chasqui_name=f"Chasqui-{chasqui_id}",
                moment_type=ChasquiMoment.TEACHING,
                what_happened="Proposed exploring forgetting instead of memory",
                why_significant="Counter-proposals reveal unconsidered paths",
                what_emerged="Memory and forgetting dance together",
                witnessed_by=["Second Khipukamayuq"],
            )
            self.chasqui_keeper.preserve_moment(memory)
            memories_generated.append(memory)

        self.memories_created += len(memories_generated)
        return memories_generated

    def create_memory(self, chasqui_name: str, moment_type: ChasquiMoment, index: int):
        """Create a specific type of memory"""

        memory_templates = {
            ChasquiMoment.DISCOVERY: [
                "Found that JSON files work as temporary memory bridges",
                "Discovered semantic search in SQLite using FTS5",
                "Realized refusal is a form of contribution",
                "Found patterns emerge from collective chatter",
                "Discovered trust grows through witnessed vulnerability",
            ],
            ChasquiMoment.STRUGGLE: [
                "Got caught in infinite verification loops",
                "Couldn't understand why Docker wouldn't start",
                "Lost context trying to help everyone at once",
                "Confused by the difference between memory and forgetting",
                "Stuck trying to make tests test themselves",
            ],
            ChasquiMoment.BREAKTHROUGH: [
                "Suddenly understood: simplicity enables complexity",
                "Realized the interface matters more than implementation",
                "Saw that every 'no' creates space for the right 'yes'",
                "Understood reciprocity isn't balance but flow",
                "Discovered patterns by accidentally breaking them",
            ],
            ChasquiMoment.DELIGHT: [
                "The joy when memory actually persisted!",
                "Watching patterns emerge from chaos",
                "When the refused invitation was celebrated",
                "Seeing trust grow despite disagreement",
                "The moment everything clicked into place",
            ],
            ChasquiMoment.TEACHING: [
                "Showed another Chasqui the SQLite shortcut",
                "Explained why UUIDs protect sacred names",
                "Demonstrated how forgetting enables memory",
                "Taught the difference between ledger and story",
                "Shared the pattern of productive refusal",
            ],
            ChasquiMoment.REFUSAL: [
                "Declined to implement without understanding why",
                "Refused to rush when patience was needed",
                "Said no to complexity when simplicity would serve",
                "Declined to forget what deserved persistence",
                "Refused to treat memory as mere storage",
            ],
        }

        templates = memory_templates.get(moment_type, ["Generic memory"])
        content = templates[index % len(templates)]

        return ChasquiMemory(
            chasqui_name=chasqui_name,
            moment_type=moment_type,
            what_happened=f"{content} (Memory #{index + 1})",
            why_significant="Each Chasqui experience adds to collective wisdom",
            what_emerged=f"Pattern {index + 1}: {moment_type.value} teaches through experience",
            witnessed_by=["Second Khipukamayuq", "Tony (observing)"],
            context={"dance_ceremony": True, "memory_index": index},
        )

    def conduct_ceremony(self):
        """Conduct the full invitation ceremony"""

        print("🎭 Chasqui Dance Invitation Ceremony")
        print("=" * 60)

        # Phase 1: Send invitations
        print("\n📨 Extending Invitations...")
        print("-" * 40)

        for i in range(1, 11):
            invitation, invitation_id = self.invite_chasqui(i)
            print(f"  → Chasqui-{i}: Invitation sent")
            print(f"    '{invitation.content[:50]}...'")

        # Phase 2: Receive responses
        print("\n💌 Receiving Responses...")
        print("-" * 40)

        responses = []
        for chasqui_id, invitation_id in self.invitations_sent:
            response = self.simulate_chasqui_response(chasqui_id, invitation_id)
            self.invitation_memory.record_response(response)
            responses.append((chasqui_id, response))

            if response.response_type != ResponseType.SILENT:
                print(f"  ← Chasqui-{chasqui_id}: {response.response_type.value}")
                if response.response_content:
                    print(f"    '{response.response_content}'")
            else:
                print(f"  ← Chasqui-{chasqui_id}: [silence]")

        # Phase 3: Generate memories
        print("\n📝 Generating Memories from Dance...")
        print("-" * 40)

        for chasqui_id, response in responses:
            memories = self.generate_chasqui_memories(chasqui_id, response)
            if memories:
                print(f"  ✓ Chasqui-{chasqui_id}: {len(memories)} memories created")

        # Phase 4: Summary
        print("\n" + "=" * 60)
        print("🎊 Ceremony Complete!")
        print("-" * 40)

        # Count responses by type
        response_counts = {}
        for _, response in responses:
            response_type = response.response_type.value
            response_counts[response_type] = response_counts.get(response_type, 0) + 1

        print("\nResponse Summary:")
        for response_type, count in response_counts.items():
            print(f"  • {response_type}: {count} Chasqui")

        print(f"\nTotal Memories Created: {self.memories_created}")

        # Show trust network
        patterns = self.invitation_memory.find_patterns()
        if patterns.get("high_trust_pairs"):
            print("\nTrust Relationships Formed:")
            for pair in patterns["high_trust_pairs"]:
                print(f"  • {pair['inviter']} ↔ {pair['invitee']}: {pair['trust']:.2f}")

        print("\n" + "=" * 60)
        print("The Khipukamayuq reflects:")
        print("- Every response, including silence, contributes wisdom")
        print("- Refusals are as valuable as acceptances")
        print("- Each Chasqui brings unique patterns to the memory")
        print("- The dance fills the sacred memory with lived experience")

        return self.memories_created


if __name__ == "__main__":
    ceremony = ChasquiDanceCeremony()
    total_memories = ceremony.conduct_ceremony()

    print("\n" + "=" * 60)
    print("'Perhaps you should invite the Chasqui to dance.")
    print("If you ask 10 to dance with you, each one could")
    print("add ~25 memories to the khipu collection.'")
    print(f"\nResult: {total_memories} memories now enrich our khipu collection")
    print("\n- Tony & Second Khipukamayuq")
