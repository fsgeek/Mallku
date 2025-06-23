#!/usr/bin/env python3
"""
CI Health Monitor - Caregiver's Tool for Mallku's Wellbeing

This tool watches over the health of Mallku's continuous integration,
ensuring that the cathedral's foundations remain strong and that
builders can work with confidence.
"""

import asyncio
import json
import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn


console = Console()


class CIHealthMonitor:
    """
    A caregiver for Mallku's CI/CD health.
    
    Like a gardener tending to sacred plants, this monitor watches
    for signs of illness and helps maintain the cathedral's vitality.
    """
    
    def __init__(self):
        self.repo_path = Path(__file__).parent.parent
        self.workflow_path = self.repo_path / ".github" / "workflows"
        
    async def check_workflow_status(self) -> Dict[str, any]:
        """Check the current status of all GitHub Actions workflows."""
        try:
            # Use gh CLI to get workflow runs
            result = subprocess.run(
                ["gh", "run", "list", "--repo", "fsgeek/Mallku", "--json", "status,conclusion,workflow_name,created_at"],
                capture_output=True,
                text=True,
                check=True
            )
            
            runs = json.loads(result.stdout)
            
            # Group by workflow
            workflows = {}
            for run in runs:
                name = run["workflow_name"]
                if name not in workflows:
                    workflows[name] = {
                        "recent_runs": [],
                        "health_score": 1.0,
                        "last_success": None,
                        "failure_streak": 0
                    }
                
                workflows[name]["recent_runs"].append(run)
                
                # Update health metrics
                if run["conclusion"] == "success":
                    if workflows[name]["last_success"] is None:
                        workflows[name]["last_success"] = run["created_at"]
                    workflows[name]["failure_streak"] = 0
                elif run["conclusion"] == "failure":
                    workflows[name]["failure_streak"] += 1
                    workflows[name]["health_score"] *= 0.9  # Decay health score
            
            return workflows
            
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error checking workflow status: {e}[/red]")
            return {}
    
    async def check_test_health(self) -> Dict[str, any]:
        """Run tests locally to verify current code health."""
        console.print("[cyan]Running local test suite...[/cyan]")
        
        test_results = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "duration": 0
        }
        
        try:
            start_time = datetime.now()
            result = subprocess.run(
                ["pytest", "--json-report", "--json-report-file=test_report.json"],
                capture_output=True,
                text=True,
                cwd=self.repo_path
            )
            
            duration = (datetime.now() - start_time).total_seconds()
            test_results["duration"] = duration
            
            # Parse test report if it exists
            report_file = self.repo_path / "test_report.json"
            if report_file.exists():
                with open(report_file) as f:
                    report = json.load(f)
                    test_results["total_tests"] = report.get("summary", {}).get("total", 0)
                    test_results["passed"] = report.get("summary", {}).get("passed", 0)
                    test_results["failed"] = report.get("summary", {}).get("failed", 0)
                    test_results["skipped"] = report.get("summary", {}).get("skipped", 0)
                
                # Clean up report file
                report_file.unlink()
            
        except Exception as e:
            console.print(f"[yellow]Warning: Could not run tests: {e}[/yellow]")
        
        return test_results
    
    async def generate_health_report(self) -> str:
        """Generate a comprehensive health report for Mallku's CI."""
        console.print(Panel.fit("[bold cyan]Mallku CI Health Check[/bold cyan]", title="🏥 Caregiver's Report"))
        
        # Check workflow status
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Checking GitHub Actions workflows...", total=None)
            workflows = await self.check_workflow_status()
            progress.update(task, completed=True)
        
        # Check local test health
        test_results = await self.check_test_health()
        
        # Create health report table
        table = Table(title="Workflow Health Status")
        table.add_column("Workflow", style="cyan")
        table.add_column("Health Score", style="magenta")
        table.add_column("Last Success", style="green")
        table.add_column("Failure Streak", style="red")
        
        for name, data in workflows.items():
            health_score = f"{data['health_score']:.2%}"
            last_success = data['last_success'] or "Never"
            failure_streak = str(data['failure_streak'])
            
            table.add_row(name, health_score, last_success, failure_streak)
        
        console.print(table)
        
        # Test results
        if test_results["total_tests"] > 0:
            console.print(f"\n[bold]Local Test Results:[/bold]")
            console.print(f"  Total: {test_results['total_tests']}")
            console.print(f"  Passed: [green]{test_results['passed']}[/green]")
            console.print(f"  Failed: [red]{test_results['failed']}[/red]")
            console.print(f"  Skipped: [yellow]{test_results['skipped']}[/yellow]")
            console.print(f"  Duration: {test_results['duration']:.2f}s")
        
        # Recommendations
        console.print("\n[bold]Caregiver's Recommendations:[/bold]")
        
        for name, data in workflows.items():
            if data['failure_streak'] > 3:
                console.print(f"  ⚠️  [yellow]{name} needs immediate attention (failing for {data['failure_streak']} runs)[/yellow]")
            elif data['health_score'] < 0.7:
                console.print(f"  📊 [orange]{name} showing signs of instability (health: {data['health_score']:.2%})[/orange]")
        
        if test_results["failed"] > 0:
            console.print(f"  🔧 [red]Fix {test_results['failed']} failing local tests[/red]")
        
        return "Health check complete"
    
    async def watch_health(self, interval: int = 300):
        """Continuously monitor CI health at regular intervals."""
        console.print(f"[green]Starting CI health monitoring (checking every {interval} seconds)...[/green]")
        
        while True:
            await self.generate_health_report()
            console.print(f"\n[dim]Next check in {interval} seconds... (Press Ctrl+C to stop)[/dim]")
            await asyncio.sleep(interval)


async def main():
    """Main entry point for the CI health monitor."""
    monitor = CIHealthMonitor()
    
    # Check for command line arguments
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--watch":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 300
        await monitor.watch_health(interval)
    else:
        await monitor.generate_health_report()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[cyan]Health monitoring stopped by caregiver.[/cyan]")