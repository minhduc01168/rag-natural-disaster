try:
    from ragas import evaluate
    from ragas.metrics import faithfulness, answer_relevancy
    from datasets import Dataset
except ImportError:
    evaluate = None

class RagasEvaluator:
    """
    Sử dụng RAGAS để đánh giá chất lượng của Agentic RAG.
    Các metrics được tập trung:
    - Faithfulness: Câu trả lời có dựa hoàn toàn vào context không?
    - Answer Relevancy: Câu trả lời có đúng trọng tâm câu hỏi không?
    """
    def __init__(self, mock: bool = False):
        self.mock = mock
        if not self.mock and evaluate is None:
            raise ImportError("Vui lòng cài đặt 'ragas' và 'datasets' để dùng tính năng đánh giá này.")

    def evaluate_qa(self, questions: list[str], contexts: list[list[str]], answers: list[str]) -> dict:
        """
        Đánh giá một tập hợp QA.
        """
        if not questions or not contexts or not answers:
            return {"faithfulness": 0.0, "answer_relevancy": 0.0}

        if self.mock:
            # Fake evaluation scores for testing/development
            return {"faithfulness": 0.95, "answer_relevancy": 0.88}

        # Format data cho RAGAS (HuggingFace Dataset format)
        data = {
            "question": questions,
            "contexts": contexts,
            "answer": answers
        }
        dataset = Dataset.from_dict(data)

        # Chạy evaluate với Ragas metrics
        result = evaluate(
            dataset,
            metrics=[faithfulness, answer_relevancy]
        )
        return dict(result)
