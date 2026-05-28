title: Chunking Strategies: Why How You Split Documents Matters More Than You Think
author: RuffRAGs Blog
date: 2026-03-22
category: Engineering
link: https://ruffraGs.ai/blog/chunking-strategies
---
Chunking Strategies: Why How You Split Documents Matters More Than You Think

Of all the decisions in a RAG pipeline, chunking gets the least attention and causes the most silent failures. The way you split documents controls what the retriever can find, what fits in the model's context window, and whether the answer the model generates is coherent or garbled. Getting chunking right is one of the highest-leverage improvements available to most RAG systems.

Why Chunking Exists

Embedding models and LLMs both have input length limits. A 50-page document cannot be embedded as a single vector — it would need to be truncated, and the resulting embedding would be a blurry average of every topic the document touches. Similarly, injecting entire long documents into the LLM prompt consumes the context window rapidly.

Chunking solves this by splitting documents into segments that fit within model limits and that are semantically coherent enough for a single embedding to represent meaningfully.

Fixed-Size Chunking

The simplest approach: split on character or token count with an overlap. This is what LangChain's `RecursiveCharacterTextSplitter` implements with its `chunk_size` and `chunk_overlap` parameters.

The overlap is essential. Without it, a sentence split across two chunks results in both chunks lacking context. An overlap of 10–20% of chunk size is a reasonable starting point.

The weakness of fixed-size chunking is that it is content-agnostic. A chunk boundary might land in the middle of a code block, a table row, or a numbered list, making both chunks partially incoherent.

Semantic Chunking

Instead of splitting on character count, semantic chunking splits on meaning. A common implementation embeds every sentence, then looks for points where adjacent sentence embeddings diverge significantly — a large cosine distance indicates a topic shift, which becomes a chunk boundary.

This produces chunks that are more semantically self-contained. The tradeoff is cost: you must embed every sentence before you know where to split, which is slow and expensive for large corpora. It also produces variable-size chunks, complicating batch processing.

Document-Structure-Aware Chunking

Many documents have inherent structure: headers, sections, paragraphs, code blocks, bullet lists. Structure-aware chunking respects these boundaries. Split on H2 headings rather than character count; keep a code block together rather than cutting through it; never split a table mid-row.

Markdown and HTML parsers make this straightforward for web content. For PDFs, extracting structure is harder but tools like pdfplumber and Unstructured.io provide reasonable results.

This approach requires document-type-specific logic but produces the most coherent chunks for structured documents.

Chunk Size Trade-offs

Larger chunks (800–1500 tokens) preserve more context and reduce the chance that the relevant sentence is split across a boundary. But large chunks embed as averages of many topics, making them harder to retrieve precisely, and they consume more of the context window per result.

Smaller chunks (128–400 tokens) embed more precisely and are cheaper to include in context. But they may lack enough surrounding context for the model to understand the answer they contain, and they are more likely to fragment multi-sentence explanations.

A practical starting point: 512–800 token chunks with 10% overlap. Measure retrieval recall and generation faithfulness, then adjust.

The Parent-Child Retrieval Pattern

One elegant solution to the size trade-off is parent-child chunking. Documents are split into small child chunks for precise retrieval. When a child chunk is retrieved, the system fetches its larger parent chunk (the full section or paragraph group) and injects that into the LLM context instead.

This gets the precision of small-chunk retrieval with the contextual richness of large-chunk generation. LangChain's `ParentDocumentRetriever` implements this pattern directly.

Metadata as a Retrieval Aid

Chunks should carry metadata from their source document: title, author, URL, section heading, publication date. This metadata serves two purposes: it lets the retriever filter by metadata (returning only chunks from documents published after a certain date, for example), and it lets the LLM cite the source accurately.

Always propagate metadata from document to chunk at split time. Reconstructing it afterward is painful.

Testing Your Chunking Strategy

The only reliable way to evaluate a chunking strategy is to measure retrieval recall on a golden question set before and after the change. Intuition about what "should" work is frequently wrong. Chunk size and overlap are hyperparameters; treat them like any other hyperparameter and tune them empirically.
