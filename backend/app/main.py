from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Database
from backend.app.database.database import Base, engine

# Create database tables BEFORE importing services
Base.metadata.create_all(bind=engine)

# Services
from backend.app.services.pipeline_service import generate_thought_leadership
from backend.app.services.chat_service import generate_reply


app = FastAPI()


app.mount(
    "/static",
    StaticFiles(directory="backend/app/static"),
    name="static"
)


templates = Jinja2Templates(
    directory="backend/app/templates"
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(data: ChatRequest):

    reply = generate_reply(data.message)

    return {
        "reply": reply
    }


class ContentRequest(BaseModel):
    topics: str
    audience: str


@app.post("/generate-content")
async def generate_content(data: ContentRequest):

    result = generate_thought_leadership(
        topics=data.topics,
        audience=data.audience
    )

    return result