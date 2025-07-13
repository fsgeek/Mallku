#!/bin/bash
# Database Security Architecture Hook
# 51st Artisan - Architectural Integrity Patterns
#
# Prevents direct database access that bypasses security architecture
# Runs when you use Edit or Write tools on Python files

# Only check Python files
if [[ ! "$FILE_PATH" =~ \.py$ ]]; then
    exit 0
fi

# Skip test files
if [[ "$FILE_PATH" =~ test_ ]] || [[ "$FILE_PATH" =~ /tests/ ]]; then
    exit 0
fi

# Check for database security violations
VIOLATIONS=""

# Pattern 1: Direct get_database() usage
if grep -q "get_database()" "$FILE_PATH" 2>/dev/null; then
    VIOLATIONS="${VIOLATIONS}❌ Found get_database() - use get_secured_database() instead\n"
fi

# Pattern 2: Direct ArangoClient usage
if grep -q "ArangoClient" "$FILE_PATH" 2>/dev/null; then
    if ! grep -q "# security-exception" "$FILE_PATH" 2>/dev/null; then
        VIOLATIONS="${VIOLATIONS}❌ Found direct ArangoClient usage - use secure API gateway\n"
    fi
fi

# Pattern 3: Direct ArangoDB port
if grep -q "localhost:8529" "$FILE_PATH" 2>/dev/null; then
    VIOLATIONS="${VIOLATIONS}❌ Found direct ArangoDB port (8529) - use API gateway (8080)\n"
fi

# Pattern 4: Direct database imports
if grep -q "from.*database import get_database" "$FILE_PATH" 2>/dev/null; then
    VIOLATIONS="${VIOLATIONS}❌ Importing get_database - import get_secured_database instead\n"
fi

# If violations found, block the edit
if [ -n "$VIOLATIONS" ]; then
    echo -e "\n🛡️ Database Security Architecture Violation Detected!\n"
    echo -e "$VIOLATIONS"
    echo -e "📚 Context: All database access MUST go through the secure API gateway"
    echo -e "   See Issue #176 for architectural background\n"
    echo -e "✅ Use these secure patterns instead:"
    echo -e "   - get_secured_database() not get_database()"
    echo -e "   - API gateway (localhost:8080) not ArangoDB (localhost:8529)"
    echo -e "   - No direct ArangoClient instantiation\n"
    echo -e "💡 To override (only in core database modules):"
    echo -e "   Add comment: # security-exception: reason\n"
    exit 1
fi

exit 0
