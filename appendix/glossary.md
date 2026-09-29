# Glossary

[← Contents](../README.md)

Every term from the guide, in plain English. The chapter where it's explained is in brackets.

| Term | Plain-English meaning |
|------|----------------------|
| **Agent** | A model plus a harness that lets it take actions in a loop until a goal is reached. *Agent = Model + Harness.* [5] |
| **Agent loop** | The cycle: call the model → run the tools it asks for → send back results → repeat until it's done. [7] |
| **AGENTS.md / CLAUDE.md** | Text files of project rules and facts that the harness automatically loads into context. The agent's "long-term memory". [8] |
| **API** | A "menu" one program offers so other programs can ask it to do things. [1] |
| **API key** | A secret password that identifies you to an API (and bills you). Never share it or commit it. [1] |
| **Assistant (role)** | Messages written by the model. [3] |
| **Benchmark** | A fixed set of test tasks used to measure how good a model or agent is. [11] |
| **Cache / prompt caching** | The API remembers the unchanged start of your request, so re-sending it is cheaper and faster. [4, 8] |
| **Compaction** | Summarising a long conversation and replacing the old history with the summary, to free up context space. [8] |
| **Content block** | One piece of a message: a `text` block, a `tool_use` block, a `tool_result` block, a `thinking` block, etc. [3, 6] |
| **Context** | Everything the model sees in one request: system prompt, tools, history, files. [4] |
| **Context engineering** | The craft of putting the right information (and only that) into the model's context. [8] |
| **Context rot** | Model quality getting worse as the context gets bigger and noisier. [4] |
| **Context window** | The maximum number of tokens the model can look at in one request. Its "desk size". [2] |
| **Defence in depth** | Stacking several safety layers so one failure doesn't cause harm. [9] |
| **Effort** | A setting that controls how much the model thinks. Higher is smarter but slower and pricier. [12] |
| **Endpoint** | The web address an API request is sent to. [1] |
| **Eval harness** | A program that runs a model or agent on a benchmark and scores it. A different meaning of "harness". [11] |
| **Function** | A named, reusable chunk of code with inputs and an output. Every tool is a function. [1] |
| **Function calling** | Another name for tool use. [6] |
| **Guard rail** | A limit that stops runaway behaviour: max steps, timeouts, budgets. [7] |
| **Hallucination** | When a model confidently states something false. [2] |
| **Harness** | The software around a model that runs the loop, provides tools, manages context, enforces safety, and connects to the user. [5] |
| **Harness engineering** | Designing and tuning a harness (prompts, tools, context handling) to get better results from the same model. [11] |
| **Headless mode** | Running a harness from a script without an interactive screen. [10] |
| **Hook** | A script the harness runs automatically at a certain moment (before a tool, after a tool, at the end...). Always runs, unlike a prompt instruction. [10] |
| **HTTP** | The standard way programs send requests and responses over the internet. [1] |
| **Input schema** | A JSON Schema describing what inputs a tool accepts. [6] |
| **JSON** | A text format for structured data: `{}` objects, `[]` lists, `"key": value`. [1] |
| **Just-in-time loading** | Fetching information only when it's needed (via search/read tools) instead of loading everything at the start. [8] |
| **LLM** | Large Language Model: an AI that predicts the next token of text. Claude, GPT, Gemini, Llama... [2] |
| **max_tokens** | The most tokens the model may write in one reply. [3] |
| **MCP** | Model Context Protocol: an open standard for plugging outside tools and data into any harness. "USB-C for AI." [10] |
| **Messages** | The list of conversation turns (with roles) sent to the model. [3] |
| **Multi-agent** | Several agents working together, often an orchestrator plus workers. [10] |
| **Orchestrator** | An agent (or harness) that splits work and coordinates other agents. [10] |
| **Parallel tool calls** | The model asking for several tools in one reply. All results go back in one message. [6] |
| **Permission mode** | How much freedom the agent has: read-only, ask, auto-edit, or full auto. [9] |
| **Plan mode** | A mode where the agent can only read and must propose a plan before editing. [10] |
| **Prompt** | The text you write to ask the model something. [4] |
| **Prompt injection** | Malicious instructions hidden in content the agent reads (a web page, a file) that try to hijack it. [9] |
| **ReAct** | "Reason + Act": the think → act → observe pattern behind the agent loop. [7] |
| **Role** | Who "said" a message: `system`, `user`, or `assistant`. [3] |
| **Sandbox** | An isolated environment that limits what the agent's commands can reach. [9] |
| **SDK** | Software Development Kit: a library that makes an API easy to use from code. [3] |
| **Skill** | A folder of instructions (and scripts) that the harness loads only when a task needs it. [10] |
| **Slash command** | A saved prompt you trigger by typing `/name`. [10] |
| **Stateless** | Having no memory between requests. LLMs are stateless; harnesses add memory. [2] |
| **stop_reason** | Why the model stopped writing: `end_turn`, `tool_use`, `max_tokens`, `refusal`... [3] |
| **Subagent** | A helper agent with its own separate context, started by the main agent for a sub-job. [10] |
| **System prompt** | Standing instructions from the developer that set the model's role and rules. [3] |
| **Test harness** | Classic software term: code that runs other code's tests automatically. [11] |
| **Thinking** | Private reasoning a model can do before answering. [2] |
| **Token** | A chunk of text (≈ ¾ of a word) that models read and write. You pay per token. [2] |
| **Tool** | A function the harness lets the model request, described by name, description and input schema. [6] |
| **tool_result** | The block the harness sends back with a tool's output, matched by `tool_use_id`. [6] |
| **tool_use** | The block the model writes to request a tool. [6] |
| **User (role)** | Messages from the human, and also tool results sent by the harness. [3, 7] |

[← Contents](../README.md)
