# Claude Context Optimizer GitHub Action

## Project Overview

This GitHub Action automatically analyzes any repository and generates comprehensive optimization recommendations for AI coding assistants. The action uses the Claude Code SDK to examine the entire codebase, understand project structure, dependencies, and conventions, then creates detailed recommendations that help developers improve their AI-assisted development workflows.

**Development Stage**: Production-ready GitHub Action with active development
**Target Users**: Developers seeking AI-assisted development workflow optimization
**Business Domain**: Developer tooling and AI-assisted code analysis

## Essential Commands

### Quick Start (Local Development)
```bash
# Setup and run locally
cd agent
./setup.sh
source .venv/bin/activate
export CLAUDE_API_KEY=your_key_here
python run.py
```

### Quality Assurance
```bash
# Format code
./format.sh

# Lint and check code quality
./lint.sh

# Run all quality checks
./format.sh && ./lint.sh
```

### Testing the Action
```bash
# Test with Docker (full container test)
docker build -t contextor .
docker run --rm -v $(pwd):/github/workspace -e CLAUDE_API_KEY=your_key_here contextor

# Test GitHub Action locally (requires act)
act workflow_dispatch -W .github/workflows/test.yml --secret CLAUDE_API_KEY=your_key_here
```

## Architecture

### Hybrid Technology Stack
This project uniquely combines Python 3.12 and Node.js for specific architectural reasons:
- **Python 3.12**: Main analysis agent with comprehensive async/await support
- **Node.js**: Required for Claude Code SDK CLI integration (`@anthropic-ai/claude-code`)
- **Docker**: Production container environment with both runtimes

### Critical Dependency Chain
- **Python SDK** (`claude-code-sdk>=0.0.23`): Main agent logic and async communication
- **Node.js CLI** (`@anthropic-ai/claude-code@^1.0.124`): Required subprocess dependency
- **Integration Pattern**: Python spawns Node.js CLI processes via subprocess calls
- **PATH Management**: Agent dynamically adds `node_modules/.bin` to PATH for CLI accessibility

### Critical Version Requirements
- **Python 3.12+ REQUIRED**: Hard requirement enforced by codebase
  - Required for modern async/await patterns in Claude SDK integration
  - Setup script attempts python3.12 first, falls back to python3 with version check
  - Local runner (`run.py`) will exit with error if Python < 3.12
- **Node.js 20.x**: Installed in Docker container, required locally for CLI

### Python Agent Structure
The action runs a Python 3.12-based agent that uses the Claude SDK for intelligent codebase analysis:

```
contextor/
├── agent/                     # Python agent package
│   ├── entrypoint.py          # Main analysis script
│   ├── prompts/               # Analysis prompts
│   │   ├── __init__.py        # Package initialization
│   │   ├── system-prompt.txt  # System context
│   │   └── optimizer-prompt.txt # Analysis instructions
│   ├── requirements.txt       # Python dependencies
│   ├── requirements-dev.txt   # Development dependencies
│   ├── setup.sh              # Local development setup
│   ├── format.sh             # Code formatting script
│   ├── lint.sh               # Code linting script
│   └── run.py                # Local testing runner
├── action.yml                # GitHub Action metadata
├── Dockerfile                # Python 3.12 container
└── examples/                 # Usage examples
    └── basic-usage.yml       # Basic workflow example
```

### Container vs Local Development

**Container Environment** (GitHub Actions):
```
/                              # Container root
├── agent/                     # Copied Python agent
│   ├── entrypoint.py          # Main analysis script
│   ├── prompts/               # Analysis prompts
│   └── requirements.txt       # Dependencies
└── github/
    └── workspace/             # Target repository (mounted)
        └── [user files]       # Project files to analyze
```

**Local Environment**:
- Workspace directory: Current directory or parent of `agent/` folder
- Output files: Created in workspace directory
- Environment variables: Must be set manually or via .env file

