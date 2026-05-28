title: Evaluating RAG Systems: Beyond Vibes-Based Testing
author: RuffRAGs Blog
date: 2026-03-14
category: Evaluation
link: https://ruffraGs.ai/blog/evaluating-rag-systems
---
Evaluating RAG Systems: Beyond Vibes-Based Testing

Most RAG systems in production are evaluated the same way: a developer asks a few questions, the answers look reasonable, and the system ships. This approach fails silently. Real evaluation requires metrics, test sets, and systematic measurement of both the retrieval and generation components separately.

The Two-Stage Evaluation Problem

RAG has two failure modes, and they compound each other. Retrieval can fail by returning irrelevant documents, missing the right document entirely, or returning the right document but not ranking it highly enough to be included in the context window. Generation can fail by misreading a correctly retrieved document, hallucinating details, or answering a different question than the one asked.

Because the stages are coupled, a bad final answer might be the retrieval's fault, the generation's fault, or both. Evaluating only end-to-end accuracy hides which component needs fixing. Always evaluate retrieval and generation independently.

Retrieval Metrics

The standard retrieval metrics come from information retrieval literature.

Recall@k: of all the documents that contain the correct answer, how many are in the top-k results? High recall@k means the retriever is not missing relevant documents.

Precision@k: of the top-k returned documents, what fraction actually contain useful information? High precision means the retriever is not polluting the context with noise.

Mean Reciprocal Rank (MRR): measures how highly the first relevant document is ranked. A retriever that always puts the right document at position 1 scores 1.0; one that tends to bury it at position 5 scores 0.2.

To compute these, you need a labeled evaluation set: a list of questions, each paired with the documents that contain the correct answer. Building this set is work, but it is the only way to know if a change to your chunking strategy, embedding model, or retrieval method actually improved things.

Generation Metrics

Faithfulness: does the generated answer contain only information that is present in the retrieved documents? An answer that introduces facts not in the context is a hallucination. Faithfulness scores this on a 0–1 scale.

Answer relevance: does the answer address the question that was asked? A faithful but off-topic answer is still a bad answer.

Context utilization: did the model actually use the retrieved documents, or did it ignore them and rely on parametric knowledge? A model that ignores context defeats the purpose of RAG.

Frameworks like RAGAS automate these metrics using an LLM judge: a separate model reads the question, the retrieved context, and the generated answer, then scores each dimension. This is not perfect — LLM judges have biases — but it scales to thousands of examples where human annotation would not.

Building a Golden Dataset

A golden dataset is your ground truth: representative questions paired with reference answers and the documents expected to retrieve them. Building it is unglamorous but essential.

Practical approaches: export real user queries from logs (anonymized), have domain experts write questions targeting important content areas, or use an LLM to generate question-answer pairs from your documents and then human-review the outputs for quality.

Aim for 200–500 examples covering your main use cases. More is better, but a small high-quality set beats a large noisy one.

Regression Testing

Once you have a golden dataset and baseline metrics, treat them like a test suite. Every change to the pipeline — new embedding model, different chunk size, modified prompt, updated documents — should be measured against the baseline before deployment.

A retrieval change that improves recall@5 by 8% but drops faithfulness by 12% is a net loss. You cannot see this tradeoff without measurement.

Common Tools

RAGAS: open-source framework providing faithfulness, answer relevance, and context recall metrics out of the box.

Arize Phoenix: observability platform that traces RAG pipelines, surfaces retrieval quality per query, and stores evaluation results for trend analysis.

LangSmith: LangChain's evaluation and tracing tool; integrates directly with LangChain and LangGraph pipelines and supports custom evaluators.

Continuous evaluation — running your golden dataset against every build — is the difference between a RAG system that gets better over time and one that drifts in unknown directions.
