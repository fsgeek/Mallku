"""
Mock objects for testing Fire Circle components.
"""


class MockResponse:
    def __init__(self):
        self.content = type(
            "obj",
            (object,),
            {
                "text": """File: src/mallku/firecircle/governance/decision.py
Line: 12
Category: security
Severity: critical
Issue: No authentication check before processing decisions
Fix: Add authentication verification before processing

File: src/mallku/firecircle/governance/decision.py
Line: 11
Category: security
Severity: warning
Issue: Input validation TODO not implemented
Fix: Implement input validation for proposal parameter"""
            },
        )
        self.consciousness = type("obj", (object,), {"consciousness_signature": 0.85})


class MockAdapter:
    def __init__(self, name):
        self.name = name
        self.is_connected = True

    async def send_message(self, message, dialogue_context):
        return MockResponse()


class MockMessage:
    def __init__(self, text):
        self.text = text
