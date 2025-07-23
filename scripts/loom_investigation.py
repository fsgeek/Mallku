#!/usr/bin/env -S uv run python
"""
Loom Investigation - Using MCP to audit Mallku's reality
========================================================

63rd Artisan - Actually delegating to apprentices
"""

import asyncio
import json
from pathlib import Path


async def create_investigation_container(component: str, script: str):
    """Create an investigation apprentice using MCP Docker tools"""

    container_name = f"mallku-investigate-{component.lower().replace(' ', '-')}"

    # Create a temporary script file
    script_path = Path(f"/tmp/{container_name}.py")
    script_path.write_text(script)

    print(f"\n🔍 Investigating: {component}")

    # This is where Claude would use actual MCP tools:
    # result = await mcp__docker-mcp__create-container(...)

    # For demonstration, using subprocess
    import subprocess

    # Remove any existing container
    subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)

    # Run investigation
    proc = subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--name",
            container_name,
            "-v",
            f"{Path.cwd()}:/workspace:ro",
            "-v",
            f"{script_path}:/investigate.py:ro",
            "-e",
            "PYTHONPATH=/workspace/src",
            "python:3.13-slim",
            "python",
            "/investigate.py",
        ],
        capture_output=True,
        text=True,
    )

    # Clean up
    script_path.unlink(missing_ok=True)

    if proc.returncode == 0:
        try:
            findings = json.loads(proc.stdout)
            return findings
        except json.JSONDecodeError:
            return {
                "component": component,
                "status": "error",
                "output": proc.stdout,
                "error": "Failed to parse JSON",
            }
    else:
        return {"component": component, "status": "error", "error": proc.stderr}


