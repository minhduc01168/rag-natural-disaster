import asyncio
from app.rag.agents.router import RouterAgent

router = RouterAgent()
res = router.route_query("Thời tiết ở Đà Nẵng thế nào?")
print(res)
