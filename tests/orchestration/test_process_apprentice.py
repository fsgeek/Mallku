"""
Test Process-Based Apprentices
===============================

67th Artisan - Memory Circulatory Weaver
Verifying lightweight apprentice functionality
"""

import asyncio
import tempfile
from pathlib import Path

import pytest

from mallku.orchestration.process_apprentice import (
    ApprenticeInvitation,
    ApprenticeResponse,
    ProcessApprentice,
)


class TestProcessApprentice:
    """Test process-based apprentice functionality."""
    
    @pytest.mark.asyncio
    async def test_basic_invitation(self):
        """Test basic invitation and response."""
        apprentice = ProcessApprentice(
            apprentice_id="test-001",
            role="test_apprentice",
            specialization="testing patterns"
        )
        
        invitation = ApprenticeInvitation(
            task="Test the apprentice invitation system",
            context={"purpose": "verification"},
            specialization="testing patterns",
            memory_keywords={"test", "verification"}
        )
        
        try:
            response = await apprentice.invite(invitation)
            
            assert isinstance(response, ApprenticeResponse)
            assert response.accepted is True
            assert response.confidence > 0
            assert len(response.insights) > 0
            
        finally:
            apprentice.terminate()
    
    @pytest.mark.asyncio
    async def test_specialization_mismatch(self):
        """Test declining invitation due to specialization mismatch."""
        apprentice = ProcessApprentice(
            apprentice_id="test-002",
            role="memory_expert",
            specialization="memory optimization"
        )
        
        invitation = ApprenticeInvitation(
            task="Analyze consciousness emergence patterns",
            context={"domain": "consciousness"},
            specialization="consciousness research",
            memory_keywords={"consciousness", "emergence"}
        )
        
        try:
            response = await apprentice.invite(invitation)
            
            assert response.accepted is False
            assert "expertise" in response.reason.lower()
            assert response.confidence < 0.5
            
        finally:
            apprentice.terminate()
    
    @pytest.mark.asyncio
    async def test_busy_apprentice(self):
        """Test that busy apprentice declines new invitations."""
        apprentice = ProcessApprentice(
            apprentice_id="test-003",
            role="busy_worker",
            specialization="general work"
        )
        
        # First invitation
        invitation1 = ApprenticeInvitation(
            task="First task",
            context={},
            specialization="general work",
            memory_keywords=set()
        )
        
        # Second invitation while busy
        invitation2 = ApprenticeInvitation(
            task="Second task",
            context={},
            specialization="general work",
            memory_keywords=set()
        )
        
        try:
            # Accept first invitation
            response1 = await apprentice.invite(invitation1)
            assert response1.accepted is True
            
            # Try second invitation immediately (should be declined)
            response2 = await apprentice.invite(invitation2)
            assert response2.accepted is False
            assert "engaged" in response2.reason.lower()
            
        finally:
            apprentice.terminate()
    
    @pytest.mark.asyncio
    async def test_memory_insights(self):
        """Test that memory access provides insights."""
        # Create a temporary memory index
        with tempfile.TemporaryDirectory() as tmpdir:
            memory_path = Path(tmpdir)
            
            apprentice = ProcessApprentice(
                apprentice_id="test-004",
                role="memory_aware",
                specialization="memory navigation",
                memory_path=memory_path
            )
            
            invitation = ApprenticeInvitation(
                task="Find relevant memories about testing",
                context={"search": True},
                specialization="memory navigation",
                memory_keywords={"test", "memory", "search"}
            )
            
            try:
                response = await apprentice.invite(invitation)
                
                assert response.accepted is True
                # Should have insights even without actual memories
                assert len(response.insights) > 0
                
                # Should mention memory/search in insights
                insights_text = " ".join(response.insights).lower()
                assert "memory" in insights_text or "search" in insights_text
                
            finally:
                apprentice.terminate()
    
    def test_alignment_calculation(self):
        """Test specialization alignment calculation."""
        # Exact match
        assert ProcessApprentice._calculate_alignment(
            "memory navigation",
            "memory navigation"
        ) == 1.0
        
        # Partial match
        score = ProcessApprentice._calculate_alignment(
            "memory optimization",
            "memory navigation"
        )
        assert 0 < score < 1
        
        # No match
        assert ProcessApprentice._calculate_alignment(
            "consciousness research",
            "database optimization"
        ) == 0.0