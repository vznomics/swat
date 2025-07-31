
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from .auth import authenticate_user
from .samba_control import list_shares, add_share, remove_share
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles

app = FastAPI()  # ✅ Only define this once!

# Mount static directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="swat_secret")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Routes
@app.get("/", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if authenticate_user(username, password):
        request.session["user"] = username
        return RedirectResponse("/dashboard", status_code=302)
    return RedirectResponse("/", status_code=302)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/")
    
    shares = list_shares()

    print("SHARES STRUCTURE >>>", shares)  # Debug line
    return templates.TemplateResponse("dashboard.html", {"request": request, "shares": shares})

@app.post("/add")
def add(request: Request, name: str = Form(...), path: str = Form(...), readonly: bool = Form(False)):
    add_share(name, path, readonly)
    return RedirectResponse("/dashboard", status_code=302)

@app.post("/remove")
def remove(request: Request, name: str = Form(...)):
    remove_share(name)
    return RedirectResponse("/dashboard", status_code=302)
