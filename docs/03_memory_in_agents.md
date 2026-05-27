title: Memory in Agentic AI: How Agents Remember What Matters
author: RuffRAGs Blog
date: 2026-01-24
category: Architecture
link: https://ruffraGs.ai/blog/memory-in-agents
---
Memory in Agentic AI: How Agents Remember What Matters

Every meaningful conversation builds on what came before. You don't re-introduce yourself every time you speak to a colleague. Yet most early AI chatbots treated each message as if it were the first — a blank slate with no history, no context, no continuity. Agentic AI systems fix this through memory architectures that mirror how humans store and retrieve information.

The Four Tiers of Agent Memory

Researchers and practitioners commonly describe agent memory in four tiers, each with different scope and persistence:

1. Working Memory (In-Context)
The agent's "active thought" — everything currently in the LLM's context window. Fast, precise, but limited in size and duration. When the conversation ends or the context overflows, working memory evaporates.

2. Episodic Memory (Conversation History)
A log of past interactions, stored externally and loaded back into context when needed. A thread-based JSON store, a Redis cache, or a relational database can serve this role. The agent can look up "what did the user say last Tuesday?" and re-inject that history into its working context.

3. Semantic Memory (Knowledge Base / RAG)
Long-term factual knowledge indexed in a vector store. This is where RAG lives. The agent doesn't memorize facts — it knows how to retrieve them. Semantic memory scales to billions of documents and stays current as documents are added or updated.

4. Procedural Memory (System Prompt / Fine-Tuning)
How the agent behaves — its personality, policies, and skills. Encoded in the system prompt or baked into model weights via fine-tuning. This is the most stable tier; it changes rarely and deliberately.

Checkpointers: Persistent State in LangGraph

LangGraph's InMemorySaver (and its persistent siblings like SqliteSaver or PostgresSaver) act as the agent's episodic memory. Every time the agent processes a message, the full state — messages, variables, tool outputs — is saved under a thread ID. On the next turn, the checkpointer loads that state, and the agent picks up exactly where it left off.

This is powerful for multi-session workflows. A customer-support agent can remember that the user already tried rebooting, that their account is on the Pro tier, and that they were frustrated last week — all without the user repeating themselves.

The Context Window Bottleneck

LLMs have a finite context window. As conversation history grows, older messages must be truncated or summarized. Smart memory systems handle this by:

- Summarizing older turns into a compact digest.
- Pruning irrelevant messages while retaining key facts.
- Moving important details into semantic memory (the vector store) so they can be retrieved on demand rather than kept in context at all times.

This "working set" approach mirrors how human attention works: we hold a few things in mind right now and rely on long-term memory for the rest.

Session Management in Practice

In the RuffRAGs architecture, each conversation is keyed by a session_id. The run_chat function loads the thread's history from disk, streams the agent's response with LangGraph, appends the new messages, and saves everything back to a JSON file. This gives users continuity across browser sessions or app restarts — the kind of experience that feels natural and human.

Memory and Privacy

Persistent memory raises important privacy considerations. Users may not want their queries stored indefinitely. Best practices include:

- Explicit opt-in for conversation history.
- Clear retention policies (e.g., delete threads after 90 days).
- User-controlled memory deletion ("forget everything I've said").
- Encryption at rest for stored threads.

Designing memory with privacy in mind from the start is far easier than retrofitting it later.

Conclusion

Memory is what transforms a stateless Q&A system into a genuine assistant. By layering in-context working memory, persistent episodic history, and a retrieval-backed semantic store, agentic AI systems can maintain context across time, recall relevant facts on demand, and provide the kind of coherent, continuous experience that users actually want. Getting memory right is one of the most impactful architectural decisions you'll make when building an AI agent.
