from fastapi import APIRouter, HTTPException

router = APIRouter()

debates_info = {
    "data-analytics-in-agriculture": "農業資料分析：數位科技如何引領農業革新？",
    "iot-in-agriculture": "物聯網在智慧農業：連結土地與科技的未來",
    "automation-and-robotics": "自動化與機器人技術：重塑農業生產的未來",
    "drone-usage-for-crop-monitoring": "無人機在作物監測的應用：高空中的農業守望者",
    "smart-irrigation-systems": "智慧灌溉系統：節水高效率的農業灌溉解決方案",
    "ai-in-pest-and-disease-detection": "人工智慧在病蟲害檢測：提升預防與管理的智慧",
    "blockchain-for-food-traceability": "區塊鏈技術實現食品追溯：從田間到餐桌的透明之旅",
    "vertical-and-urban-farming": "垂直與城市農業：創新農業在都市中的實踐",
    "agri-tech-for-sustainable-farming": "促進永續農業的關鍵農業技術：為未來種下希望",
    "challenges-in-implementing-smart-agriculture": "實施智慧農業的挑戰：探索創新與永續性的平衡"
}


@router.get("/api/topic-info")
async def get_topic_info(topic_id: str):
    if topic_id and topic_id in debates_info:
        page_title = debates_info[topic_id]
        welcome_message = "農業是我們真正的財富，它是最有益、最自然的資源。"
        return {"page_title": page_title, "welcome_message": welcome_message}
    raise HTTPException(status_code=404, detail="Topic not found")