from fastapi import APIRouter, HTTPException

router = APIRouter()

debates_info = {
     "cancel-entrance-exam": "取消大學入學考試：解放還是風險？",
     "ban-smoking": "全面禁煙：公共健康的保護還是個人自由的侵犯？",
     "higher-taxes-for-rich": "對富人加稅：公平正義還是財富懲罰？",
     "same-sex-marriage": "同性結婚：尊重自由還是破壞社會結構？",
     "abolish-death-penalty": "廢除死刑：人道主義的勝利還是正義的失敗？",
     "global-education-system": "全球統一教育制度：文化同質化還是知識分享？",
     "social-media-regulation": "社群媒體監管：訊息過濾還是言論自由？",
     "gene-editing": "基因編輯技術：科學突破還是倫理危機？",
     "universal-basic-income": "全民基本收入：經濟解藥還是懶惰催化劑？",
     "penalties-for-polluters": "重罰污染企業：環境保護還是經濟壓力？"
}

@router.get("/api/topic-info")
async def get_topic_info(topic_id: str):
    if topic_id and topic_id in debates_info:
        page_title = debates_info[topic_id]
        welcome_message = "僅作為學術使用，請勿引起爭議..."
        return {"page_title": page_title, "welcome_message": welcome_message}
    raise HTTPException(status_code=404, detail="Topic not found")