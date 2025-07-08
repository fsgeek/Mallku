import asyncio
from unittest.mock import MagicMock, patch

import pytest

from mallku.firecircle.runner import FireCircleReviewRunner


class TestGitHubIntegration:
    """Verify GitHub API integration for Fire Circle."""

    @pytest.mark.asyncio
    @patch("mallku.firecircle.runner.Github")
    async def test_fetch_pr_context(self, MockGithub):
        """Test that _fetch_pr_context correctly fetches the PR diff."""
        # Arrange
        mock_github_instance = MockGithub.return_value
        mock_repo = MagicMock()
        mock_pr = MagicMock()
        mock_pr.get_diff.return_value = "mocked diff"
        mock_repo.get_pull.return_value = mock_pr
        mock_github_instance.get_repo.return_value = mock_repo

        runner = FireCircleReviewRunner()

        # Act
        with patch.dict("os.environ", {"GITHUB_TOKEN": "test_token", "GITHUB_REPOSITORY": "fsgeek/Mallku"}):
            diff = await runner._fetch_pr_context(123)

        # Assert
        assert diff == "mocked diff"
        mock_github_instance.get_repo.assert_called_once_with("fsgeek/Mallku")
        mock_repo.get_pull.assert_called_once_with(123)
