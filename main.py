from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import cases, tdabc, dashboards


app = FastAPI(
    title="TDABC + Patient Flow",
    version="1.0.0"
)

# ✅ ADD CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cases.router, prefix="/cases", tags=["Cases"])
app.include_router(tdabc.router, prefix="/tdabc", tags=["TDABC"])
app.include_router(dashboards.router, prefix="/dashboards", tags=["Dashboards"])
app.include_router(dashboards.router)

@app.get("/health")
def health():
    return {"status": "ok"}
