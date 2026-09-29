"""
mini_agent.py: a tiny but real AI coding harness.

It has every core part of a harness from this guide:
  1. THE LOOP      think -> act -> observe, until the model is done   (Chapter 7)
  2. TOOLS         list / read / write / edit files, run commands     (Chapter 6)
  3. CONTEXT       system prompt + AGENTS.md/CLAUDE.md + history      (Chapter 8)
  4. SAFETY        folder jail, deny list, ask-before-acting          (Chapter 9)
  5. INTERFACE     a simple chat in your terminal                     (Chapter 11)

Run it:
    pip install anthropic
    export ANTHROPIC_API_KEY="sk-ant-..."
    python mini_agent.py                 # asks before every change
    python mini_agent.py --auto          # never asks (only use in a sandbox!)
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import anthropic

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
MODEL = "claude-opus-5-5"
MAX_STEPS = 30              # guard rail: most tool calls per task
MAX_TOOL_OUTPUT = 10_000    # guard rail: cut long tool output (characters)
COMMAND_TIMEOUT = 60        # guard rail: seconds before a command is killed
WORKSPACE = Path.cwd().resolve()   # the agent may only touch files in here
AUTO_APPROVE = "--auto" in sys.argv

# Commands we never run, even if the user says yes (a tiny deny list).
DENY_PATTERNS = ["rm -rf /", "sudo ", "mkfs", ":(){", "> /dev/sd", "curl ", "wget "]

client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from the environment


# ---------------------------------------------------------------------------
# PART 1: TOOLS. Plain Python functions, plus descriptions for the model.
# ---------------------------------------------------------------------------
def safe_path(path: str) -> Path:
    """Turn a path from the model into a real path, refusing to leave WORKSPACE."""
    full = (WORKSPACE / path).resolve()
    if full != WORKSPACE and WORKSPACE not in full.parents:
        raise ValueError(f"'{path}' is outside the project folder; access denied.")
    return full


def list_files(path: str = ".") -> str:
    folder = safe_path(path)
    entries = sorted(folder.iterdir())
    lines = [f"{'[dir] ' if e.is_dir() else '      '}{e.relative_to(WORKSPACE)}"
             for e in entries if e.name != ".git"]
    return "\n".join(lines) or "(empty folder)"


def read_file(path: str) -> str:
    return safe_path(path).read_text()


def write_file(path: str, content: str) -> str:
    file = safe_path(path)
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(content)
    return f"Wrote {len(content)} characters to {path}"


def edit_file(path: str, old_text: str, new_text: str) -> str:
    file = safe_path(path)
    text = file.read_text()
    count = text.count(old_text)
    if count == 0:
        raise ValueError("old_text was not found. Read the file first and copy the text exactly.")
    if count > 1:
        raise ValueError(f"old_text appears {count} times. Include more surrounding lines so it is unique.")
    file.write_text(text.replace(old_text, new_text))
    return f"Edited {path}"


def run_command(command: str) -> str:
    if any(bad in command for bad in DENY_PATTERNS):
        raise PermissionError("this command is blocked by the harness's safety rules.")
    result = subprocess.run(command, shell=True, cwd=WORKSPACE, capture_output=True,
                            text=True, timeout=COMMAND_TIMEOUT)
    return f"exit code: {result.returncode}\n--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"


# Name -> (function, does it change things and so needs approval?)
TOOL_FUNCTIONS = {
    "list_files":  (list_files,  False),
    "read_file":   (read_file,   False),
    "write_file":  (write_file,  True),
    "edit_file":   (edit_file,   True),
    "run_command": (run_command, True),
}

# What the MODEL sees. Descriptions are prompts: say what AND when.
TOOLS = [
    {
        "name": "list_files",
        "description": "List files and folders at a path in the project. Use this first to explore.",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "Folder path, e.g. '.' or 'src'"}},
            "required": [],
        },
    },
    {
        "name": "read_file",
        "description": "Read a text file's full contents. Always read a file before editing it.",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "File path, e.g. 'src/app.py'"}},
            "required": ["path"],
        },
    },
    {
        "name": "write_file",
        "description": "Create a new file, or completely replace an existing one. For small changes use edit_file instead.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string", "description": "The complete new file contents"},
            },
            "required": ["path", "content"],
        },
    },
    {
        "name": "edit_file",
        "description": "Replace one exact piece of text in a file. old_text must match the file exactly and appear only once.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "old_text": {"type": "string", "description": "Exact text to find"},
                "new_text": {"type": "string", "description": "Text to put in its place"},
            },
            "required": ["path", "old_text", "new_text"],
        },
    },
    {
        "name": "run_command",
        "description": "Run a shell command in the project folder, e.g. 'python hello.py' or 'pytest'. Use it to test your work.",
        "input_schema": {
            "type": "object",
            "properties": {"command": {"type": "string"}},
            "required": ["command"],
        },
    },
]


# ---------------------------------------------------------------------------
# PART 2: SAFETY. Ask the human before anything that changes the world.
# ---------------------------------------------------------------------------
def is_approved(name: str, tool_input: dict) -> bool:
    needs_approval = TOOL_FUNCTIONS[name][1]
    if not needs_approval or AUTO_APPROVE:
        return True
    print(f"\n  🙋 The agent wants to run {name} with:")
    print("    " + json.dumps(tool_input, indent=2)[:800].replace("\n", "\n    "))
    return input("  Allow? [y/N] ").strip().lower() == "y"


def run_tool(name: str, tool_input: dict) -> tuple[str, bool]:
    """Run one tool call. Returns (output text, is_error). Never crashes the loop."""
    if name not in TOOL_FUNCTIONS:
        return f"Error: there is no tool called '{name}'.", True
    if not is_approved(name, tool_input):
        return "The user declined this action. Ask them what they would like instead.", True
    try:
        output = TOOL_FUNCTIONS[name][0](**tool_input)
    except Exception as error:                      # turn failures into messages the model can read
        return f"Error: {type(error).__name__}: {error}", True
    if len(output) > MAX_TOOL_OUTPUT:               # keep the context small
        output = output[:MAX_TOOL_OUTPUT] + f"\n...[cut: output was {len(output)} characters]"
    return output, False


# ---------------------------------------------------------------------------
# PART 3: CONTEXT. Build the system prompt once, and keep it frozen.
# ---------------------------------------------------------------------------
def build_system_prompt() -> str:
    prompt = f"""You are a careful coding agent working in the folder {WORKSPACE}.
