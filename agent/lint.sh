#!/bin/bash
# Linting script for the Claude Context Optimizer Agent

echo "🔍 Running code quality checks..."
echo ""

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: Virtual environment not activated"
    echo "Run: source .venv/bin/activate"
    echo ""
fi

echo "1️⃣ Running isort (import sorting)..."
isort --check-only --diff entrypoint.py
echo ""

echo "2️⃣ Running black (code formatting)..."
black --check --diff entrypoint.py
echo ""

echo "3️⃣ Running flake8 (style guide)..."
flake8 entrypoint.py --max-line-length=100 --ignore=E501,W503
echo ""

echo "4️⃣ Running pylint (code analysis)..."
pylint entrypoint.py --disable=missing-docstring,too-few-public-methods,invalid-name,too-many-locals
echo ""

echo "5️⃣ Running mypy (type checking)..."
mypy entrypoint.py --ignore-missing-imports
echo ""

echo "✅ Linting complete!"