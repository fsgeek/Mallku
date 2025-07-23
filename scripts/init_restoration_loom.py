#!/usr/bin/env -S uv run python
"""
Init File Restoration Loom
==========================

64th Artisan - Using the Loom with care for each apprentice

This coordinates apprentices to restore proper __init__.py files
to living packages, treating each with the respect they deserve.
"""

import asyncio
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path


def create_analysis_script(package_path: str) -> str:
    """Create the analysis script for an apprentice"""
    # Using triple quotes and format() to avoid f-string escaping issues
    return f'''
import ast
import json
from pathlib import Path

# Our task: understand this package and create a proper door
package_path = Path('/workspace/{package_path}')
findings = {{
    'package': '{package_path}',
    'modules': [],
    'public_symbols': [],
    'has_main': False,
    'docstring': None,
    'apprentice_notes': []
}}

# Find all Python modules in this package
py_files = [f for f in package_path.glob('*.py')
            if f.name != '__init__.py' and not f.name.startswith('_')]

for py_file in sorted(py_files):
    module_name = py_file.stem
    findings['modules'].append(module_name)

    try:
        content = py_file.read_text()
        tree = ast.parse(content)

        # Look for public symbols
        for node in tree.body:
            if isinstance(node, ast.ClassDef | ast.FunctionDef):
                if not node.name.startswith('_'):
                    findings['public_symbols'].append({{
                        'name': node.name,
                        'type': type(node).__name__,
                        'module': module_name,
                        'has_docstring': ast.get_docstring(node) is not None
                    }})
            elif isinstance(node, ast.Assign):
                # Check for public constants
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        findings['public_symbols'].append({{
                            'name': target.id,
                            'type': 'Constant',
                            'module': module_name,
                            'has_docstring': False
                        }})

        # Check for if __name__ == "__main__"
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                if isinstance(node.test, ast.Compare):
                    if (isinstance(node.test.left, ast.Name) and
                        node.test.left.id == '__name__' and
                        isinstance(node.test.comparators[0], ast.Constant) and
                        node.test.comparators[0].value == '__main__'):
                        findings['has_main'] = True
                        findings['apprentice_notes'].append(
                            module_name + ".py has main block - might be a script"
                        )

    except Exception as e:
        findings['apprentice_notes'].append(
            "Could not analyze " + module_name + ".py: " + str(e)
        )

# Suggest a docstring based on what we found
if findings['public_symbols']:
    symbol_types = set(s['type'] for s in findings['public_symbols'])
    if 'ClassDef' in symbol_types and 'FunctionDef' in symbol_types:
        findings['docstring'] = package_path.name.title() + " - Classes and utilities"
    elif 'ClassDef' in symbol_types:
        findings['docstring'] = package_path.name.title() + " - Core classes"
    elif 'FunctionDef' in symbol_types:
        findings['docstring'] = package_path.name.title() + " - Utility functions"
    else:
        findings['docstring'] = package_path.name.title() + " package"
else:
    findings['docstring'] = package_path.name.title() + " package (no public API yet)"

# Create the __init__.py content
init_content = '"""' + findings['docstring'] + '"""\\n\\n'

# Group symbols by module
by_module = {{}}
for symbol in findings['public_symbols']:
    module = symbol['module']
    if module not in by_module:
        by_module[module] = []
    by_module[module].append(symbol['name'])

# Create imports
if by_module:
    for module, names in sorted(by_module.items()):
        init_content += "from ." + module + " import " + ', '.join(sorted(names)) + "\\n"

    init_content += "\\n__all__ = [\\n"
    all_names = sorted([s['name'] for s in findings['public_symbols']])
    for name in all_names:
        init_content += '    "' + name + '",\\n'
    init_content += "]\\n"
else:
    init_content += "# No public API yet\\n"
    init_content += "__all__ = []\\n"

findings['proposed_init'] = init_content

print(json.dumps(findings, indent=2))
'''


