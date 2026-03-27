# AI Agent (ReAct Pattern)

## What is an AI Agent?

An AI Agent is an LLM that can **think, act, and observe in a loop** to autonomously solve tasks. It uses **tools** (functions, APIs) to interact with the real world.

**Agent = LLM (brain) + Tools (hands) + Loop (decision cycle) + Memory (context)**

> Tools + system prompt alone is NOT an agent. Without an **execution loop**, it's just a tool-aware LLM.

## ReAct Pattern

ReAct = **Re**asoning + **Act**ing

```
plan → action → observe → output
```

| Step | What happens | Who |
|------|-------------|-----|
| **Plan** | Understand query, decide what to do, pick a tool | LLM |
| **Action** | Call the selected tool with input | Code |
| **Observe** | Feed tool output back to LLM | Code → LLM |
| **Output** | Return final human-readable answer | LLM |

## Agent Components

1. **Reasoning** — LLM decides what to do next
2. **Tools** — registered Python functions (`get_weather`, `run_command`)
3. **Execution Loop** — runs repeatedly until task is done (the core of an agent)
4. **Observation handling** — tool output fed back into LLM as context
5. **Memory** — chat history / past steps stored in `messages` list

## How the Loop Works

```
outer loop: take user input
    inner loop:
        call LLM → get JSON response
        if "plan"   → log thinking, continue
        if "action" → call tool, inject output as "observe", continue
        if "output" → print answer, break
```

- **Outer loop** — keeps taking user queries
- **Inner loop** — agent keeps running until it produces a final output
- Tool results go back as user messages with `step: "observe"`

## Key Implementation Details

- **Tool registry** — functions stored in a dict, called dynamically by name
- **JSON mode** — `response_format={"type": "json_object"}` forces parseable output
- **System prompt** — defines steps, lists tools, enforces JSON format, gives examples
- **One step per LLM call** — agent does one action at a time, not multiple

## Things to Remember

1. Agent = tools + prompt + **execution loop** + reasoning cycle
2. Without the loop, it's just a chatbot with tool descriptions
3. The LLM decides which tool to call and when to stop
4. Tool output is injected back as a user message (not hardcoded)
5. Any Python function can be a tool if registered in the dict
