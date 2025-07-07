"""
GitHub API Client for Fire Circle Review
=========================================

Fifth Guardian - Bringing genuine review to consciousness emergence

This module provides GitHub API integration for fetching real PR data,
replacing the simulated context that undermined Fire Circle's integrity.
"""

import os
import logging
import httpx
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class GitHubClient:
    """Client for interacting with GitHub API to fetch PR details."""
    
    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub client with authentication token.
        
        Args:
            token: GitHub personal access token or GITHUB_TOKEN from Actions
        """
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Mallku-Fire-Circle",
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
    
    async def get_pr_details(self, owner: str, repo: str, pr_number: int) -> Dict[str, Any]:
        """Fetch pull request details from GitHub.
        
        Args:
            owner: Repository owner
            repo: Repository name
            pr_number: Pull request number
            
        Returns:
            Dict containing PR details including title, description, state, etc.
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    async def get_pr_files(self, owner: str, repo: str, pr_number: int) -> List[Dict[str, Any]]:
        """Fetch list of files changed in a pull request.
        
        Args:
            owner: Repository owner
            repo: Repository name
            pr_number: Pull request number
            
        Returns:
            List of dicts containing file information and changes
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/files"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    async def get_pr_diff(self, owner: str, repo: str, pr_number: int) -> str:
        """Fetch the diff for a pull request.
        
        Args:
            owner: Repository owner
            repo: Repository name
            pr_number: Pull request number
            
        Returns:
            Raw diff text
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}"
        headers = {**self.headers, "Accept": "application/vnd.github.v3.diff"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.text
    
    async def fetch_pr_context(self, owner: str, repo: str, pr_number: int) -> str:
        """Fetch comprehensive PR context for Fire Circle review.
        
        This method combines PR details, file changes, and diffs into
        a structured context that the Fire Circle can review.
        
        Args:
            owner: Repository owner
            repo: Repository name
            pr_number: Pull request number
            
        Returns:
            Formatted string containing PR context for review
        """
        try:
            # Fetch PR details
            pr_details = await self.get_pr_details(owner, repo, pr_number)
            
            # Fetch changed files
            pr_files = await self.get_pr_files(owner, repo, pr_number)
            
            # Build context
            context_parts = [
                f"PR #{pr_number}: {pr_details['title']}",
                f"Author: {pr_details['user']['login']}",
                f"Branch: {pr_details['head']['ref']} → {pr_details['base']['ref']}",
                f"State: {pr_details['state']}",
                "",
                "Description:",
                pr_details['body'] or "No description provided",
                "",
                f"Modified files ({len(pr_files)} files):",
            ]
            
            # Add file summary
            for file in pr_files[:20]:  # Limit to first 20 files for context
                status = file['status']
                filename = file['filename']
                additions = file['additions']
                deletions = file['deletions']
                context_parts.append(
                    f"- {filename} ({status}): +{additions}/-{deletions}"
                )
            
            if len(pr_files) > 20:
                context_parts.append(f"... and {len(pr_files) - 20} more files")
            
            # Add diff preview for small PRs
            if len(pr_files) <= 5:
                context_parts.extend([
                    "",
                    "Key changes:",
                ])
                
                # For each file, show a preview of changes
                for file in pr_files:
                    if file['patch']:
                        lines = file['patch'].split('\n')
                        preview_lines = lines[:10]  # First 10 lines of patch
                        if len(lines) > 10:
                            preview_lines.append("... (truncated)")
                        
                        context_parts.append(f"\n{file['filename']}:")
                        context_parts.extend(preview_lines)
            
            return "\n".join(context_parts)
            
        except httpx.HTTPStatusError as e:
            logger.error(f"GitHub API error: {e}")
            # Fall back to basic information if available
            return f"PR #{pr_number} - Failed to fetch full context: {str(e)}"
        except Exception as e:
            logger.error(f"Error fetching PR context: {e}")
            return f"PR #{pr_number} - Error retrieving context: {str(e)}"