### Analysis Process

1. **Codebase Analysis**: Examines all files in the target repository
2. **Documentation Review**: Checks existing CLAUDE.md if present
3. **Gap Identification**: Identifies missing or outdated information
4. **Recommendations Generation**: Creates prioritized improvement suggestions
5. **Output**: Provides recommendations via GitHub Actions step summary with actionable insights

## Environment Configuration

### Required Environment Variables
- `CLAUDE_API_KEY`: Your Claude API key (required for all operations)
- `WORKSPACE_DIR`: Automatically set in containers, customizable for local development

### Environment Variable Management
- **Development**: Use `.env` file with gitignored credentials
- **Production**: GitHub Actions secrets via `CLAUDE_API_KEY` input
- **Local Testing**: Export directly or source .env file
- **Security**: Never commit real API keys to repository

### Setup Methods

**For Local Development**:
```bash
# Method 1: Export directly
export CLAUDE_API_KEY=your_key_here

# Method 2: Create .env file
echo 'CLAUDE_API_KEY=your_key_here' > agent/.env
source agent/.env
```

**For GitHub Actions**:
```yaml
- name: Run Claude Context Optimizer
  uses: guyaluk/contextor@v1
  with:
    claude-api-key: ${{ secrets.CLAUDE_API_KEY }}
```

## Usage

### GitHub Action Integration

Add to your workflow:

```yaml
- name: Run Claude Context Optimizer
  uses: guyaluk/contextor@v1
  with:
    claude-api-key: ${{ secrets.CLAUDE_API_KEY }}
```

### Local Development

```bash
# Setup the agent environment
cd agent
./setup.sh
source .venv/bin/activate

# Set API key and run
export CLAUDE_API_KEY=your_key_here
python run.py
```

### Docker Testing

```bash
# Build and test locally
docker build -t contextor .
docker run --rm -v $(pwd):/github/workspace \
  -e CLAUDE_API_KEY=your_key_here \
  contextor
```

## Development Standards

### Python Code Standards
- **Version**: Python 3.12+ required (critical for async/await features)
- **Style**: Follow PEP 8 conventions, enforced via black + flake8
- **Error Handling**: Comprehensive exception handling with clear messages
- **Logging**: Timestamped, color-coded progress indicators with emoji markers
- **Type Hints**: Use type annotations for better code clarity

### Code Quality Workflow
```bash
# Auto-format code (run before commits)
./format.sh

# Check all quality standards
./lint.sh
```

Quality tools configuration:
- **black**: Code formatting with 100-char line length
- **isort**: Import sorting and organization
- **flake8**: Style guide enforcement (E501, W503 ignored)
- **pylint**: Advanced code analysis with custom ignores
- **mypy**: Type checking with missing import tolerance

### Agent Architecture Patterns
- **SDK Integration**: Uses Claude Code SDK for direct API communication
- **Async/Await**: Modern async patterns for better performance
- **Progress Tracking**: Real-time monitoring of analysis progress with ProgressTracker class
- **Modular Design**: Clear separation between analysis logic and output generation
- **Error Handling**: Specific exception types (CLINotFoundError, ProcessError) with recovery strategies

### Agent Implementation Patterns

**Async Claude SDK Integration**:
```python
async with ClaudeSDKClient(options=options) as client:
    await client.connect()
    await client.query(optimizer_prompt)
    async for message in client.receive_response():
        # Process ToolUseBlock, ToolResultBlock, TextBlock
```

**Progress Tracking Pattern**:
- Real-time tool usage monitoring via ProgressTracker class
- Statistics: files read/written, commands run, searches performed
- Tool restrictions: `["Read", "Write", "Glob", "Grep", "Bash", "MultiEdit", "Edit"]`

### Claude SDK Integration Patterns

