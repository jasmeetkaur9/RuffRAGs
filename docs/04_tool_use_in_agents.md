title: Tool Use in AI Agents: Extending What Agents Can Do
author: RuffRAGs Blog
date: 2026-01-31
category: Fundamentals
link: https://ruffraGs.ai/blog/tool-use-in-agents
---
Tool Use in AI Agents: Extending What Agents Can Do

A language model on its own can reason, explain, and generate — but it cannot take actions in the world. It cannot check today's stock price, run a SQL query, send a message, or execute code. Tools bridge this gap. When an agent is given tools, it becomes capable of interacting with external systems and producing real-world effects.

What Is a Tool?

In the context of agentic AI, a tool is any callable function the model can invoke. The model does not execute the function itself — it generates a structured request describing which tool to call and with what arguments, and the orchestration framework executes it, then returns the result to the model.

From the model's perspective, using a tool looks like this: observe the task, decide a tool call is needed, generate the call as structured output (typically JSON), receive the result, incorporate the result into reasoning, and continue. This loop can repeat many times before a final answer is produced.

Standard Tool Categories

Web search tools let agents retrieve current information not in their training data. A user asking about today's news, a recent product release, or real-time pricing needs a search tool. Most production agents use a search API like Tavily, Bing Search, or a custom crawler.

Code execution tools allow agents to write and run code, then observe the output. This unlocks data analysis, mathematical computation, file processing, and automation tasks that language generation alone cannot perform. Tools like a Python REPL or a sandboxed code interpreter are common choices.

Database tools give agents read and write access to structured data. A SQL tool lets an agent query a relational database, filter results, and aggregate statistics. Paired with schema awareness, this makes agents capable of acting as natural-language database interfaces.

File system tools allow reading from and writing to files. Combined with code execution, this enables agents to process large documents, generate reports, and persist results for later use.

API tools are wrappers around external services — weather APIs, calendar services, CRM platforms, payment systems. Any service with an API can in principle be wrapped as an agent tool.

Defining Tools in LangChain

LangChain and LangGraph represent tools as Python functions decorated with metadata the model uses to decide when and how to call them. A simple tool definition looks like:

```python
from langchain_core.tools import tool

@tool
def get_word_count(text: str) -> int:
    """Count the number of words in the provided text."""
    return len(text.split())
```

The docstring becomes the tool description the model reads. The function signature becomes the argument schema. The model uses both to decide whether this tool is appropriate for the current task.

For more complex tools — those with multiple arguments, optional parameters, or complex return types — you define a Pydantic schema explicitly and register it alongside the function.

Tool Selection and Planning

When an agent has many tools available, the model must decide which tool to call for each step. This decision is part of the model's reasoning process and is influenced by the tool descriptions, the current task, and any planning the model has done.

Tool descriptions are therefore not mere documentation — they are prompt content that directly affects behavior. Vague descriptions lead to wrong tool selection. Specific, accurate descriptions improve reliability. Describe what the tool does, what its inputs represent, and when it should be used versus alternatives.

Avoiding Tool Misuse

Tools with side effects — sending emails, writing to databases, calling payment APIs — need guardrails. A model that misunderstands the task might call a destructive tool when a read-only one would suffice.

Common mitigations: require human approval before any irreversible tool call, use separate read and write tools rather than a single combined tool, and log all tool invocations for audit. Rate limits and permission scopes at the API level provide a backstop even when the agent logic is wrong.

The Principle of Least Privilege

Give the agent only the tools it actually needs for the task at hand. An agent answering questions about documentation does not need file-write access. An agent generating reports does not need email-send access. Narrowing the tool surface reduces the blast radius of any error or manipulation.

This is the single most effective safety measure for tool-using agents, and it costs nothing to implement at design time.
