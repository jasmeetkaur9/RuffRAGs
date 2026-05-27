title: Tool Use in AI Agents: Giving LLMs Hands
author: RuffRAGs Blog
date: 2026-01-31
category: Architecture
link: https://ruffraGs.ai/blog/tool-use-in-agents
---
Tool Use in AI Agents: Giving LLMs Hands

A language model without tools is like a brilliant expert locked in a room with no phone, no computer, and no pen — full of knowledge but unable to act. Tool use is the capability that unlocks agency: it gives the LLM hands to reach out and interact with the world. Understanding how tool use works is fundamental to building effective AI agents.

What Is a Tool?

In the context of LLM agents, a tool is any function or service the model can call to perform an action or retrieve information outside its own weights. Common examples include:

- Web search — query the internet for real-time information
- Code interpreter — execute Python, analyze data, generate plots
- Database query — run SQL against a structured data source
- File system access — read, write, and search files
- REST API calls — interact with external services (weather, calendar, CRM)
- Calculator — perform precise arithmetic (LLMs are notoriously unreliable at math)
- Vector store search — the retrieval half of a RAG pipeline
- Email/calendar — send messages and schedule events

The LLM doesn't execute tools itself. It generates a structured request (a tool call) specifying which tool to invoke and with what arguments. The orchestration framework intercepts this, runs the actual function, and returns the result as a new message in the conversation.

How Tool Calling Works

Modern LLMs (GPT-4o, Claude 3, Llama 3+) have native support for structured tool calls. The developer registers tools as JSON schemas describing the function name, parameters, and types. The model sees these schemas in its system prompt and knows it can produce a tool-call output in addition to regular text.

A simplified flow:

1. User: "What's the stock price of AAPL right now?"
2. LLM: [generates tool_call] { "tool": "web_search", "query": "AAPL stock price today" }
3. Framework: executes the search, retrieves results
4. LLM: [sees results in context, generates] "Apple (AAPL) is currently trading at $213.45."

The model reasons about which tools to call, in what order, and how to interpret their outputs. This is the core reasoning loop of an agent.

Tool Selection and Chaining

Sophisticated agents chain tools dynamically. A research task might unfold as:

1. Call web_search to find relevant articles.
2. For each article, call fetch_url to retrieve full text.
3. Call summarize to condense each article.
4. Call write_file to save a combined report.

The agent decides this sequence by reasoning about what information it has, what it still needs, and which tools can bridge the gap. This emergent planning behavior — not hardcoded by the developer — is what makes tool-using agents genuinely powerful.

Parallel Tool Calls

Modern agent frameworks support calling multiple tools simultaneously when the calls are independent. Fetching three web pages in parallel rather than sequentially can cut latency by 60% or more. LangGraph and similar frameworks expose this natively, letting the agent indicate which tool calls can fan out concurrently.

Safety and Sandboxing

Giving an AI agent access to tools introduces real risk. An agent with filesystem write access can delete files. One with email access can send messages on your behalf. Best practices for safe tool use include:

- Minimal privilege: give agents only the tools they actually need.
- Sandboxed execution: run code in isolated containers (Docker, Firecracker) with no network access.
- Human approval gates: require user confirmation before irreversible actions (deleting files, sending emails, making purchases).
- Rate limiting: cap how many tool calls an agent can make per session to limit runaway loops.
- Audit logging: record every tool call and its output for post-hoc review.

Tool Use in the RuffRAGs Context

RuffRAGs uses a focused tool set: vectorstore similarity search is the primary "tool" wrapped inside the dynamic prompt middleware. The agent receives retrieved document chunks as part of its system prompt and responds from that grounded context. This narrow tool surface — retrieval only, no external APIs — is a deliberate safety choice for a domain-specific Q&A assistant.

Conclusion

Tools are what separate a language model from an AI agent. By giving LLMs the ability to search the web, run code, query databases, and interact with external services, tool use transforms passive text generation into active problem-solving. As the catalog of available tools grows and models become better at selecting and chaining them, the scope of tasks that agents can handle autonomously will only expand.