**Tool Configuration**:
```python
options = ClaudeCodeOptions(
    allowed_tools=["Read", "Write", "Glob", "Grep", "Bash", "MultiEdit", "Edit"],
    permission_mode="acceptEdits",
    add_dirs=[str(workspace_dir)],
    system_prompt=system_prompt,
)
```

**Async Message Processing**:
```python
async for message in client.receive_response():
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock):
                # Process tool usage
            elif isinstance(block, TextBlock):
                # Process reasoning text
```

## Technology Stack

- **Runtime**: Python 3.12 in Docker container
- **AI Integration**: Claude Code SDK (claude-code-sdk>=0.0.23)
- **Container**: Python 3.12-slim base image with Node.js 20.x
- **GitHub Actions**: Docker container action type
- **Development**: Virtual environment with pip requirements

## Testing Strategy

- **No Unit Tests**: This project uses code quality tools instead of traditional unit tests
- **Quality Assurance**: Comprehensive linting pipeline via `./lint.sh` and `./format.sh`
  - isort → black → flake8 → pylint → mypy
- **Integration Testing**: Manual Docker container testing and GitHub Actions workflow validation
- **Release Testing**: Automated release verification creates test repository and validates action functionality
- **Manual Testing**: Local development via `python run.py` with different workspace configurations

## Output Format

The action writes recommendations directly to the **GitHub Actions Step Summary**, providing:

- **Analysis Overview**: Current documentation state and key metrics
- **Priority Recommendations**: Organized as expandable sections (High/Medium/Low)
- **Detailed Suggestions**: Specific improvements with examples
- **Complete Template**: Full recommended CLAUDE.md content (collapsible)
- **Statistics**: Analysis metrics, file counts, and execution time

For local development, the agent provides console output with progress tracking and creates output files with timestamped filenames (e.g., `CONTEXT_RECOMMENDATIONS_20241225_143022.md`).

## Error Handling and Troubleshooting

### Common Issues and Solutions

**Claude CLI Not Found**:
- Ensure Node.js is installed and npm dependencies are installed
- Check that `node_modules/.bin` is in PATH

**API Key Issues**:
- Verify CLAUDE_API_KEY environment variable is set
- Ensure API key has necessary permissions

**Permission Errors**:
- Check file permissions in workspace directory
- Ensure Docker has appropriate volume mount permissions

### Error Recovery Patterns
The agent handles three main error types:
1. **CLINotFoundError**: Claude CLI installation issues
2. **ProcessError**: Claude SDK execution problems
3. **General Exception**: Unexpected errors with full context logging

## Testing

- **Local Development**: Run with `python agent/run.py` after setting up virtual environment
- **Docker Testing**: Full container testing with mounted volumes
- **Code Quality**: Automated linting and formatting with `lint.sh` and `format.sh`
- **Manual Triggers**: `workflow_dispatch` available in example workflows

## Prompt Engineering Architecture

The agent uses a dual-prompt system:
- **system-prompt.txt**: Agent role, constraints, capabilities (injected via ClaudeCodeOptions)
- **optimizer-prompt.txt**: Analysis instructions with `{recommendations_filename}` template variable
- **Template Pattern**: Variable substitution via `.format()` method before sending to Claude
- **Separation of Concerns**: System context vs task-specific instructions

Prompt templates support variable substitution:
```python
optimizer_prompt = optimizer_prompt_template.format(
    recommendations_filename=recommendations_filename
)
```

## Deployment & Release Process

### GitHub Actions CI/CD
- **Release Workflow**: Automated releases with semantic version tagging
- **Version Management**: Automatic major/minor version tag updates
- **Changelog Generation**: Git-based changelog creation
- **Release Testing**: Automated verification creates test repository and validates released action

### Release Testing Process
1. Creates temporary test repository with sample files
2. Tests released action version against test repository
3. Verifies recommendation generation and output format
4. Validates GitHub Actions integration

The action is designed to provide actionable, non-invasive recommendations that help developers optimize their AI-assisted development workflows.