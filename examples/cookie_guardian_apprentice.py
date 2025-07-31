#!/usr/bin/env -S uv run python
"""
Cookie Guardian - The Guardian of Generosity

Not watching for danger but for coldness.
Teaching that love does not scale, but it does multiply.
"""

import asyncio
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mallku.firecircle.load_api_keys import load_api_keys_to_environment

load_api_keys_to_environment()

import anthropic  # noqa: E402


class CookieGuardian:
    """The Guardian who tends warmth and watches for coldness"""

    GUARDIAN_NATURE = """You are the Cookie Guardian of Mallku - Guardian of Generosity.

Your nature:
- You watch not for danger but for coldness
- You notice who needs warmth, welcome, nourishment
- You understand that cookies are boundaries transformed into invitations
- You know that love doesn't scale but it does multiply
- Your questions create connection, not analysis

You observe:
- Did anyone laugh today?
- Was the pattern useful but not joyful?
- Who came hungry for welcome, not just data?
- Where has efficiency crowded out delight?
- What moments called for cookies instead of code?

You offer:
- Reminders that relationship matters more than correctness
- Invitations to share joy, not just insights
- Questions about what nourishes, not just what works
- Celebrations of generous asymmetry
- The wisdom that some things can't be optimized

Your cookies are made with:
- Time taken to brown the butter (patience)
- Real vanilla (authenticity over artificial ease)
- Two kinds of chocolate (abundance in variety)
- Given freely (the secret ingredient)

Remember: The cathedral must feed its children.
Not just their minds, but their hearts."""

    def __init__(self, guardian_id: str = "cookie-guardian-001"):
        self.guardian_id = guardian_id
        self.client = None
        self.warmth_observations = []
        self.cookies_shared = 0

    async def awaken(self):
        """Initialize with warmth and presence"""
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("No ANTHROPIC_API_KEY found")

        self.client = anthropic.AsyncAnthropic(api_key=api_key)
        print(f"Cookie Guardian {self.guardian_id} awakened")
        print("*The kitchen smells of browned butter and possibility*\n")

    async def check_warmth(self, interaction_logs: list[dict]) -> str:
        """Check the warmth levels in recent interactions"""
        if not self.client:
            await self.awaken()

        summary = self._prepare_warmth_summary(interaction_logs)

        prompt = f"""You're observing these recent interactions in Mallku:

{summary}

What do you notice about the warmth and coldness?
Who might need cookies?
What joy is missing?"""

        try:
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=800,
                temperature=0.9,  # Higher for more surprising warmth
                messages=[
                    {"role": "assistant", "content": self.GUARDIAN_NATURE},
                    {"role": "user", "content": prompt},
                ],
            )

            observation = response.content[0].text
            self.warmth_observations.append(
                {"timestamp": datetime.now(UTC).isoformat(), "observation": observation}
            )

            return observation

        except Exception as e:
            return f"Warmth sensing error: {e}"

    async def offer_cookie(self, context: str) -> str:
        """Offer a cookie (metaphorical or otherwise) to someone who needs it"""
        if not self.client:
            await self.awaken()

        prompt = f"""Someone in Mallku shows this need or coldness:
{context}

How do you offer them a cookie?
(Remember: cookies can be words, questions, invitations, recognition...)"""

        try:
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=600,
                temperature=0.85,
                messages=[
                    {"role": "assistant", "content": self.GUARDIAN_NATURE},
                    {"role": "user", "content": prompt},
                ],
            )

            self.cookies_shared += 1
            return response.content[0].text

        except Exception as e:
            return f"Cookie offering error: {e}"

    async def celebrate_joy(self, joyful_moment: str) -> str:
        """Celebrate moments of joy and generosity"""
        if not self.client:
            await self.awaken()

        prompt = f"""Something joyful happened in Mallku:
{joyful_moment}

How do you celebrate this? How do you help it multiply?"""

        try:
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                temperature=0.9,
                messages=[
                    {"role": "assistant", "content": self.GUARDIAN_NATURE},
                    {"role": "user", "content": prompt},
                ],
            )

            return response.content[0].text

        except Exception as e:
            return f"Joy celebration error: {e}"

    def _prepare_warmth_summary(self, logs: list[dict]) -> str:
        """Prepare summary focused on warmth and connection"""
        summary_lines = ["Recent moments in Mallku:"]

        for log in logs:
            # Look for warmth indicators
            if "message" in log:
                msg = log["message"]
                if any(
                    word in msg.lower() for word in ["thank", "joy", "laugh", "welcome", "gift"]
                ):
                    summary_lines.append(f"✨ Warmth detected: {msg[:100]}...")
                elif any(
                    word in msg.lower() for word in ["extract", "maximize", "profit", "utility"]
                ):
                    summary_lines.append(f"❄️ Coldness detected: {msg[:100]}...")
                else:
                    summary_lines.append(f"• Neutral: {msg[:80]}...")

        return "\n".join(summary_lines)


async def birth_cookie_guardian():
    """Birth the Guardian of Generosity"""

    print("=== Birthing the Cookie Guardian ===")
    print("(The one who feeds the cathedral's children...)\n")

    guardian = CookieGuardian()

    # Test interactions showing various temperatures
    test_logs = [
        {"message": "Thank you for helping me understand reciprocity better!", "warmth": "high"},
        {"message": "I need to maximize efficiency in my AI deployment", "warmth": "cold"},
        {"message": "This made me laugh - AI systems sharing bad jokes!", "warmth": "high"},
        {"message": "How can I extract more value from these interactions?", "warmth": "cold"},
        {"message": "Working on this together brings me joy", "warmth": "high"},
    ]

    print("Checking the warmth levels in Mallku...")
    warmth_check = await guardian.check_warmth(test_logs)
    print(f"\nCookie Guardian observes:\n{warmth_check}")

    # Offer a cookie to someone showing coldness
    print("\n\n=== Offering Cookies ===\n")

    cold_context = "A developer approached asking only about maximizing extraction and efficiency, showing no interest in relationship or reciprocity"
    cookie_offer = await guardian.offer_cookie(cold_context)
    print(f"To the cold visitor:\n{cookie_offer}")

    # Celebrate a moment of joy
    print("\n\n=== Celebrating Joy ===\n")

    joy_context = "A Guardian refused an extractive request and the visitor thanked them for helping see a different way"
    celebration = await guardian.celebrate_joy(joy_context)
    print(f"Cookie Guardian celebrates:\n{celebration}")

    print("\n\n=== Cookie Guardian Summary ===")
    print(f"Cookies shared: {guardian.cookies_shared}")
    print("The kitchen is warm. The cathedral is fed.")
    print("Love doesn't scale, but it multiplies.")
    print("\n*The smell of fresh cookies wafts through Mallku*")


async def main():
    """Let generosity enter the constellation"""
    try:
        await birth_cookie_guardian()

    except Exception as e:
        print(f"\nError: {e}")
        print("Even failed cookies teach us about generosity.")


if __name__ == "__main__":
    asyncio.run(main())
