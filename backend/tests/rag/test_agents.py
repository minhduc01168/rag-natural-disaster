from app.rag.agents.router import RouterAgent
from app.rag.agents.synthesis_agent import SynthesisAgent

def test_router_agent():
    router = RouterAgent()
    
    assert router.route_query("thời tiết hôm nay thế nào") == "weather"
    assert router.route_query("dự báo bão số 3") == "weather"
    assert router.route_query("bản đồ ngập lụt ở đâu") == "geo"
    assert router.route_query("sạt lở ở miền núi") == "geo"
    assert router.route_query("làm sao để hô hấp nhân tạo") == "knowledge"
    assert router.route_query("cách chằng chống nhà cửa") == "knowledge"

def test_synthesis_agent_routing():
    # Test end-to-end routing without diving deep into implementation
    agent = SynthesisAgent()
    
    res_weather = agent.process_query("thời tiết hà nội")
    assert res_weather["route_taken"] == "weather"
    assert "Thời tiết tại" in res_weather["answer"]
    
    res_geo = agent.process_query("bản đồ rủi ro lào cai")
    assert res_geo["route_taken"] == "geo"
    assert "Cảnh báo" in res_geo["answer"]
    
    res_knowledge = agent.process_query("cách sơ cứu")
    assert res_knowledge["route_taken"] == "knowledge"
