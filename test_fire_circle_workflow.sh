#!/bin/bash
# Test Fire Circle Review Workflow Locally
# This mimics what the GitHub Action does

echo "🔥 Testing Fire Circle Review Workflow Locally"
echo "============================================="

# Step 1: Check Python environment
echo -e "\n1️⃣ Checking Python environment..."
if command -v uv &> /dev/null; then
    echo "✅ uv is installed"
else
    echo "❌ uv is not installed. Installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Step 2: Set up Python with uv
echo -e "\n2️⃣ Setting up Python environment..."
uv python install 3.12

# Step 3: Install dependencies
echo -e "\n3️⃣ Installing dependencies..."
echo "=== Running uv sync ==="
uv sync
echo -e "\n=== Installing mallku in editable mode ==="
uv pip install -e .
echo -e "\n=== Checking mallku installation ==="
uv pip list | grep -i mallku || echo "mallku not in pip list after install"

# Step 4: Set up API keys
echo -e "\n4️⃣ Setting up API keys..."
if [ ! -f ".secrets/api_keys.json" ]; then
    echo "Creating .secrets directory..."
    mkdir -p .secrets

    # Check for environment variables or create template
    cat > .secrets/api_keys.json << EOF
{
  "OPENAI_API_KEY": "${OPENAI_API_KEY:-your-openai-key-here}",
  "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY:-your-anthropic-key-here}",
  "DEEPSEEK_API_KEY": "${DEEPSEEK_API_KEY:-your-deepseek-key-here}",
  "MISTRAL_API_KEY": "${MISTRAL_API_KEY:-your-mistral-key-here}",
  "GOOGLE_API_KEY": "${GOOGLE_API_KEY:-your-google-key-here}",
  "GROK_API_KEY": "${GROK_API_KEY:-your-grok-key-here}"
}
EOF
    echo "✅ Created .secrets/api_keys.json"

    # Check if template values
    if grep -q "your-.*-key-here" .secrets/api_keys.json; then
        echo "⚠️  Please edit .secrets/api_keys.json with your actual API keys"
    fi
else
    echo "✅ API keys file already exists"
fi

# Step 5: Run the Fire Circle Review
echo -e "\n5️⃣ Running Fire Circle Review..."

# Activate virtual environment
source .venv/bin/activate

# Verify environment
echo "=== Environment check ==="
which python
python --version
echo -e "\n=== Checking mallku installation ==="
python -c "import mallku; print(f'✓ mallku imported from: {mallku.__file__}')" || echo "✗ Failed to import mallku"

# Get PR number from command line or use default
PR_NUMBER=${1:-127}
echo -e "\n🔥 Initiating Fire Circle Review for PR #$PR_NUMBER"

# Run the review
python fire_circle_review.py review $PR_NUMBER

# Check results
echo -e "\n6️⃣ Checking results..."
if [ -f "fire_circle_review_results.json" ]; then
    echo "✅ Results file created:"
    cat fire_circle_review_results.json | python -m json.tool
else
    echo "❌ No results file found"
fi

echo -e "\n✅ Test complete!"