async def investigate_mallku():
    """Coordinate investigation of multiple Mallku components"""

    investigations = [
        {
            "component": "Fire Circle",
            "script": """
import json
import sys
from pathlib import Path

findings = {
    "component": "Fire Circle",
    "status": "investigating",
    "real": [],
    "aspirational": [],
    "notes": []
}

try:
    # Check if Fire Circle can be imported
    sys.path.insert(0, '/workspace/src')
    from mallku.firecircle import convene_fire_circle
    findings["real"].append("Core module imports successfully")

    # Check for MessageType patch
    from mallku.firecircle.protocol.message_type_patch import patch_message_type
    findings["real"].append("MessageType patch exists (62nd Artisan fix)")

    # Check for mock interfaces
    fc_path = Path('/workspace/src/mallku/firecircle')
    mock_count = 0
    subprocess_count = 0

    for py_file in fc_path.rglob('*.py'):
        content = py_file.read_text()
        if 'mock' in content.lower() and 'mock' not in py_file.name:
            mock_count += 1
        if 'subprocess' in content:
            subprocess_count += 1

    if mock_count > 0:
        findings["aspirational"].append(f"{mock_count} files contain mock references")
    if subprocess_count > 0:
        findings["notes"].append(f"{subprocess_count} files use subprocess")

    findings["status"] = "complete"

except ImportError as e:
    findings["aspirational"].append(f"Import failed: {str(e)}")
    findings["status"] = "error"

print(json.dumps(findings, indent=2))
""",
        },
        {
            "component": "Weaver and Loom",
            "script": """
import json
import sys
from pathlib import Path

findings = {
    "component": "Weaver and Loom",
    "status": "investigating",
    "real": [],
    "aspirational": [],
    "notes": []
}

try:
    sys.path.insert(0, '/workspace/src')

    # Check Loom
    loom_path = Path('/workspace/src/mallku/orchestration/loom')
    if loom_path.exists():
        findings["real"].append("Loom directory exists")

        # Check for actual MCP usage
        mcp_files = []
        subprocess_files = []

        for py_file in loom_path.glob('*.py'):
            content = py_file.read_text()
            if 'mcp' in content.lower():
                if 'subprocess' in content:
                    subprocess_files.append(py_file.name)
                else:
                    mcp_files.append(py_file.name)

        if subprocess_files:
            findings["aspirational"].append(
                f"MCP integration uses subprocess: {subprocess_files}"
            )

        # Check for 62nd/63rd Artisan contributions
        if (loom_path / 'minimal_loom.py').exists():
            findings["real"].append("Minimal Loom exists (62nd Artisan)")
        if (loom_path / 'real_loom.py').exists():
            findings["real"].append("Real Loom exists (63rd Artisan)")
        if (loom_path / 'mcp_real_loom.py').exists():
            findings["real"].append("MCP Real Loom exists (63rd Artisan)")

    findings["status"] = "complete"

except Exception as e:
    findings["status"] = "error"
    findings["notes"].append(str(e))

print(json.dumps(findings, indent=2))
""",
        },
        {
            "component": "Database Security",
            "script": """
import json
import sys
from pathlib import Path

findings = {
    "component": "Database Security",
    "status": "investigating",
    "real": [],
    "aspirational": [],
    "notes": []
}

try:
    sys.path.insert(0, '/workspace/src')

    # Check for database security script
    script_path = Path('/workspace/scripts/verify_database_security.py')
    if script_path.exists():
        findings["real"].append("Security verification script exists")

    # Check for API gateway
    gateway_path = Path('/workspace/src/mallku/core/database/secure_gateway.py')
    if gateway_path.exists():
        findings["real"].append("Secure gateway implementation exists")

    # Check for violations
    db_path = Path('/workspace/src/mallku/core/database')
    direct_access = 0
    secured_access = 0

    for py_file in Path('/workspace/src').rglob('*.py'):
        if 'test' not in str(py_file):
            content = py_file.read_text()
            if 'get_database()' in content:
                direct_access += 1
            if 'get_secured_database()' in content:
                secured_access += 1

    if direct_access > 0:
        findings["aspirational"].append(f"{direct_access} files use direct database access")
    if secured_access > 0:
        findings["real"].append(f"{secured_access} files use secured access")

    findings["status"] = "complete"

except Exception as e:
    findings["status"] = "error"
    findings["notes"].append(str(e))

print(json.dumps(findings, indent=2))
""",
        },
    ]

    print("🧵 Loom Investigation - Auditing Mallku's Reality")
    print("=" * 60)
    print("Delegating investigations to apprentice containers...")

    # Run investigations concurrently
    results = await asyncio.gather(
        *[create_investigation_container(inv["component"], inv["script"]) for inv in investigations]
    )

    # Generate report
    print("\n\n📊 MALLKU REALITY AUDIT REPORT")
    print("=" * 60)

    total_real = 0
    total_aspirational = 0

    for result in results:
        if result.get("status") == "complete":
            real_count = len(result.get("real", []))
            asp_count = len(result.get("aspirational", []))
            total_real += real_count
            total_aspirational += asp_count

            print(f"\n### {result['component']}")
            print("Status: ✓ Complete")
            print(f"Real components: {real_count}")
            print(f"Aspirational components: {asp_count}")

            if result.get("real"):
                print("\nReal:")
                for item in result["real"]:
                    print(f"  ✓ {item}")

            if result.get("aspirational"):
                print("\nAspirational:")
                for item in result["aspirational"]:
                    print(f"  ⚠ {item}")

            if result.get("notes"):
                print("\nNotes:")
                for note in result["notes"]:
                    print(f"  • {note}")
        else:
            print(f"\n### {result.get('component', 'Unknown')}")
            print("Status: ✗ Error")
            if result.get("error"):
                print(f"Error: {result['error']}")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print(f"Total real components found: {total_real}")
    print(f"Total aspirational components: {total_aspirational}")
    print(f"Reality ratio: {total_real / (total_real + total_aspirational) * 100:.1f}%")

    print("\n💡 Key Insight: With working delegation, we can systematically")
    print("   audit all of Mallku without exhausting weaver context!")


if __name__ == "__main__":
    asyncio.run(investigate_mallku())
