title: The ReAct Pattern: How Agents Plan and Act Together
author: RuffRAGs Blog
date: 2026-02-07
category: Fundamentals
link: https://ruffraGs.ai/blog/react-planning-pattern
---
The ReAct Pattern: How Agents Plan and Act Together

If you have ever watched an AI agent work through a complex task step by step — searching, reasoning, searching again, then answering — you have seen the ReAct pattern in action. ReAct, short for Reasoning + Acting, is the most widely used framework for structuring how agents interleave thought and action. Understanding it demystifies how modern agents behave and helps you debug when they go wrong.

The Core Idea

Before ReAct, the dominant approach to agent planning was either pure chain-of-thought (reason first, act once) or pure action-then-observe loops with no explicit reasoning trace. ReAct interleaves both: the agent produces a thought, then an action, observes the result, produces another thought, and continues until it can produce a final answer.

A typical ReAct trace looks like this:

Thought: The user is asking about the latest version of the product. I should search the documentation for version information.
Action: search_docs("latest product version")
Observation: The search returned documentation stating the latest version is 3.2.1, released March 2026.
Thought: I now have the version. I can answer the user directly.
Answer: The latest version is 3.2.1, released in March 2026.

The thought steps are not just scaffolding — they improve answer quality. Models that externalize reasoning before acting make fewer errors than those that jump directly to action. The observation grounds the next reasoning step in real retrieved data rather than memory or invention.

Why Interleaving Matters

The alternative to interleaving is to generate a full plan upfront and then execute it. This works for simple, predictable tasks, but fails when early steps return unexpected results that should change the plan.

ReAct handles dynamic situations naturally. If a search returns no results, the next thought can revise the query. If a tool call fails, the reasoning step can choose a fallback. The plan adapts in real time to what the environment actually returns, rather than rigidly executing a plan formed before any information was retrieved.

ReAct in Practice

Most modern agent frameworks implement ReAct or a variant of it. LangChain's `create_react_agent` function builds a ReAct loop around any LLM and tool set. LangGraph gives you finer control by letting you implement the loop as an explicit graph with typed state, so you can intercept, modify, or branch the reasoning at any step.

The core loop in LangGraph looks like: a reasoning node that calls the LLM and produces either a tool call or a final answer; a conditional edge that routes to the tool execution node if a tool was called, or to the output node if the model is done; and a tool node that runs the tool, appends the observation to state, and routes back to the reasoning node.

This cycle runs until the model decides it has enough information to answer, or until a step limit is reached.

Failure Modes

ReAct agents can get stuck in reasoning loops. The model generates a thought, takes an action, gets a result, and then generates a nearly identical thought and repeats the same action — often because the observation did not resolve the uncertainty the model had. Setting a maximum step count prevents infinite loops; catching repetitive action patterns and surfacing them as an error is more informative.

Hallucinated observations are another failure mode. A model that is uncertain of its tool results may generate a plausible-sounding observation rather than reporting that the tool returned nothing useful. Separating tool output (injected by the framework) from model-generated text (the thought) makes this detectable: if the observation field was not populated by a real tool call, something went wrong.

Extending ReAct

ReAct is a baseline. More advanced patterns extend it:

Reflexion adds a self-evaluation step after each complete episode, where the agent critiques its own reasoning trace and stores lessons learned for the next attempt.

Tree-of-Thought runs multiple parallel ReAct traces and selects the best branch, useful when the correct action at a given step is uncertain.

Plan-and-Execute separates planning from execution: a planner agent generates a full step list, then executor agents carry out each step, potentially in parallel. This reduces latency for tasks where the steps are independent.

Each extension trades simplicity for capability. ReAct remains the right starting point for most tasks — add complexity only when you have measured that the simpler approach is insufficient.
