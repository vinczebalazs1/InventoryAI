# InventoryAI – Intelligent Inventory Management with RAG-based Chatbot

## Overview

InventoryAI is a Retrieval-Augmented Generation (RAG) based chatbot system designed for intelligent inventory management.  
The main goal of the project is to enable natural language querying over structured inventory databases, providing accurate, real-data-grounded responses instead of relying solely on the static knowledge of large language models.

This project was developed as a university semester project and will be extended further in the second semester.

---

## Motivation

Large Language Models (LLMs) are powerful tools for natural language understanding and generation, but they have a fundamental limitation:  
their knowledge is static and cannot directly access real-time or organization-specific databases.

Retrieval-Augmented Generation (RAG) addresses this issue by combining:

- semantic retrieval from external knowledge sources  
- and response generation using an LLM

This approach significantly reduces hallucinations and improves factual accuracy.

---

## Project Objectives

The primary objectives of InventoryAI are:

- building an AI-powered assistant for inventory lookup  
- enabling semantic search across inventory records  
- integrating vector-based retrieval with GPT-based response generation  
- providing an interactive user interface for querying

Example user questions:

- “Where is the MATLAB software located?”
- “Which site has the Cisco CallManager license?”
- “Is there any available Xilinx software?”

---

## System Architecture

The solution follows a standard RAG pipeline:

1. **User Query Input**
2. **Embedding Generation** (OpenAI embedding models)
3. **Vector Similarity Search** in Qdrant
4. **Context Construction** from retrieved inventory entries
5. **Answer Generation** with GPT models using retrieved context

---

## Data Preparation

The inventory dataset was originally provided in Excel format.

Preprocessing steps included:

- normalization of text fields (lowercasing, whitespace cleanup)
- validation of duplicate and missing values
- exploratory analysis of frequent locations and devices
- transforming each inventory record into a unified textual representation

---

## Embedding Models Tested

Multiple OpenAI embedding models were evaluated:

- `text-embedding-3-small`
- `text-embedding-3-large`
- `text-embedding-ada-002`

Each model produced vectors stored in separate Qdrant collections due to differing dimensions (1536 vs 3072).

### Conclusion

`text-embedding-3-large` provided the best retrieval precision, capturing subtle semantic differences in inventory-related queries.

---

## Vector Database: Qdrant

Qdrant was used as the vector search backend.

Stored data included:

- embedding vectors
- full metadata payload (location, inventory ID, item name)

This enabled both high-quality retrieval and traceable responses.

---

## LLM Evaluation

Several OpenAI chat models were compared:

- GPT-4o-mini
- GPT-4-turbo
- GPT-5

Evaluation criteria:

- language quality
- relevance and completeness
- response structure
- ability to use retrieved context effectively

GPT-5 delivered the most accurate and context-aware answers, therefore it was chosen for the final system.

---

## User Interface

A Streamlit-based web application was developed with:

- chat-style interaction
- input sanitization (basic XSS protection)
- fast query-response cycle

---

## Performance Optimization

To reduce latency and API costs:

- embedding requests were cached using `@lru_cache`
- repeated queries became significantly faster
- overall user experience improved without reducing accuracy

---

## Future Work

Planned improvements for the next semester include:

- authentication and role-based access control
- enhanced UI features
- further retrieval optimization
- deployment-ready infrastructure

---

## Tech Stack

- Python
- OpenAI API (Embeddings + GPT)
- Qdrant Vector Database
- LangChain
- Streamlit

---

## Author

This public version of the project was created and maintained by:

- Balázs Iván Vincze

---

## Original Team Project

The full InventoryAI system was developed as part of a university semester project together with:

- Ágota Vass  
- Roland Kuskó  

Mentor: Mark Bence Szigeti  

This repository includes only my personal contributions.


---

## Disclaimer

The original repository was maintained privately by the project mentor.  
This public version contains only the components and code written by me for portfolio and educational purposes.

All data used in this repository is synthetic and provided only for demonstration purposes.  
It does not contain any real university or institutional inventory records.
