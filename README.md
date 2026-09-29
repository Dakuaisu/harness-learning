# Harness Learning: AI Harnesses Explained From Zero

This guide teaches you what an **AI harness** is, how one works inside, and how to build one yourself. It starts from the basics and uses plain English, analogies, and lots of diagrams. You don't need to know anything about AI to begin.

> **The one-sentence version:**
> An AI model on its own can only *read text and write text*. A **harness** is the program wrapped around the model that lets it *do things*: read files, run commands, search the web, remember what happened, and keep working step by step until a job is done.

```mermaid
flowchart LR
    You["🧑 You"] -->|"asks for a task"| H
    subgraph H["🛠️ THE HARNESS (a normal program)"]
        direction TB
        L["Loop: think → act → look → repeat"]
        T["Tools: files, terminal, web..."]
        C["Memory & context management"]
        S["Safety rules & permissions"]
    end
    H <-->|"text in / text out"| M["🧠 AI Model (the LLM)"]
    H <-->|"real actions"| W["🌍 The real world<br/>files, computers, internet"]
```

---

## 🗺️ Your learning path

Follow the parts in order. Each one builds on the one before.

```mermaid
flowchart TD
    A["PART 1: Prerequisites<br/>(the foundations)"] --> A1["1. Programs, APIs & JSON"]
    A1 --> A2["2. How an LLM actually works"]
    A2 --> A3["3. Talking to an LLM through an API"]
    A3 --> A4["4. Prompts, context & tokens"]
    A4 --> B["PART 2: The Harness<br/>(the main topic)"]
    B --> B1["5. What is a harness?"]
    B1 --> B2["6. Tools: giving the model hands"]
    B2 --> B3["7. The agent loop: the heartbeat"]
    B3 --> B4["8. Context engineering: managing memory"]
    B4 --> B5["9. Safety: permissions & sandboxes"]
    B5 --> B6["10. Power features: subagents, MCP, skills, hooks"]
    B6 --> B7["11. Real harnesses compared"]
    B7 --> C["PART 3: Build one yourself"]
    C --> C1["12. Build a mini harness in ~200 lines of Python"]
    C1 --> D["APPENDIX<br/>Glossary · Cheat sheet · Exercises"]

    style A fill:#dbeafe,stroke:#2563eb,color:#000
    style B fill:#dcfce7,stroke:#16a34a,color:#000
    style C fill:#fef3c7,stroke:#d97706,color:#000
    style D fill:#f3e8ff,stroke:#9333ea,color:#000
```

## 📚 Table of contents

### Part 1: Prerequisites
| # | Chapter | What you'll learn |
|---|---------|-------------------|
| 1 | [Programs, APIs & JSON](part-1-prerequisites/01-programs-apis-json.md) | What a program is, what an API is, what JSON looks like |
| 2 | [How an LLM works](part-1-prerequisites/02-how-llms-work.md) | Tokens, next-word prediction, and why the model "forgets" |
| 3 | [Calling an LLM API](part-1-prerequisites/03-calling-an-llm-api.md) | Messages, roles, system prompts, and your first API call |
| 4 | [Prompts, context & tokens](part-1-prerequisites/04-prompts-context-tokens.md) | The context window, cost, and writing good instructions |

### Part 2: The Harness
| # | Chapter | What you'll learn |
|---|---------|-------------------|
| 5 | [What is a harness?](part-2-harness/05-what-is-a-harness.md) | The big picture, and why "model + harness = agent" |
| 6 | [Tools](part-2-harness/06-tools.md) | How a model that only writes text can still "use" a tool |
| 7 | [The agent loop](part-2-harness/07-the-agent-loop.md) | The think → act → observe cycle that drives everything |
| 8 | [Context engineering](part-2-harness/08-context-engineering.md) | Fitting a big job into a limited memory |
| 9 | [Safety, permissions & sandboxes](part-2-harness/09-safety-permissions-sandboxes.md) | Keeping an AI that can run commands from causing damage |
| 10 | [Power features](part-2-harness/10-power-features.md) | Subagents, MCP, skills, hooks, planning, memory files |
| 11 | [Real harnesses compared](part-2-harness/11-real-harnesses.md) | Claude Code, Codex, Cursor and others, plus the other meanings of "harness" |

### Part 3: Build one
| # | Chapter | What you'll learn |
|---|---------|-------------------|
| 12 | [Build your own mini harness](part-3-build/12-build-your-own.md) | A working coding agent, explained line by line ([code](part-3-build/code/mini_agent.py)) |

### Appendix
- [Glossary](appendix/glossary.md): every term in plain English
- [Cheat sheet](appendix/cheat-sheet.md): the whole guide on one page
- [Exercises & next steps](appendix/exercises-and-next-steps.md): practice projects from easy to hard

---

## 💡 How to read this guide

- **Diagrams**: the flowcharts are written in [Mermaid](https://mermaid.js.org/). GitHub draws them as pictures automatically. In VS Code, install a "Markdown Preview Mermaid" extension to see them.
- **Code**: the examples are in Python because it reads almost like English. You don't need to run anything until Part 3.
- **"🔑 Key idea" boxes** mark the sentences to remember.
- **"🧪 Try it" boxes** are small exercises you can do.
- If a word is confusing, check the [Glossary](appendix/glossary.md).

Start here → [Chapter 1: Programs, APIs & JSON](part-1-prerequisites/01-programs-apis-json.md)
