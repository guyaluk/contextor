#!/bin/bash
# Setup virtual environment for local development

echo "🔧 Setting up virtual environment with Python 3.12..."

# Check if Python 3.12 is available
if command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
    echo "✅ Found Python 3.12"
elif command -v python3 &> /dev/null; then
    python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )\d+\.\d+')
    if [[ "$python_version" == "3.12" ]]; then
        PYTHON_CMD="python3"
        echo "✅ Found Python 3.12 as python3"
    else
        echo "⚠️  Warning: Python 3.12 is recommended. Found Python $python_version"
        echo "   This may work but consider installing Python 3.12"
        PYTHON_CMD="python3"
    fi
else
    echo "❌ Error: Python 3 not found. Please install Python 3.12"
    exit 1
fi

# Create .venv if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    $PYTHON_CMD -m venv .venv
    echo "✅ Created virtual environment"
else
    echo "📦 Virtual environment already exists"
fi

# Activate .venv
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Install development dependencies
echo "🔧 Installing development tools..."
pip install -r requirements-dev.txt

# Install npm dependencies for Claude CLI
echo "📦 Installing Claude CLI..."
if command -v npm &> /dev/null; then
    npm install
    echo "✅ Claude CLI installed locally"
else
    echo "⚠️  Warning: npm not found. Please install Node.js to use Claude CLI"
    echo "   The agent requires the Claude Code CLI to function"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To activate the environment, run:"
echo "  source .venv/bin/activate"
echo ""
echo "To run the agent locally:"
echo "  python run.py"
echo ""
echo "To deactivate when done:"
echo "  deactivate"