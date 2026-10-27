from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"title": "CineMatch", "movie_title": ""},
    )

@app.post("/", response_class=HTMLResponse)
async def recommend(
    request: Request,
    movie_title: str = Form(...),
    content_type: str = Form("movie"),
):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "CineMatch",
            "movie_title": movie_title.strip(),
            "content_type": content_type,
        },
    )


app.mount("/static", StaticFiles(directory="app/static"), name="static")
