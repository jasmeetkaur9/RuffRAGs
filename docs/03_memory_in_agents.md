title: Memory in AI Agents: How Agents Remember Across Time
author: RuffRAGs Blog
date: 2026-01-24
category: Fundamentals
link: https://ruffraGs.ai/blog/memory-in-agents
---
Memory in AI Agents: How Agents Remember Across Time

Every conversation you have with an AI agent begins, by default, with a blank slate. The model has no recollection of what you discussed yesterday, last week, or five minutes ago in a different session. For simple chatbots this is acceptable. For agents expected to build on prior context, learn user preferences, or complete multi-session tasks, it is a critical limitation. Memory systems solve this.

The Four Types of Agent Memory

Researchers and practitioners generally distinguish four memory types, borrowing loosely from cognitive science.

Sensory memory is the raw input the agent receives right now — the current message, any attached files, the latest tool output. It exists only for the current processing step and is not persisted. Every agent has this by default.

Working memory is the agent's active context window. It holds the current conversation, recent tool results, and any information explicitly passed into the prompt for this session. It is fast and directly accessible, but it is bounded by the model's context limit and does not survive session restarts.

Episodic memory stores records of past interactions — what was said, what actions were taken, what the outcomes were. Implemented as a retrievable log, it lets an agent recall that "last Tuesday the user asked about deployment and we resolved it by updating the config." RAG over a conversation history database is the most common implementation.

Semantic memory stores general facts and knowledge, separate from any specific interaction. This is where a RAG knowledge base fits: indexed documents about your product, domain knowledge, reference material. The agent retrieves from this store when it needs background information rather than personal history.

Short-Term vs Long-Term

A practical way to think about memory is along a single axis: does it survive when the session ends?

Short-term memory lives in the context window. It is immediate, zero-latency, and costs nothing extra to access — the model simply reads from the prompt. But it is ephemeral. When the session ends, it is gone. And for long conversations, the context window fills up, forcing you to summarize or truncate earlier turns.

Long-term memory is stored externally — in a database, a vector store, or a key-value store — and retrieved as needed. It survives restarts and scales to arbitrary history length. The tradeoff is retrieval latency and the need to decide what to store and when.

Most production agents use both: short-term for the current conversation and long-term for history that spans sessions or exceeds context limits.

Implementation Patterns

The simplest long-term memory implementation is a flat conversation log. At the end of each session, serialize the messages to disk or a database. At the start of the next session, load the last N messages back into context. This works well when sessions are short and users pick up where they left off.

For longer histories, retrieval-based memory is more scalable. Embed each conversation turn and store it in a vector database. When the agent starts a new session, retrieve the turns most semantically similar to the current query rather than loading everything. The agent gets relevant history without blowing the context budget.

Summarization is another option. At the end of each session, or periodically within a long session, ask the model to produce a compressed summary of what was discussed. Store the summary, discard the raw turns. Future sessions load the summary instead of the full history. This loses detail but preserves the gist at a fraction of the token cost.

Memory in LangGraph

LangGraph, the most widely used agentic framework in Python, handles short-term memory through its state schema — a typed dictionary that persists across nodes in the graph. Long-term memory across sessions is handled via checkpointers: pluggable backends (SQLite, PostgreSQL, Redis) that serialize and restore the full graph state at any step.

This means you can pause an agent mid-task, shut down the process, restart it, and resume from exactly where it left off. For long-running tasks that span hours or days, this is essential.

What to Store and What to Forget

Not everything is worth remembering. Storing every agent action fills your database with noise that degrades retrieval quality. A useful heuristic: store outcomes and decisions, not process. The fact that the agent searched three times before finding the right document is process. The fact that the user prefers concise answers is an outcome worth keeping.

Designing a good memory system means thinking about what a new session actually needs to know to serve the user well — and being selective about everything else.
