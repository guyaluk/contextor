# AI Agent Context Optimizer

Python-based agent for analyzing codebases and generating AI agent context documentation recommendations (CLAUDE.md, AGENTS.md, or similar) using the Claude SDK.

## Requirements

- Python 3.12+
- Node.js 20.x+ (for Claude CLI)
- Claude API key

## Setup for Local Development

### Quick Setup

1. **Create and activate virtual environment:**
   ```bash
   cd agent
   ./setup.sh
   source .venv/bin/activate
   ```

### Manual Setup

1. **Ensure you have Python 3.12:**
   ```bash
   python3.12 --version
   # or check if python3 is 3.12
   python3 --version
   ```

2. **Create virtual environment:**
   ```bash
   python3.12 -m venv .venv
   # or use python3 if it's version 3.12
   python3 -m venv .venv
   ```

3. **Activate virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Install Node.js dependencies (Claude CLI):**
   ```bash
   npm install
   ```

### Running the Agent

1. **Set your Claude API key:**
   ```bash
   export CLAUDE_API_KEY=your_key_here
   ```

   Or create a `.env` file:
   ```bash
   echo 'CLAUDE_API_KEY=your_key_here' > .env
   source .env
   ```

2. **Run the agent:**
   ```bash
   python run.py
   ```

### Development Tools

**Code Quality:**
```bash
# Auto-format code
./format.sh

# Run all linting checks
./lint.sh
```

**Available tools:**
- `isort` - Import sorting
- `black` - Code formatting
- `flake8` - Style guide enforcement
- `pylint` - Code analysis
- `mypy` - Type checking

   The agent will:
   - Analyze the current directory (or parent if running from agent folder)
   - For GitHub Actions: Write recommendations to step summary
   - For local testing: Generate `AI_CONTEXT_RECOMMENDATIONS.md` file
   - Provide detailed progress logging

## Project Structure

```
agent/
├── __init__.py              # Package initialization
├── entrypoint.py            # Main agent script using Claude SDK
├── prompts/                 # System and optimizer prompts
│   ├── __init__.py
│   ├── system-prompt.txt    # System context and instructions
│   └── optimizer-prompt.txt # Analysis and recommendation instructions
├── requirements.txt         # Python dependencies
├── requirements-dev.txt     # Development tools (linting, formatting)
├── package.json            # Node.js dependencies (Claude CLI)
├── setup.sh                # Virtual environment setup script
├── format.sh               # Code formatting automation
├── lint.sh                 # Code quality checks
├── run.py                  # Local runner for testing
└── README.md              # This file
```

## Features

### Enhanced Logging
- Real-time progress tracking
- Color-coded output for easy reading
- Detailed statistics and analysis summary
- Tool usage monitoring with comprehensive reporting

### Python SDK Integration
- Uses Claude Code SDK with local Claude CLI for direct integration
- Asynchronous execution with proper error handling
- Better performance and control over the analysis process
- Direct access to tool results and progress tracking

### Language Detection & Standards
- Automatically detects programming languages used in the codebase
- Recommends language-specific conventions (Python PEP 8, JavaScript ESLint, etc.)
- Provides concrete examples for naming patterns and code organization
- Focuses on project-specific patterns that differ from defaults

### Local Development Support
- Virtual environment with proper dependencies
- Local testing without Docker
- Python 3.12 version checking
- Flexible workspace configuration

## Docker Usage

This agent is designed to run in a Docker container as part of a GitHub Action:

```bash
# Build the container
docker build -t contextor .

# Test locally with your repository
docker run --rm -v $(pwd):/github/workspace \
  -e CLAUDE_API_KEY=your_key_here \
  contextor
```

## Output

The agent provides comprehensive recommendations via:

**GitHub Actions**: Written to step summary with new two-section format:
- **Issues & Recommendations**: Clear list of what's missing and needs to be added
- **Complete Copyable Context File**: Full recommended documentation in a code block for easy copying
- **Efficiency Impact Analysis**: Detailed assessment of how recommendations improve AI agent efficiency

**Local Testing**: For local development, the agent analyzes the current directory and provides:
- **Console Output**: Real-time progress with colored logging
- **Analysis Summary**: Current documentation state and key findings
- **File Generation**: May generate recommendation files depending on Claude's analysis results

## Troubleshooting

### Python Version Issues
```bash
# Check your Python version
python3 --version

# Install Python 3.12 on macOS
brew install python@3.12

# Install Python 3.12 on Ubuntu/Debian
sudo apt update && sudo apt install python3.12
```

### Import Errors
```bash
# Make sure you're in the agent directory
cd agent

# Activate virtual environment
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### API Key Issues
```bash
# Check if API key is set
echo $CLAUDE_API_KEY

# Set API key for current session
export CLAUDE_API_KEY=your_key_here

# Or add to your shell profile for persistence
echo 'export CLAUDE_API_KEY=your_key_here' >> ~/.bashrc
source ~/.bashrc
```

## Development

To extend or modify the agent:

1. **Modify prompts**: Edit files in `prompts/` directory
2. **Add features**: Update `entrypoint.py` with new functionality
3. **Add dependencies**: Update `requirements.txt` and run `pip install -r requirements.txt`
4. **Test locally**: Use `python run.py` for quick testing
5. **Test in Docker**: Build and run the container

## Integration with GitHub Actions

The agent integrates with the main GitHub Action workflow. See the main project README for usage instructions.

The action uses standard exit codes:
- **Exit 0**: Analysis completed successfully, recommendations written to step summary
- **Exit 1**: Analysis failed, check the logs for details