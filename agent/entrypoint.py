#!/usr/bin/env python3
"""
Claude Context Optimizer - Python SDK Implementation
Analyzes codebases and generates CLAUDE.md recommendations using ClaudeSDKClient
"""

import asyncio
import os
import sys
import time
from datetime import datetime
from pathlib import Path

from claude_code_sdk import (
    AssistantMessage,
    ClaudeCodeOptions,
    ClaudeSDKClient,
    CLINotFoundError,
    ProcessError,
    TextBlock,
    ToolResultBlock,
    ToolUseBlock,
)


class Colors:
    """ANSI color codes for terminal output"""

    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BLUE = "\033[0;34m"
    YELLOW = "\033[1;33m"
    NC = "\033[0m"  # No Color


def log(message: str) -> None:
    """Simple logging function with timestamp"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def write_github_step_summary(content: str) -> None:
    """Write content to GitHub step summary for display in Actions UI"""
    github_step_summary = os.getenv("GITHUB_STEP_SUMMARY")
    if github_step_summary:
        with open(github_step_summary, "a", encoding="utf-8") as f:
            # Wrap content in HTML details/summary for collapsible sections
            # and use proper markdown code blocks for copyable content
            f.write(content)
            f.write("\n")


class ProgressTracker:
    """Track analysis progress and statistics"""

    def __init__(self):
        self.files_read = []
        self.files_written = []
        self.commands_run = []
        self.searches_performed = []
        self.start_time = time.time()

    def add_file_read(self, path: str):
        self.files_read.append(path)

    def add_file_written(self, path: str):
        self.files_written.append(path)

    def add_command(self, cmd: str):
        self.commands_run.append(cmd)

    def add_search(self, pattern: str):
        self.searches_performed.append(pattern)

    def get_summary(self) -> str:
        duration = time.time() - self.start_time
        return f"""Analysis completed in {duration:.1f}s:
   - Files read: {len(self.files_read)}
   - Files written: {len(self.files_written)}
   - Commands run: {len(self.commands_run)}
   - Searches performed: {len(self.searches_performed)}"""


async def main() -> None:
    """Main function to run the Claude analysis"""

    # Configuration - allow override for local testing
    workspace_dir = Path(os.getenv("WORKSPACE_DIR", "/github/workspace"))

    # Generate timestamp for recommendations filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    recommendations_filename = f"AI_CONTEXT_RECOMMENDATIONS_{timestamp}.md"
    recommendations_file = workspace_dir / recommendations_filename

    # Detect GitHub Actions environment
    is_github_actions = bool(os.getenv("GITHUB_STEP_SUMMARY"))

    log(f"{Colors.BLUE}🚀 Claude Context Optimizer - Python SDK{Colors.NC}")
    log(f"📅 Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"📁 Workspace Directory: {workspace_dir}")
    log("")

    # Validate required environment variables
    claude_api_key = os.getenv("CLAUDE_API_KEY")
    if not claude_api_key:
        log(
            f"{Colors.RED}❌ Error: CLAUDE_API_KEY environment variable is required{Colors.NC}"
        )
        sys.exit(1)

    # Validate context file parameter
    context_file = os.getenv("CONTEXT_FILE", "").upper()
    if not context_file:
        log(
            f"{Colors.RED}❌ Error: CONTEXT_FILE environment variable is required{Colors.NC}"
        )
        log("Please specify either 'CLAUDE.md' or 'AGENTS.md'")
        sys.exit(1)

    if context_file not in ["CLAUDE.MD", "AGENTS.MD"]:
        log(
            f"{Colors.RED}❌ Error: Invalid CONTEXT_FILE '{context_file}'{Colors.NC}"
        )
        log("Please specify either 'CLAUDE.md' or 'AGENTS.md'")
        sys.exit(1)

    # Convert back to proper case for file operations
    context_file = "CLAUDE.md" if context_file == "CLAUDE.MD" else "AGENTS.md"
    log(f"🎯 Target context file: {context_file}")

    # Set ANTHROPIC_API_KEY for Claude CLI authentication
    os.environ["ANTHROPIC_API_KEY"] = claude_api_key
    log("🔑 Set ANTHROPIC_API_KEY for Claude CLI authentication")

    # Add local node_modules/.bin to PATH for Claude CLI
    # Check multiple possible locations for node_modules
    possible_paths = [
        Path("/agent/node_modules/.bin"),  # Docker container location
        Path(__file__).parent / "node_modules" / ".bin",  # Local development
    ]

    local_bin_path = None
    for path in possible_paths:
        if path.exists():
            local_bin_path = str(path)
            break

    if local_bin_path:
        current_path = os.environ.get("PATH", "")
        os.environ["PATH"] = f"{local_bin_path}:{current_path}"
        log(f"📦 Added local CLI to PATH: {local_bin_path}")
    else:
        log(f"{Colors.YELLOW}⚠️  Warning: Could not find node_modules/.bin in any expected location{Colors.NC}")

    # Check if the specified context file exists in workspace
    context_path = workspace_dir / context_file
    context_path_lower = workspace_dir / context_file.lower()

    existing_context_file = None
    if context_path.exists():
        existing_context_file = context_file
    elif context_path_lower.exists():
        existing_context_file = context_file.lower()

    if existing_context_file:
        log(f"📄 Existing {existing_context_file} found - will analyze and generate recommendations")
    else:
        log(f"📄 No existing {context_file} found - will generate recommendations for new file")

    # Read prompt files - use relative paths for package structure
    try:
        # For Docker container or package installation
        system_prompt_path = Path(__file__).parent / "prompts" / "system-prompt.txt"
        optimizer_prompt_path = (
            Path(__file__).parent / "prompts" / "optimizer-prompt.txt"
        )

        # Fallback to absolute paths for compatibility
        if not system_prompt_path.exists():
            system_prompt_path = Path("/system-prompt.txt")
        if not optimizer_prompt_path.exists():
            optimizer_prompt_path = Path("/optimizer-prompt.txt")

        if not system_prompt_path.exists():
            log(
                f"{Colors.RED}❌ Error: System prompt file not found: {system_prompt_path}{Colors.NC}"
            )
            sys.exit(1)

        if not optimizer_prompt_path.exists():
            log(
                f"{Colors.RED}❌ Error: Optimizer prompt file not found: "
                f"{optimizer_prompt_path}{Colors.NC}"
            )
            sys.exit(1)

        system_prompt = system_prompt_path.read_text(encoding="utf-8")
        optimizer_prompt_template = optimizer_prompt_path.read_text(encoding="utf-8")

        # Format the optimizer prompt with the recommendations filename and context file
        optimizer_prompt = optimizer_prompt_template.format(
            recommendations_filename=recommendations_filename,
            context_file=context_file
        )

        log("📄 Successfully loaded prompt files")
        log(f"📄 Recommendations will be written to: {recommendations_filename}")

    except Exception as e:
        log(f"{Colors.RED}❌ Error reading prompt files: {e}{Colors.NC}")
        sys.exit(1)

    # Initialize progress tracker
    tracker = ProgressTracker()
    tools_used = set()

    # Configure Claude SDK options

    log(f"{Colors.BLUE}🤖 Initializing Claude SDK...{Colors.NC}")

    options = ClaudeCodeOptions(
        allowed_tools=["Read", "Write", "Glob", "Grep", "Bash", "MultiEdit", "Edit", "TodoWrite"],
        permission_mode="acceptEdits",
        add_dirs=[str(workspace_dir)],
        system_prompt=system_prompt,
    )

    # System prompt is injected via system_prompt in ClaudeCodeOptions
    # Optimizer prompt contains the task instructions

    log(
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    try:
        # Run Claude analysis using SDK
        log(
            f"{Colors.BLUE}🤖 Running AI agent context analysis and recommendations generation...{Colors.NC}"
        )

        async with ClaudeSDKClient(options=options) as client:
            # Connect to Claude
            await client.connect()

            # Send the analysis request with formatted prompt
            await client.query(optimizer_prompt)

            # Monitor progress and collect responses
            log("📡 Monitoring Claude's progress...")
            log("   (Real-time tool usage and reasoning will be shown below)")

            claude_reasoning_count = 0

            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, ToolUseBlock):
                            tool_name = block.name
                            tools_used.add(tool_name)

                            # Log tool usage in real-time
                            if tool_name == "Read":
                                file_path = block.input.get("file_path", "")
                                log(f"📖 Reading: {file_path}")
                                tracker.add_file_read(file_path)
                            elif tool_name in ["Write", "MultiEdit", "Edit"]:
                                file_path = block.input.get("file_path", "")
                                log(f"✍️  Writing: {file_path}")
                                tracker.add_file_written(file_path)
                            elif tool_name == "Bash":
                                command = block.input.get("command", "")[
                                    :100
                                ]  # Truncate long commands
                                log(f"⚡ Running: {command}...")
                                tracker.add_command(command)
                            elif tool_name == "Grep":
                                pattern = block.input.get("pattern", "")
                                path = block.input.get("path", ".")
                                log(f"🔍 Searching '{pattern}' in {path}")
                                tracker.add_search(pattern)
                            elif tool_name == "Glob":
                                pattern = block.input.get("pattern", "")
                                log(f"📁 Finding files: {pattern}")
                                tracker.add_search(pattern)
                            else:
                                log(f"🛠️  Using tool: {tool_name}")

                        elif isinstance(block, ToolResultBlock):
                            if hasattr(block, "is_error") and block.is_error:
                                log(f"{Colors.RED}❌ Tool execution failed{Colors.NC}")
                            # Success is logged by the tool use blocks above

                        elif isinstance(block, TextBlock) and block.text.strip():
                            # Show Claude's reasoning more frequently for better visibility
                            text = block.text.strip()
                            claude_reasoning_count += 1

                            # Show every reasoning or important keywords (more verbose)
                            if claude_reasoning_count % 2 == 0 or any(
                                keyword in text.lower()
                                for keyword in [
                                    "analysis",
                                    "recommendations",
                                    "found",
                                    "creating",
                                    "complete",
                                    "examining",
                                    "checking",
                                    "writing",
                                    "generating",
                                ]
                            ):

                                if len(text) > 100:
                                    log(f"💭 Claude: {text[:100]}...")
                                else:
                                    log(f"💭 Claude: {text}")

        log(
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )

        # Generate final summary
        log(
            f"{Colors.GREEN}✅ AI agent context recommendations generation completed successfully!{Colors.NC}"
        )
        log("")
        log("📈 Final Results:")

        if tools_used:
            log(f"   - Tools used: {', '.join(sorted(tools_used))}")

        # Show detailed progress summary
        log("")
        log("📊 Analysis Statistics:")
        summary_lines = tracker.get_summary().split("\n")
        for line in summary_lines:
            log(f"   {line}")

        # Check if recommendations file was created
        if recommendations_file.exists():
            file_size = recommendations_file.stat().st_size
            log(f"   - Recommendations file: {recommendations_file}")
            log(f"   - File size: {file_size:,} bytes")

            # Read the recommendations file
            try:
                content = recommendations_file.read_text(encoding="utf-8")
                line_count = len(content.split("\n"))
                log(f"   - Content lines: {line_count}")

                # If GitHub Actions, write content to step summary
                if is_github_actions:
                    write_github_step_summary(content)
                    log("📱 AI agent context recommendations written to GitHub Actions step summary")
                else:
                    log("📄 Recommendations available in local file")

            except Exception as e:
                log(
                    f"{Colors.YELLOW}⚠️  Could not read recommendations file: {e}{Colors.NC}"
                )
                sys.exit(1)

        else:
            log(
                f"{Colors.YELLOW}⚠️  Warning: No recommendations file created: {recommendations_file}{Colors.NC}"
            )
            sys.exit(1)

    except CLINotFoundError as e:
        log(f"{Colors.RED}❌ Claude CLI not found: {e}{Colors.NC}")
        log("Make sure Claude CLI is properly installed in the container")
        sys.exit(1)
    except ProcessError as e:
        log(f"{Colors.RED}❌ Claude process error: {e}{Colors.NC}")
        sys.exit(1)
    except Exception as e:
        log(f"{Colors.RED}❌ Unexpected error during Claude execution: {e}{Colors.NC}")
        sys.exit(1)

    log("")
    log(f"📅 Completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log("")


if __name__ == "__main__":
    asyncio.run(main())
