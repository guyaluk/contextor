#!/bin/bash
# Auto-formatting script for the Claude Context Optimizer Agent

echo "🔧 Auto-formatting code..."
echo ""

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: Virtual environment not activated"
    echo "Run: source .venv/bin/activate"
    echo ""
fi

echo "1️⃣ Running isort (sorting imports)..."
isort entrypoint.py
echo ""

echo "2️⃣ Running black (formatting code)..."
black entrypoint.py
echo ""

echo "✅ Formatting complete!"
echo ""
echo "Run ./lint.sh to check for remaining issues."