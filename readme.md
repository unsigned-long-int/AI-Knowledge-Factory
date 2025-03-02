# AI-Knowledge-Factory

## Introduction
**AI-Knowledge-Factory** is an AI-powered knowledge collection and enrichment tool designed to dynamically gather, embed, and retrieve relevant information to enhance user queries with factual background context. The tool leverages a polymorphic implementation of the **Collector Protocol**, responsible for acquiring and updating the knowledge base, embedding the collected information, and efficiently retrieving relevant context using **Cosine Similarity**.

The core functionality of this tool involves:
1. **Dynamic Information Collection:** Collecting and embedding knowledge relevant to a user query.
2. **Efficient Knowledge Retrieval:** Computing similarity between stored embeddings and the query vector to retrieve the most relevant results.
3. **Query Enrichment:** Enhancing the user query with the retrieved knowledge base context to improve response accuracy.

## Motivation
Despite advancements in AI model fine-tuning, generating **factually accurate and precise responses** remains a challenge. Language models are inherently flexible and may sometimes:
- Forget or misremember details.
- Hallucinate responses.
- Provide generic answers instead of precise facts.

To ensure highly accurate responses, context must be explicitly included in the query prompt. However, manually sourcing and providing this context is inefficient due to:
- **Lack of direct access** to the necessary background information.
- **Token limitations**, restricting the amount of information that can be included in a prompt.

| **Model**      | **Token Limit**  | **Approx. Pages (~512 tokens/page)** |
|---------------|----------------|--------------------------------------|
| GPT-4o-mini  | 128,000 tokens  | ~384 pages                          |
| GPT-4o       | 128,000 tokens  | ~384 pages                          |

### **Proposed Solution**
To overcome these challenges, AI-Knowledge-Factory:
1. **Embeds both the user query and knowledge base context** for semantic similarity analysis.
2. **Invokes the appropriate `Collector Protocol` implementation** to dynamically fetch missing knowledge and update the knowledge base with embeddings.
3. **Computes the Cosine Similarity** between the user query embedding and stored knowledge base embeddings.
4. **Selects the top-N most relevant results** from the knowledge base to enrich the user query before processing.
5. **(Optional) Skips knowledge base updates** if the required knowledge is already embedded and available.

## Technical Implementation
### **Collector Protocol (Dynamic Knowledge Collection)**
The **Collector Protocol** is implemented using **duck typing**, allowing multiple interchangeable implementations. Each implementation should:
- Follow the defined **Collector Protocol** structure.
- Be annotated with `@append_metadata(description="<collector responsibility>")` to specify its role.
- Provide additional metadata via its `__doc__` string.

### **Knowledge Storage and Retrieval**
AI-Knowledge-Factory follows the **Ingestor and Retrieval Protocols** to store and access knowledge. By default:
- Knowledge is stored using **CSV-based ingestion and retrieval**.
- However, implementations can be extended to support alternative storage solutions such as **vector databases** (e.g., FAISS, Pinecone, Weaviate) or other custom storage mechanisms.
- The only requirement is that both ingestor and retriever implementations adhere to their respective protocols.

## Development Status
🚧 **This project is currently under active development.** 🚧  
While the core architecture is in place, additional refinements and optimizations are being implemented to enhance efficiency, scalability, and modularity.


## License
This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.



