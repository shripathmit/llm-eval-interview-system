"""Lab: A retrieval eval harness in miniature.

What this teaches: retrieval quality is measurable before any LLM is
involved. Give each query a known set of relevant documents, run the
retriever, and compute recall at k (did the relevant docs show up in
the top k) and MRR (how high the first relevant doc ranked). Every
retrieval change gets judged by these two numbers, not by vibes.

The retriever here is plain token overlap, so the lab runs anywhere.
Swap in embeddings and the metrics stay the same.

How to run: python3 retrieval_eval_harness.py
"""

CORPUS = {
    "d1": "Ground truth is the reference you score against: the label that says what the system should have produced.",
    "d2": "Cohen's kappa corrects percent agreement for the agreement two raters would reach by chance.",
    "d3": "A regression gate compares current eval scores to a baseline and blocks the release when a metric drops.",
    "d4": "Chunking splits documents into pieces small enough to embed and retrieve as focused snippets.",
    "d5": "Position bias means a judge prefers whichever answer is shown first, regardless of content.",
    "d6": "Failure bucketing groups failed items by cause so you fix the largest bucket first.",
    "d7": "A golden set is a fixed, human labeled set of items used to score every change the same way.",
    "d8": "Verbosity bias means a judge gives higher scores to longer answers with the same facts.",
}

QUERIES = [
    {"id": "q1", "text": "what do you score the system output against", "relevant": {"d1"}},
    {"id": "q2", "text": "agreement between two raters corrected for chance", "relevant": {"d2"}},
    {"id": "q3", "text": "block a release when a metric drops below baseline", "relevant": {"d3"}},
    {"id": "q4", "text": "judge prefers the first answer shown", "relevant": {"d5"}},
    {"id": "q5", "text": "fixed human labeled set used to score changes", "relevant": {"d7", "d1"}},
    {"id": "q6", "text": "how do you know the labels themselves are trustworthy", "relevant": {"d7"}},
]


def tokenize(text):
    return set(text.lower().strip(".,").split())


def retrieve(query_text, corpus, k):
    """Rank documents by token overlap with the query, return top k ids."""
    query_tokens = tokenize(query_text)
    scored = []
    for doc_id, doc_text in corpus.items():
        overlap = len(query_tokens & tokenize(doc_text))
        scored.append((doc_id, overlap))
    scored.sort(key=lambda pair: (-pair[1], pair[0]))
    return [doc_id for doc_id, _ in scored[:k]]


def recall_at_k(retrieved, relevant):
    if not relevant:
        return 0.0
    return len(set(retrieved) & relevant) / len(relevant)


def reciprocal_rank(retrieved, relevant):
    for rank, doc_id in enumerate(retrieved, start=1):
        if doc_id in relevant:
            return 1.0 / rank
    return 0.0


def main():
    k = 3
    recalls = []
    rrs = []

    print(f"Retrieval eval: {len(QUERIES)} queries, corpus of {len(CORPUS)} docs, k = {k}")
    print()
    for query in QUERIES:
        retrieved = retrieve(query["text"], CORPUS, k)
        recall = recall_at_k(retrieved, query["relevant"])
        rr = reciprocal_rank(retrieved, query["relevant"])
        recalls.append(recall)
        rrs.append(rr)
        print(f"  {query['id']}: retrieved {retrieved}  recall@{k} = {recall:.2f}  RR = {rr:.2f}")

    print()
    print(f"Mean recall@{k}: {sum(recalls) / len(recalls):.2f}")
    print(f"MRR:             {sum(rrs) / len(rrs):.2f}")
    print()
    print("Read recall first: a relevant doc outside the top k can never be")
    print("used by the generator. Read MRR second: it tells you how much")
    print("noise the generator has to read past to reach the good doc.")


if __name__ == "__main__":
    main()
