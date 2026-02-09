# Week 8 – System Fine-Tuning and Performance Optimization

## Overview

The main objective of Week 8 was to fine-tune and optimize the overall performance of the InventoryAI system.  
This phase focused on improving the efficiency of embedding generation, which plays a critical role in the Retrieval-Augmented Generation (RAG) pipeline.

---

## What Was Improved?

Previously, the system generated a new OpenAI embedding for every user query, even in cases where the exact same question had already been asked before.

This caused unnecessary overhead, including:

- increased response latency,
- a higher number of API calls,
- and greater operational cost.

To address this issue, a performance optimization was introduced.

---

## Embedding Cache Implementation

During this week, a caching mechanism was added to store previously computed embeddings.

With this improvement:

- if a user submits a repeated query,
- the system retrieves the stored embedding from cache,
- instead of generating a new one via the OpenAI API.

This significantly reduces redundant computation and improves system responsiveness.

---

## Results and Benefits

The optimization led to several measurable advantages:

- **Faster response times** for repeated or similar questions  
- **Reduced API load**, minimizing unnecessary embedding requests  
- **Lower operational costs**, due to fewer external API calls  
- **More stable and efficient RAG performance** overall  

---

## Summary

Week 8 focused on a practical fine-tuning task that resulted in real performance improvements for the InventoryAI chatbot system.  
By introducing embedding caching, the system became faster, more cost-efficient, and better optimized for repeated usage scenarios.

Further optimizations in future work may include advanced cache strategies, retrieval tuning, and deployment-level performance enhancements.
