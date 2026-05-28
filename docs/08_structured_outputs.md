title: Structured Outputs: Getting Reliable JSON from LLMs
author: RuffRAGs Blog
date: 2026-02-18
category: Engineering
link: https://ruffraGs.ai/blog/structured-outputs
---
Structured Outputs: Getting Reliable JSON from LLMs

One of the most common frustrations when integrating LLMs into production systems is getting the model to return data in a consistent, parseable format. A model that sometimes returns valid JSON and sometimes wraps it in markdown fences — or adds an apologetic preamble — breaks downstream pipelines. Structured outputs are the solution.

The Problem with Freeform Generation

LLMs are trained on human text, and human text is not a strict schema. When you ask a model to "return a JSON object with fields name and score," you might get:

- A perfect JSON blob
- JSON wrapped in triple-backtick code fences
- A sentence followed by JSON
- JSON with extra fields the model decided to add
- Prose describing what it would have put in the JSON

Each of these requires different parsing logic. At scale, every parsing failure is a dropped result, a user-facing error, or a silent data corruption.

Constrained Decoding

The modern fix is constrained decoding: at the token-generation level, the model is forced to only emit tokens that could continue a valid JSON string. Libraries like Outlines and llama.cpp's grammar mode implement this by tracking a finite-state machine over the JSON grammar and masking any token that would produce an invalid continuation.

The result is that the model cannot produce malformed JSON — not because you asked it to, but because invalid tokens are zeroed out before sampling. This is fundamentally different from prompt engineering; the constraint is enforced at the probability distribution, not in the instruction.

OpenAI's Structured Outputs (available since GPT-4o) uses the same principle under the hood. You pass a JSON Schema, and the API guarantees the response matches it exactly.

Tool / Function Calling as a Structured Output Primitive

Function calling (or tool use) is the most widely available form of structured output. When you define a tool schema, the model generates a structured call to that tool rather than freeform text. The LLM provider enforces that the generated JSON matches the schema.

This is especially useful in agentic systems, where the model needs to decide which tool to call and with what parameters. The tool schema doubles as a structured output schema.

Pydantic and Instructor

For Python developers, the Instructor library wraps any OpenAI-compatible API and uses function calling under the hood to return validated Pydantic models. You define your output type as a Pydantic class and Instructor handles retries automatically: if the model returns something that fails Pydantic validation, it sends the validation error back to the model and asks it to correct the output.

LangChain exposes similar functionality through `.with_structured_output()`, which wraps the same mechanism for any supported model.

Designing Good Output Schemas

A few schema design patterns that reduce errors:

Use enums over freeform strings when the set of valid values is finite. "status": "active" | "inactive" | "pending" is far more reliable than "status": string.

Keep nesting shallow. Deep nested objects give the model more opportunities to drop a field or misplace a brace.

Add descriptions to every field. Most providers pass field descriptions to the model as part of the schema prompt. A field named "conf" is ambiguous; "conf" with description "confidence score between 0 and 1" is not.

Avoid optional fields unless truly necessary. Every optional field the model might omit is a potential null-pointer in your downstream code.

When Structured Outputs Fall Short

Constrained decoding ensures format validity, not semantic correctness. A model can return perfectly valid JSON where every field is the wrong value. Validation is a floor, not a ceiling. You still need evaluation pipelines to catch semantic errors that structure constraints cannot catch.