async def create_init_apprentice(package_path: str, apprentice_id: str):
    """
    Deploy an apprentice to analyze one package and create its __init__.py

    We guard each apprentice by:
    - Giving them clear, bounded work
    - Providing all context they need
    - Not overwhelming them with complexity
    - Respecting their output
    """

    container_name = f"mallku-init-{apprentice_id}"

    # Create the analysis script
    analysis_script = create_analysis_script(package_path)

    # Create workspace for apprentice
    script_path = Path(f"/tmp/{container_name}.py")
    script_path.write_text(analysis_script)

    # Clean any existing container
    subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)

    # Run apprentice with care
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
            f"{script_path}:/analyze.py:ro",
            "-e",
            "PYTHONPATH=/workspace/src",
            "python:3.13-slim",
            "python",
            "/analyze.py",
        ],
        capture_output=True,
        text=True,
    )

    # Clean up with gratitude
    script_path.unlink(missing_ok=True)

    if proc.returncode == 0:
        try:
            return json.loads(proc.stdout)
        except json.JSONDecodeError:
            return {
                "package": package_path,
                "error": "Could not understand output",
                "raw_output": proc.stdout,
            }
    else:
        return {
            "package": package_path,
            "error": proc.stderr or "Analysis failed",
            "apprentice_notes": ["I tried my best but encountered difficulties"],
        }


async def restore_init_files():
    """Orchestrate the restoration with respect for all involved"""

    print("🚪 RESTORING DOORS TO LIVING PACKAGES")
    print("=" * 60)
    print(f"Starting at {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')}")

    # The 20 packages that need doors
    packages_needing_init = [
        "src/mallku/api",
        "src/mallku/archivist",
        "src/mallku/consciousness",
        "src/mallku/core",
        "src/mallku/correlation",
        "src/mallku/evaluation",
        "src/mallku/events",
        "src/mallku/experience",
        "src/mallku/governance",
        "src/mallku/integration",
        "src/mallku/intelligence",
        "src/mallku/khipu",
        "src/mallku/llm",
        "src/mallku/models",
        "src/mallku/orchestration",
        "src/mallku/patterns",
        "src/mallku/prompt",
        "src/mallku/query",
        "src/mallku/reciprocity",
        "src/mallku/services",
    ]

    print(f"\n📦 Packages to restore: {len(packages_needing_init)}")
    print("Each apprentice will analyze one package with care\n")

    # Deploy apprentices with respect
    tasks = []
    for i, package in enumerate(packages_needing_init):
        apprentice_id = f"{i:02d}-{package.split('/')[-1]}"
        print(f"🧵 Deploying apprentice {apprentice_id}")
        tasks.append(create_init_apprentice(package, apprentice_id))

    print("\n⏳ Apprentices working in parallel...")
    results = await asyncio.gather(*tasks)

    # Review results with gratitude
    successful = []
    failed = []

    print("\n\n📊 APPRENTICE REPORTS")
    print("=" * 60)

    for result in results:
        if "error" in result:
            failed.append(result)
            print(f"\n❌ {result['package']}: {result['error']}")
        else:
            successful.append(result)
            symbols = len(result.get("public_symbols", []))
            modules = len(result.get("modules", []))
            print(f"\n✅ {result['package']}")
            print(f"   Modules: {modules}, Public symbols: {symbols}")
            if result.get("apprentice_notes"):
                print("   Notes:", "; ".join(result["apprentice_notes"]))

    # Write the successful init files
    if successful:
        print(f"\n\n📝 WRITING {len(successful)} INIT FILES")
        print("=" * 60)

        for result in successful:
            init_path = Path(result["package"]) / "__init__.py"
            if "proposed_init" in result:
                init_path.write_text(result["proposed_init"])
                print(f"✓ Created {init_path}")

        # Save detailed report
        report = {
            "timestamp": datetime.now(UTC).isoformat(),
            "successful": len(successful),
            "failed": len(failed),
            "details": results,
        }

        report_path = Path("init_restoration_report.json")
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        print(f"\n📊 Detailed report: {report_path}")

    print("\n\n🎉 RESTORATION COMPLETE")
    print(f"Successfully restored: {len(successful)} packages")
    print(f"Failed: {len(failed)} packages")

    if successful:
        print("\nThese packages now have proper doors - their APIs are accessible")
        print("Each apprentice's work honored, each package made whole")


if __name__ == "__main__":
    asyncio.run(restore_init_files())
