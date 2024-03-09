# main.py 只放直接顯示於直接渲染的 API
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers.HomepageRouter import router as homepage_router
from app.routers.RegisterRouter import router as register_router
# from app.routers.LoginRouter import router as login_router
# from app.routers.LogoutRouter import router as logout_router
# from app.routers.VoteCountsRouter import router as vote_counts_router
from app.routers.ChooseTopicRouter import router as choose_topic_router
# from app.routers.DebateFormRouter import router as debate_form_router
# from app.routers.MyAccountRouter import router as my_account_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(homepage_router)
app.include_router(register_router)
# app.include_router(login_router)
# app.include_router(logout_router)
# app.include_router(vote_counts_router)
app.include_router(choose_topic_router)
# app.include_router(debate_form_router)
# app.include_router(my_account_router)

# @app.on_event("startup")
# async def startup_event():
    # initial invite token
    # from dependencies import get_register_service
    # init = get_register_service()
    # init._generate_initial_verify_code()



# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)