title: ReAct: The Planning Pattern Behind Modern AI Agents
author: RuffRAGs Blog
date: 2026-02-07
category: Patterns
link: https://ruffraGs.ai/blog/react-planning-pattern
---
ReAct: The Planning Pattern Behind Modern AI Agents

When you ask a human expert to solve a complex problem, they don't just blurt out an answer. They think out loud — "Let me look that up," "Hmm, that changes things," "Okay, next I need to..." — and interleave thought with action. The ReAct (Reason + Act) prompting pattern brings this natural problem-solving rhythm to AI agents.

The Paper That Started It All

Introduced in the 2022 paper "ReAct: Synergizing Reasoning and Acting in Language Models" by Shunyu Yao et al., ReAct demonstrated that prompting LLMs to alternate between natural-language reasoning traces and concrete actions dramatically outperformed either reasoning-only (chain-of-thought) or action-only approaches on tasks like question answering, fact verification, and interactive decision-making.

The core insight: explicit thinking before acting reduces compounding errors. An agent that reasons about why it's taking an action is more likely to catch mistakes before they cascade.

The ReAct Loop

A ReAct agent's trace looks like this:

Thought: The user wants to know the side effects of Drug X. I should search the medical database first.
Action: search_database("Drug X side effects")
Observation: Drug X may cause nausea, headache, and elevated heart rate. Consult a physician if symptoms persist.
Thought: I have enough information to answer. The results are recent (2025) and from a trusted source.
Answer: Drug X may cause nausea, headache, and elevated heart rate...

Each Thought step is a free-form reasoning trace — not shown to the user, but logged internally. Each Action step invokes a tool. Each Observation is the tool's output fed back into context. This cycle repeats until the agent decides it has enough information to produce a final answer.

Why Explicit Reasoning Helps

Chain-of-thought research showed that forcing the model to "show its work" before answering improves accuracy. ReAct extends this: by writing down why it's choosing a particular action, the agent makes its decision process auditable and recoverable. If an action returns an unexpected result, the thought that follows can explicitly note the surprise and adjust the plan — rather than blindly continuing a broken trajectory.

ReAct vs. Other Planning Strategies

- Chain-of-Thought (CoT): reasoning only, no tool calls. Good for pure reasoning tasks; blind to the external world.
- ReAct: interleaved reasoning and action. Good for tasks requiring both reasoning and information gathering.
- Plan-and-Execute: generate the full plan upfront, then execute each step. More efficient for well-defined tasks; less adaptive to surprises.
- Reflexion: adds self-reflection and memory of past failures across multiple attempts. Excellent for iterative improvement tasks.
- Tree of Thoughts: explores multiple reasoning branches in parallel. Best for problems with many possible approaches.

ReAct is the most common pattern in production agents today because it balances adaptability, debuggability, and implementation simplicity.

Implementing ReAct in LangGraph

LangGraph makes the ReAct pattern explicit through its graph structure. The agent node generates thoughts and tool calls. Edge conditions route to tool nodes or to the output. Tool outputs flow back to the agent node, completing the loop. The graph topology literally encodes the ReAct cycle.

Adding a checkpointer means every step of the Thought-Action-Observation cycle is saved, giving you a complete audit trail. This is invaluable for debugging agents that went off the rails: you can replay the exact sequence of thoughts and observations that led to a wrong answer.

Limitations of ReAct

ReAct can get stuck in loops — repeatedly calling the same tool with slightly different queries when results are insufficient. Mitigation strategies include:

- Maximum step limits: abort after N action-observation cycles.
- Loop detection: compare recent observations; if they're similar, escalate to a different strategy.
- Human escalation: flag to a human when the agent has exceeded its confidence threshold.

Conclusion

ReAct is elegantly simple: think, act, observe, repeat. Yet this simple loop is the backbone of the most capable AI agents deployed today. By making reasoning explicit and tightly coupling it to real-world action, ReAct produces agents that are more accurate, more debuggable, and more trustworthy than their non-reasoning counterparts. If you're building agentic systems, ReAct is the first pattern to internalize.