You can use tools to look at and change files and to run commands.

How to work:
- Explore first: list and read files before changing them.
- Make small, focused changes. Don't touch files unrelated to the task.
- After changing code, run it or run the tests to check that it works.
- When you are finished, give the user a short summary of what you did."""

    # Project memory: the harness loads these files so the model "remembers" project rules.
    for name in ("AGENTS.md", "CLAUDE.md"):
        memory_file = WORKSPACE / name
        if memory_file.exists():
            prompt += f"\n\n# Project notes from {name}\n{memory_file.read_text()}"
    return prompt


SYSTEM_PROMPT = build_system_prompt()


def close_open_tool_calls(messages: list, reason: str) -> None:
    """The API requires every tool_use to get a tool_result. If we stopped early,
    answer any unanswered requests so the history stays valid for the next task."""
    last = messages[-1]
    if last["role"] != "assistant":
        return
    pending = [b for b in last["content"] if b.type == "tool_use"]
    if pending:
        messages.append({"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": b.id, "content": reason, "is_error": True}
            for b in pending]})


# ---------------------------------------------------------------------------
# PART 4: THE AGENT LOOP. Think -> act -> observe, until done.
# ---------------------------------------------------------------------------
def run_agent(messages: list) -> None:
    for step in range(1, MAX_STEPS + 1):
        # THINK: send the whole history. The model has no memory of its own.
        response = client.beta.messages.create(
            model=MODEL,
            max_tokens=16000,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
            output_config={"effort": "high"},     # how hard to think: low / medium / high
            cache_control={"type": "ephemeral"},  # prompt caching: re-reading history is cheaper
            # If the model declines a request, retry it on a recommended fallback model.
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        )

        # Save the model's turn exactly as it came back (append-only history).
        messages.append({"role": "assistant", "content": response.content})

        for block in response.content:
            if block.type == "text" and block.text.strip():
                print(f"\n🤖 {block.text}")

        usage = response.usage
        print(f"   [step {step} · tokens in: {usage.input_tokens} new + "
              f"{usage.cache_read_input_tokens or 0} cached · out: {usage.output_tokens}]")

        # Is the model finished?
        if response.stop_reason == "refusal":
            print("\n🚫 The model declined this request.")
            return
        if response.stop_reason == "max_tokens":
            print("\n✂️  The reply was cut off (max_tokens). Try a smaller task.")
            close_open_tool_calls(messages, "Not run: the reply was cut off.")
            return
        if response.stop_reason != "tool_use":
            return                                   # end_turn: done!

        # ACT: run every tool the model asked for.
        results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"\n🔧 {block.name}({json.dumps(block.input)[:120]})")
                output, is_error = run_tool(block.name, block.input)
                print(("   ❌ " if is_error else "   ✅ ") + output[:200].replace("\n", " "))
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,         # match the result to its request
                    "content": output,
                    "is_error": is_error,
                })

        # OBSERVE: all results go back together in ONE user message, then loop.
        messages.append({"role": "user", "content": results})

    print(f"\n⛔ Stopped after {MAX_STEPS} steps (safety limit).")


# ---------------------------------------------------------------------------
# PART 5: INTERFACE. The outer loop: you <-> the agent.
# ---------------------------------------------------------------------------
def main() -> None:
    print(f"Mini agent working in {WORKSPACE}")
    print("Mode: " + ("AUTO (no approvals!)" if AUTO_APPROVE else "ask before changes"))
    print("Type a task, or 'quit' to exit.\n")

    messages = []    # the conversation history: the agent's short-term memory
    while True:
        try:
            task = input("\n🧑 You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if task.lower() in ("quit", "exit"):
            break
        if not task:
            continue
        messages.append({"role": "user", "content": task})
        try:
            run_agent(messages)
        except KeyboardInterrupt:
            print("\n⏸️  Interrupted.")
            close_open_tool_calls(messages, "Interrupted by the user.")
        except anthropic.APIError as error:
            print(f"\n⚠️  API error: {error}")
    print("Bye!")


if __name__ == "__main__":
    main()
