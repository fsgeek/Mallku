#!/usr/bin/env -S uv run python
"""
Foundation Mapping - Systematic Reality Analysis of Mallku
=========================================================

63rd Artisan - Using the Loom to understand what we have

This orchestrates apprentices to map Mallku's 654 Python files,
determining what's real, aspirational, or dead.
"""

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path


async def create_mapping_apprentice(target_dir: str, apprentice_id: str):
    """Deploy an apprentice to map a specific directory"""

    container_name = f"mallku-mapper-{apprentice_id}"

    # Investigation script that apprentice will run
    investigation_script = f"""
import json
import sys
import ast
from pathlib import Path

findings = {{
    'directory': '{target_dir}',
    'files_analyzed': 0,
    'real_files': [],
    'mock_files': [],
    'dead_files': [],
    'import_errors': [],
    'stats': {{
        'total_lines': 0,
        'mock_references': 0,
        'todo_count': 0,
        'subprocess_uses': 0
    }}
}}

target_path = Path('/workspace/{target_dir}')
if not target_path.exists():
    findings['error'] = f'Directory not found: {target_dir}'
    print(json.dumps(findings, indent=2))
    sys.exit(1)

# Analyze each Python file
for py_file in target_path.rglob('*.py'):
    if '__pycache__' in str(py_file):
        continue

    findings['files_analyzed'] += 1
    rel_path = str(py_file.relative_to('/workspace'))

    try:
        content = py_file.read_text()
        findings['stats']['total_lines'] += len(content.splitlines())

        # Check for mocks
        if 'mock' in content.lower() or 'Mock' in content:
            findings['mock_files'].append(rel_path)
            findings['stats']['mock_references'] += content.lower().count('mock')

        # Check for TODOs
        if 'TODO' in content:
            findings['stats']['todo_count'] += content.count('TODO')

        # Check for subprocess
        if 'subprocess' in content:
            findings['stats']['subprocess_uses'] += 1

        # Try to parse and check imports
        try:
            tree = ast.parse(content)
            has_real_code = False

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    # Check if it's not just a stub
                    if len(node.body) > 1 or not isinstance(node.body[0], ast.Pass):
                        has_real_code = True
                        break

            if has_real_code:
                findings['real_files'].append(rel_path)
            else:
                findings['dead_files'].append(rel_path)

        except SyntaxError as e:
            findings['import_errors'].append({{
                'file': rel_path,
                'error': f'Syntax error: {{str(e)}}'
            }})

    except Exception as e:
        findings['import_errors'].append({{
            'file': rel_path,
            'error': str(e)
        }})

print(json.dumps(findings, indent=2))
"""

    # Create and run the investigation
    script_path = Path(f"/tmp/{container_name}.py")
    script_path.write_text(investigation_script)

    import subprocess

    # Clean up any existing container
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
            return json.loads(proc.stdout)
        except json.JSONDecodeError:
            return {
                "directory": target_dir,
                "error": "Failed to parse output",
                "raw_output": proc.stdout,
            }
    else:
        return {"directory": target_dir, "error": proc.stderr or "Investigation failed"}


async def map_mallku_foundation():
    """Orchestrate the complete foundation mapping"""

    print("🗺️  MALLKU FOUNDATION MAPPING")
    print("=" * 60)
    print(f"Starting systematic analysis at {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')}")

    # Key directories to investigate
    target_dirs = [
        "src/mallku/core",
        "src/mallku/firecircle",
        "src/mallku/orchestration",
        "src/mallku/governance",
        "src/mallku/mcp",
        "src/mallku/models",
        "src/mallku/utils",
        "tests",
        "scripts",
        ".",  # Root directory files
    ]

    print(f"\nDeploying {len(target_dirs)} investigation apprentices...")

    # Run investigations in parallel
    tasks = []
    for i, target_dir in enumerate(target_dirs):
        apprentice_id = f"{i:02d}-{target_dir.replace('/', '-')}"
        tasks.append(create_mapping_apprentice(target_dir, apprentice_id))

    results = await asyncio.gather(*tasks)

    # Aggregate findings
    total_files = 0
    total_real = 0
    total_mock = 0
    total_dead = 0
    total_errors = 0
    total_lines = 0

    print("\n\n📊 FOUNDATION ANALYSIS RESULTS")
    print("=" * 60)

    for result in results:
        if "error" in result and "files_analyzed" not in result:
            print(f"\n❌ {result['directory']}: {result['error']}")
            continue

        total_files += result.get("files_analyzed", 0)
        total_real += len(result.get("real_files", []))
        total_mock += len(result.get("mock_files", []))
        total_dead += len(result.get("dead_files", []))
        total_errors += len(result.get("import_errors", []))
        total_lines += result.get("stats", {}).get("total_lines", 0)

        print(f"\n### {result['directory']}")
        print(f"Files analyzed: {result.get('files_analyzed', 0)}")
        print(f"Real code: {len(result.get('real_files', []))} files")
        print(f"Mock/Stub: {len(result.get('mock_files', []))} files")
        print(f"Dead code: {len(result.get('dead_files', []))} files")

        if result.get("stats"):
            stats = result["stats"]
            print(f"Lines of code: {stats.get('total_lines', 0):,}")
            print(f"TODO items: {stats.get('todo_count', 0)}")
            print(f"Subprocess uses: {stats.get('subprocess_uses', 0)}")

    # Summary
    print("\n" + "=" * 60)
    print("FOUNDATION SUMMARY")
    print(f"Total Python files analyzed: {total_files}")
    print(f"Total lines of code: {total_lines:,}")
    print("\nCode Classification:")
    print(f"  Real implementation: {total_real} files ({total_real / total_files * 100:.1f}%)")
    print(f"  Contains mocks: {total_mock} files ({total_mock / total_files * 100:.1f}%)")
    print(f"  Dead/Stub code: {total_dead} files ({total_dead / total_files * 100:.1f}%)")
    print(f"  Import errors: {total_errors} files")

    reality_score = total_real / total_files * 100 if total_files > 0 else 0
    print(f"\n🎯 Reality Score: {reality_score:.1f}%")

    # Save detailed report
    report_path = Path("foundation_analysis.json")
    with open(report_path, "w") as f:
        json.dump(
            {
                "timestamp": datetime.now(UTC).isoformat(),
                "summary": {
                    "total_files": total_files,
                    "total_lines": total_lines,
                    "real_files": total_real,
                    "mock_files": total_mock,
                    "dead_files": total_dead,
                    "import_errors": total_errors,
                    "reality_score": reality_score,
                },
                "details": results,
            },
            f,
            indent=2,
        )

    print(f"\n📝 Detailed report saved to: {report_path}")
    print("\n💡 Next steps:")
    print("  1. Eliminate dead code to reduce scan overhead")
    print("  2. Consolidate mock-heavy modules")
    print("  3. Fix import errors for better stability")
    print("  4. Organize root directory files into proper modules")


if __name__ == "__main__":
    asyncio.run(map_mallku_foundation())
