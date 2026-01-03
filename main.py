from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from api.routes import cases, tdabc, dashboards

app = FastAPI(
    title="TDABC + Patient Flow",
    version="1.0.0"
)

# Allow frontend → backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(cases.router, prefix="/cases", tags=["Cases"])
app.include_router(tdabc.router, prefix="/tdabc", tags=["TDABC"])
app.include_router(dashboards.router, prefix="/dashboards", tags=["Dashboards"])

# Serve frontend directory
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Redirect root to frontend dashboard
@app.get("/")
def root():
    return RedirectResponse(url="/frontend/index.html")

@app.get("/health")
def health():
    return {"status": "ok"}
