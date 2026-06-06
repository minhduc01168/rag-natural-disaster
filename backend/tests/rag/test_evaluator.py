from app.rag.evaluation.evaluator import RagasEvaluator

def test_ragas_evaluator_empty():
    evaluator = RagasEvaluator(mock=True)
    results = evaluator.evaluate_qa([], [], [])
    assert results["faithfulness"] == 0.0
    assert results["answer_relevancy"] == 0.0

def test_ragas_evaluator_mock_success():
    evaluator = RagasEvaluator(mock=True)
    
    questions = ["Làm sao để sơ cứu?"]
    contexts = [["Hô hấp nhân tạo"]]
    answers = ["Bạn cần hô hấp nhân tạo"]
    
    results = evaluator.evaluate_qa(questions, contexts, answers)
    
    # Because we are using mock=True, it should return the fake scores
    assert results["faithfulness"] == 0.95
    assert results["answer_relevancy"] == 0.88
