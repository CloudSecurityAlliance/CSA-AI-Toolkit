# Resources

## [Notes on how to use LLMs in your product](https://lethain.com/mental-model-for-how-to-use-llms-in-products/)

* Even the most expensive LLMs are not that expensive for B2B usage. Even the cheapest LLM is not that cheap for Consumer usage
* For example, with a high-level view of RAG, some folks might think they can replace their search technology (e.g. Elasticsearch) with RAG, but that’s only true if your dataset is very small and you can tolerate much higher response latencies.
* The challenge, from my perspective, is that most corner-cutting solutions look like they’re working on small datasets while letting you pretend that things like search relevance don’t matter, while in reality relevance significantly impacts quality of responses when you move beyond prototyping (whether they’re literally search relevance or are better tuned SQL queries to retrieve more appropriate rows). This creates a false expectation of how the prototype will translate into a production capability, with all the predictable consequences: underestimating timelines, poor production behavior/performance, etc.

## [These are not product reviews](https://youtu.be/bnA08Wwh9v4)

* Talks about the economics of producing certain kinds of content and why AI is needed, also the challenges and problems inherent
