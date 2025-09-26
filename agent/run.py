#!/usr/bin/env python3
"""
Local runner for the Claude Context Optimizer Agent
For testing outside of Docker container
Requires Python 3.12+
"""

import asyncio
import os
import sys
from pathlib import Path

# Check Python version
if sys.version_info < (3, 12):
    print(f"❌ Error: Python 3.12+ is required. You have Python {sys.version}")
    print("Please install Python 3.12 and try again.")
    print("On macOS: brew install python@3.12")
    print("On Ubuntu: apt install python3.12")
    sys.exit(1)

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Run the agent locally"""

    # Set up paths for local testing
    workspace = Path.cwd()

    # Check if we're running from the agent directory
    if Path.cwd().name == "agent":
        # Running from agent folder, set workspace to parent
        workspace = Path.cwd().parent
        print(f"🏠 Running from agent folder, setting workspace to: {workspace}")
    else:
        # Running from project root or elsewhere
        print(f"🏠 Running from: {Path.cwd()}")
        print(f"📁 Workspace set to: {workspace}")

    # Override paths for local testing
    os.environ["WORKSPACE_DIR"] = str(workspace)

    # Check for API key
    if not os.getenv("CLAUDE_API_KEY"):
        print("❌ Error: CLAUDE_API_KEY environment variable is required")
        print("")
        print("Set it with:")
        print("  export CLAUDE_API_KEY=your_key_here")
        print("")
        print("Or create a .env file in the agent directory:")
        print("  echo 'CLAUDE_API_KEY=your_key_here' > .env")
        print("  source .env")
        sys.exit(1)

    print(f"🚀 Starting Claude Context Optimizer Agent...")
    print(f"🐍 Python version: {sys.version}")
    print(f"📦 Running in workspace: {workspace}")
    print("")

    # Import and run the main function
    try:
        from entrypoint import main as agent_main
        asyncio.run(agent_main())
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the agent directory and have installed dependencies:")
        print("  ./setup.sh")
        print("  source venv/bin/activate")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running agent: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()