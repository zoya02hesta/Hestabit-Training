class RAGEvaluator:

    def context_match_score(self, answer, context):
        if not context:
            return 0.0

        overlap = sum(1 for word in answer.split() if word in context)
        return overlap / max(len(answer.split()), 1)

    def hallucination_check(self, answer, context):
        return len(answer) > len(context) * 1.5

    def confidence_score(self, context_score, hallucination):
        if hallucination:
            return 0.3 * context_score
        return 0.7 + (0.3 * context_score)

    def evaluate(self, query, answer, context):

        context_score = self.context_match_score(answer, context)
        hallucination = self.hallucination_check(answer, context)
        confidence = self.confidence_score(context_score, hallucination)

        return {
            "context_score": context_score,
            "hallucination": hallucination,
            "confidence": round(confidence, 2)
        }