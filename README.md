# AI Agent Context Optimizer 🤖

[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Test Action](https://github.com/guyaluk/contextor/actions/workflows/test.yml/badge.svg)](https://github.com/guyaluk/contextor/actions/workflows/test.yml)
[![Release](https://github.com/guyaluk/contextor/actions/workflows/release.yml/badge.svg)](https://github.com/guyaluk/contextor/actions/workflows/release.yml)
[![GitHub release](https://img.shields.io/github/release/guyaluk/contextor.svg)](https://github.com/guyaluk/contextor/releases/latest)

A GitHub Action that automatically analyzes your codebase and generates focused AI agent context documentation recommendations (CLAUDE.md, AGENTS.md, or similar) for AI coding assistants. The action provides detailed analysis with concrete examples and language-specific suggestions displayed directly in GitHub Actions step summaries.

## 🎯 What it does

This action uses Claude AI to:
- **Analyze your entire codebase** - Examines source code, dependencies, configuration files, and project structure
- **Auto-detect programming languages** - Automatically recommends language-specific conventions (Python PEP 8, JavaScript ESLint, etc.)
- **Generate focused recommendations** - Creates targeted suggestions for missing critical context, not verbose documentation
- **Provide concrete examples** - Every recommendation includes specific examples of naming patterns, commands, and code structures
- **Prioritize actionable insights** - High/Medium/Low priority recommendations that save AI assistants time and prevent errors

## 🚀 Quick Start

### Basic Usage

Create `.github/workflows/analyze-claude-md.yml`:

```yaml
name: Analyze AI Context Documentation
on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  analyze-codebase:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run AI Agent Context Optimizer
        uses: guyaluk/contextor@v0
        with:
          claude-api-key: ${{ secrets.CLAUDE_API_KEY }}
          context-file: 'CLAUDE.md'  # or 'AGENTS.md'

      # Results will be displayed in the step summary above
```

### Prerequisites

1. **Claude API Key**: This action uses Claude Code SDK for intelligent codebase analysis
   - Get your API key from [Claude AI](https://claude.ai/account/keys)
   - The key is required because the action uses Claude's AI to analyze your codebase and generate context recommendations
2. **GitHub Secret**: Add your API key as `CLAUDE_API_KEY` in your repository secrets
   - Go to your repository → Settings → Secrets and variables → Actions
   - Create a new secret named `CLAUDE_API_KEY` with your API key as the value

## 📋 Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `claude-api-key` | Claude API key for authentication | ✅ Yes | - |
| `context-file` | AI agent context file to analyze (CLAUDE.md or AGENTS.md) | ✅ Yes | - |

## 📤 Outputs

The action communicates success/failure via standard exit codes:
- **Exit 0**: Analysis completed successfully, recommendations written to step summary
- **Exit 1**: Analysis failed, check the action logs for details

## 📚 Recommendations Structure

The generated recommendations provide insights for these essential AI agent context documentation sections:

**🎯 Detected Languages & Standards** (New!)
- Auto-detected programming languages with specific conventions
- Concrete examples: "Python → snake_case functions (get_user_data), PascalCase classes (UserManager)"

**Core Sections:**
1. **📋 Overview** - Project purpose, users, development stage
2. **🏗️ Architecture** - System design, tech stack, components, data flow
3. **⚡ Key Commands** - Essential commands not obvious from scripts
4. **🛠️ Development Setup** - Critical setup steps that aren't automated
5. **📁 Project Structure** - Non-standard directory organization and conventions
6. **📏 Coding Standards** - Project-specific patterns that differ from defaults
7. **🔧 Framework & Technology** - Unusual configurations or integration approaches
8. **🧪 Testing** - Testing approach, frameworks, patterns, quality gates

**New Two-Section Format:**
1. **Issues & Recommendations**: Clear list of what's missing and needs to be added
2. **Complete Copyable Context File**: Full recommended documentation in a code block for easy copying

**Focus on Critical Context Only:**
- Recommendations target missing information that would cause AI assistants to waste time or make wrong assumptions
- Every recommendation includes concrete examples and implementation details
- Avoids documenting obvious information that's easily discoverable in configuration files

## 💡 Usage Examples

### Manual Analysis Trigger

```yaml
on:
  workflow_dispatch:
    inputs:
      detailed_analysis:
        description: 'Run detailed analysis'
        required: false
        default: true
        type: boolean

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: guyaluk/contextor@v0
        with:
          claude-api-key: ${{ secrets.CLAUDE_API_KEY }}
          context-file: 'CLAUDE.md'
```

### Scheduled Analysis

```yaml
on:
  schedule:
    - cron: '0 9 * * 1'  # Weekly analysis on Mondays at 9 AM UTC
  workflow_dispatch:

jobs:
  weekly-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Weekly AI Context Analysis
        uses: guyaluk/contextor@v0
        with:
          claude-api-key: ${{ secrets.CLAUDE_API_KEY }}
          context-file: 'CLAUDE.md'
```

### Pull Request Analysis

```yaml
on:
  pull_request:
    branches: [main]

jobs:
  analyze-pr:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Analyze codebase for AI agent context recommendations
        uses: guyaluk/contextor@v0
        with:
          claude-api-key: ${{ secrets.CLAUDE_API_KEY }}
          context-file: 'CLAUDE.md'
```

## 📁 Example Workflows

Check the [`examples/`](./examples/) directory for complete workflow examples:

- [`basic-usage.yml`](./examples/basic-usage.yml) - Basic analysis workflow that displays AI agent context recommendations in step summary

## 🔧 Advanced Configuration

### Handling Success/Failure

The action uses standard exit codes. You can add steps that run conditionally:

```yaml
- name: Run AI Agent Context Optimizer
  uses: guyaluk/contextor@v0
  with:
    claude-api-key: ${{ secrets.CLAUDE_API_KEY }}
    context-file: 'CLAUDE.md'

- name: Success notification
  if: success()
  run: echo "✅ Analysis completed successfully! Check step summary above for recommendations"

- name: Failure notification
  if: failure()
  run: echo "❌ Analysis failed! Check the logs above for details"
```

## 📋 Versioning

This action follows [semantic versioning](https://semver.org/):

- `@v0` - Latest v0.x.x (current version)
- `@v0.1` - Latest v0.1.x patch
- `@v0.1.0` - Specific version (for maximum control)

### Version Tags

- **Major versions** (`v0`, `v1`) - Automatically updated to latest
- **Minor versions** (`v0.1`, `v0.2`) - Updated to latest patch
- **Patch versions** (`v0.1.0`, `v0.1.1`) - Immutable specific versions

## 🔒 Security

- **API Key Security**: Your Claude API key is passed as a secret and never logged
- **Isolated Execution**: Runs in a Docker container with minimal permissions
- **No Data Persistence**: No data is stored outside your repository
- **Read-Only Analysis**: Only reads your codebase, generates recommendations without modifying any source code

## 🐛 Troubleshooting

### Common Issues

**Action fails with API key error:**
```
❌ Error: CLAUDE_API_KEY environment variable is required
```
- Ensure you've added `CLAUDE_API_KEY` to your repository secrets
- Check that the secret name matches exactly

**No recommendations generated:**
- Check the action logs for Claude API errors
- Verify your API key has sufficient credits
- Ensure the repository has source code to analyze
- Look for recommendations in the GitHub Actions step summary

**Python environment errors:**
- The action runs in a Python 3.12 Docker container with all dependencies pre-installed
- For local testing, see the `agent/README.md` for setup instructions

### Getting Help

1. Check the [workflow logs](../../actions) for detailed error messages
2. Review the [examples](./examples/) for correct configuration
3. Open an [issue](../../issues) with your workflow configuration and error logs

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with the provided workflows
5. Submit a pull request

### Development

To test changes locally:

```bash
# Build the Docker image
docker build -t contextor .

# Test with a sample repository
docker run --rm -v $(pwd):/github/workspace \
  -e CLAUDE_API_KEY=your_key_here \
  contextor
```

## 💬 Feedback & Community

I'd love to hear from users about their experience with this action! Whether you have:

- 🤔 **Questions** about features or implementation
- 🐛 **Issues** you've encountered
- 💡 **Feature requests** or ideas for improvements
- 📝 **General feedback** on what you think about the product
- 🎯 **Use cases** you'd like to see supported

**Feel free to reach out:**
- **Open an issue** on this GitHub repository for bugs, feature requests, or questions
- **Send me a DM** if you want to discuss something interesting or share feedback privately

Your input helps make this tool better for everyone using AI-assisted development!

---

*This action helps bridge the gap between human developers and AI assistants by ensuring your project documentation is always current, comprehensive, and AI-friendly.*