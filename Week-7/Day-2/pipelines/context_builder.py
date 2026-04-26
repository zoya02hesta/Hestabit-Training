class ContextBuilder:
    def __init__(self):
        pass

    def deduplicate(self, docs):
        seen = set()
        unique_docs = []

        for doc in docs:
            if doc not in seen:
                seen.add(doc)
                unique_docs.append(doc)

        return unique_docs

    def build_context(self, docs, max_length=1000):
        context = ""
        total_length = 0

        for doc in docs:
            if total_length + len(doc) > max_length:
                break

            context += doc + "\n"
            total_length += len(doc)

        return context