from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import joblib
import textwrap
from sklearn.metrics.pairwise import cosine_similarity

# ---------- FastAPI Setup ----------
app = FastAPI()
from starlette.middleware.sessions import SessionMiddleware
import csv, os

app.add_middleware(SessionMiddleware, secret_key="SUPER_SECRET_KEY")
USER_CSV = "users.csv"

def load_users():
    users={}
    if not os.path.exists(USER_CSV): return users
    with open(USER_CSV, newline='') as f:
        r=csv.DictReader(f)
        for row in r: users[row['username']]=row['password']
    return users

def save_users(users):
    with open(USER_CSV,'w',newline='') as f:
        w=csv.writer(f); w.writerow(["username","password"])
        for u,p in users.items(): w.writerow([u,p])

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    users = load_users()
    if username in users and users[username] == password:
        request.session["user"] = username
        return RedirectResponse("/", status_code=302)

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Invalid username or password"}
    )


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=302)

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    users = load_users()

    if username in users:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "User already exists!"}
        )

    users[username] = password
    save_users(users)

    return templates.TemplateResponse(
        "register.html",
        {"request": request, "success": "Account created successfully! Please login."}
    )


@app.get("/forgot_password", response_class=HTMLResponse)
async def forgot_page(request: Request):
    return templates.TemplateResponse("forgot_password.html", {"request": request})

@app.post("/forgot_password")
async def forgot(request: Request, username: str = Form(...), new_password: str = Form(...)):
    users = load_users()

    if username not in users:
        return templates.TemplateResponse(
            "forgot_password.html",
            {"request": request, "error": "User not found"}
        )

    users[username] = new_password
    save_users(users)

    return templates.TemplateResponse(
        "forgot_password.html",
        {"request": request, "success": "Password updated successfully! Please login."}
    )

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ---------- Load Health Model ----------
health_vectorizer = joblib.load("health_policy_vectorizer.pkl")
health_data = joblib.load("health_policy_tfidf_matrix.pkl")
health_tfidf = health_data["matrix"]
health_df = health_data["df"]

# ---------- Load Education Model (unchanged) ----------
edu_vectorizer = joblib.load("policy_vectorizer.pkl")
edu_data = joblib.load("policy_tfidf_matrix.pkl")
edu_tfidf = edu_data["matrix"]
edu_df = edu_data["df"]

# ---------- Search Function ----------
def search_policies(query: str, policy_type: str = "health", top_k: int = 3):
    if policy_type == "health":
        vec, matrix, data_df = health_vectorizer, health_tfidf, health_df
    else:
        vec, matrix, data_df = edu_vectorizer, edu_tfidf, edu_df

    query_vec = vec.transform([query.lower()])
    sims = cosine_similarity(query_vec, matrix).flatten()
    top_idx = sims.argsort()[::-1][:top_k]

    results = []
    for idx in top_idx:
        row = data_df.iloc[idx]
        results.append({
            "title": str(row["title"]),
            "summary": str(textwrap.shorten(row.get("full_text", ""), width=250, placeholder="...")),
            "score": float(round(float(sims[idx]), 3))
        })
    return results

# ---------- Routes ----------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    if "user" not in request.session:
        return RedirectResponse("/login",302)
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health", response_class=HTMLResponse)
async def health_page(request: Request):
    return templates.TemplateResponse("health.html", {"request": request, "results": []})

@app.post("/search/health", response_class=HTMLResponse)
async def health_search(request: Request, query: str = Form(...)):
    try:
        results = search_policies(query, policy_type="health")
        return templates.TemplateResponse("health.html", {
            "request": request,
            "results": results,
            "query": query
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return HTMLResponse(f"<h1>Template Rendering Error</h1><pre>{traceback.format_exc()}</pre>")

# Education routes remain unchanged
@app.get("/education", response_class=HTMLResponse)
async def education_page(request: Request):
    return templates.TemplateResponse("education.html", {"request": request, "results": None})

@app.post("/search/education", response_class=HTMLResponse)
async def education_search(request: Request, query: str = Form(...)):
    results = search_policies(query, policy_type="education")
    return templates.TemplateResponse("education.html", {"request": request, "results": results, "query": query})
