from fastapi import FastAPI, Query, HTTPException
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Zylo App ke liye CORS zaroori hai (warna browser block kar dega)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Website ko bypass karne ke liye headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://movieboxapp.in/",
    "Origin": "https://movieboxapp.in"
}

@app.get("/")
def home():
    return {"status": "Zylo MovieBox API is running successfully"}

@app.get("/search")
def search_movie(q: str = Query(..., description="Movie Name")):
    try:
        # MovieBox ka search API endpoint
        url = f"https://movieboxapp.in/wefeed-h5-bff/web/subject/search?q={q}&page=1&perPage=24"
        response = requests.get(url, headers=HEADERS, timeout=15)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="MovieBox API error")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stream/{subject_id}")
def get_stream(subject_id: str):
    try:
        # MovieBox ka stream/details API endpoint
        url = f"https://movieboxapp.in/wefeed-h5-bff/web/subject/play?subjectId={subject_id}"
        response = requests.get(url, headers=HEADERS, timeout=15)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Stream API error")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
