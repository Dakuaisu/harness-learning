# Chapter 5: What Is an AI Harness?

[← Chapter 4](../part-1-prerequisites/04-prompts-context-tokens.md) · [Contents](../README.md) · Next: [Chapter 6: Tools →](06-tools.md)

You've finished the prerequisites. Now for the main topic.

---

## 5.1 Where the word comes from

A **harness** for a horse is the set of straps that connects the horse to a cart. The horse supplies the **power**. The harness **directs** that power into useful work: pulling the cart in the right direction without running off.

```mermaid
flowchart LR
    H["🐎 Horse<br/>raw power"] --- HA["🪢 Harness<br/>connects & directs"] --- C["🛒 Cart<br/>useful work gets done"]
    M["🧠 AI Model<br/>raw intelligence"] --- AH["🛠️ AI Harness<br/>connects & directs"] --- W["📁 Real work<br/>files edited, bugs fixed"]
```

An **AI harness** is the same idea:
- The **model** supplies intelligence (reasoning, writing, planning).
- The **harness** connects that intelligence to the real world and keeps it on track.

> 🔑 **Definition:** An **AI harness** is the software around an AI model that runs it in a loop, gives it tools, manages what it sees (context), enforces safety rules, and connects it to the user and the outside world.

Other names you'll hear for the same thing or close to it: **agent harness**, **agent scaffold**, **agent framework**, **agent runtime**, **orchestrator**.

---

## 5.2 Another analogy: engine vs. car

```mermaid
flowchart TB
    subgraph CAR["🚗 THE CAR = AN AGENT"]
        E["⚙️ Engine = the MODEL<br/>(makes the power)"]
        subgraph REST["Everything else = the HARNESS"]
            S["🛞 Steering & wheels = tools"]
            D["📊 Dashboard = user interface"]
            B["🛑 Brakes & seatbelts = safety & permissions"]
            F["⛽ Fuel gauge = context/token tracking"]
            G["🧭 GPS = planning & to-do lists"]
        end
    end
```

An engine sitting on the garage floor is powerful but useless. You can't drive it anywhere. A car without an engine goes nowhere either. You need both.

> 🔑 **The famous equation:**
> # Agent = Model + Harness

Same engine, different car, very different experience. The same AI model can feel brilliant in one harness and clumsy in another. That's why companies invest so much in their harnesses.

---

## 5.3 What a harness is responsible for

Here's the full map of a harness's jobs. Each one gets its own chapter.

```mermaid
mindmap
  root((AI Harness))
    The Loop
      Call the model
      Read stop_reason
      Repeat until done
    Tools
      Describe tools to the model
      Run tool calls
      Return results
    Context
      Keep history
      Build the system prompt
      Load project notes
      Summarise when full
    Safety
      Ask permission
      Sandbox
      Block dangerous commands
    Interface
      Terminal / IDE / web / chat
      Show progress
      Let user interrupt
    Extras
      Subagents
      MCP connections
      Skills
      Hooks
      Planning / to-do lists
```

In one table:

| Job | Question it answers | Chapter |
|-----|---------------------|---------|
| **The loop** | "How does the model keep working without me pressing enter every step?" | 7 |
| **Tools** | "How does a text-only model *do* things?" | 6 |
| **Context management** | "How does it remember, and not run out of room?" | 8 |
| **Safety** | "How do I stop it from breaking things?" | 9 |
| **Interface** | "How do I see what it's doing and step in?" | 11 |
| **Extras** | "How does it handle big, complex jobs?" | 10 |

---

## 5.4 Chatbot vs. agent: what the harness changes

Let's compare what happens when you ask *"Fix the failing test in my project"*.

### In a plain chatbot (thin harness)

```mermaid
sequenceDiagram
    participant U as You
    participant C as Chatbot
    U->>C: "Fix the failing test in my project"
    C-->>U: "I can't see your project. Please paste the test and the code."
    U->>C: (pastes code)
    C-->>U: "Try changing line 12 to ..."
    Note over U: You copy the fix, run the test yourself...
    U->>C: "Still fails, here's the error"
    C-->>U: "Ah, then try ..."
```

**You** are the harness. You're doing the copying, pasting, running, and reporting back.

### In an agent harness

```mermaid
sequenceDiagram
    participant U as You
    participant H as Harness
    participant M as Model
    participant PC as Your computer
    U->>H: "Fix the failing test in my project"
    H->>M: task + tool list
    M-->>H: tool_use: run "pytest"
    H->>PC: runs pytest
    PC-->>H: "1 failed: test_login"
    H->>M: here's the output
    M-->>H: tool_use: read "auth.py"
    H->>PC: reads file
    PC-->>H: file contents
    H->>M: here's the file
    M-->>H: tool_use: edit "auth.py" line 12
    H->>PC: edits the file
    H->>M: done
    M-->>H: tool_use: run "pytest"
    H->>PC: runs pytest
    PC-->>H: "all passed ✅"
    H->>M: here's the output
    M-->>H: end_turn: "Fixed! The bug was..."
    H-->>U: "Fixed! The bug was..."
```

**The harness** does the copying, pasting, running and reporting, automatically, in a loop. You just gave the goal.

> 🔑 **Key idea:** The harness turns a model from something that **talks about** work into something that **does** work.

---

## 5.5 The whole thing in one picture

Keep this diagram in mind for the rest of the guide. Every later chapter zooms into one box.

```mermaid
flowchart TB
    U["🧑 User"] <-->|"task / updates / approvals"| UI

    subgraph HARNESS["🛠️ HARNESS"]
        UI["Interface<br/>(terminal, IDE, web)"]
        LOOP["🔁 Agent Loop<br/>(Ch. 7)"]
        CTX["📋 Context Builder<br/>system prompt + history + memory<br/>(Ch. 8)"]
        PERM["🛡️ Permission Check<br/>(Ch. 9)"]
        TOOLS["🔧 Tool Runner<br/>(Ch. 6)"]
        UI <--> LOOP
        LOOP --> CTX
        LOOP --> PERM --> TOOLS
        TOOLS -->|results| LOOP
    end

    CTX -->|"request"| MODEL["🧠 Model API"]
    MODEL -->|"response: text or tool_use"| LOOP
    TOOLS <--> WORLD["🌍 Files · Terminal · Web · Databases · Other apps"]
```

## ✅ Chapter summary

- A **harness** connects a model's intelligence to real work and keeps it on track, like a horse harness or a car around an engine.
- **Agent = Model + Harness.** The same model behaves very differently in different harnesses.
- A harness handles: **the loop, tools, context, safety, interface, and extras**.
- Without a harness, *you* do the running around. With one, the harness does it.

[← Chapter 4](../part-1-prerequisites/04-prompts-context-tokens.md) · [Contents](../README.md) · Next: [Chapter 6: Tools →](06-tools.md)
