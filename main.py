from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import requests
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

app = FastAPI(
    title="Free Fire API",
    description="API wrapper for accessing Free Fire game data including player stats, account info, and guild information",
    version="1.0.0"
)

FREE_FIRE_API_BASE = "https://free-ff-api-src-5plp.onrender.com/api/v1"
HL_GAMING_BASE = "https://proapis.hlgamingofficial.com/main/games/freefire"

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Free Fire API - Python Edition",
        "version": "1.0.0",
        "endpoints": {
            "player_stats": "/api/player-stats",
            "account_info": "/api/account",
            "guild_info": "/api/guild",
            "craftland": "/api/craftland",
            "send_likes": "/api/send-likes",
            "docs": "/docs"
        },
        "supported_regions": ["IND", "BR", "SG", "RU", "ID", "TW", "US", "VN", "TH", "ME", "PK", "CIS", "BD"]
    }

@app.get("/api/player-stats")
async def get_player_stats(
    uid: str = Query(..., description="Player UID"),
    region: str = Query("IND", description="Region code (IND, BR, SG, RU, etc.)")
):
    """
    Get player statistics including matches, wins, kills, and K/D ratio
    
    - **uid**: Free Fire player UID
    - **region**: Region code (default: IND)
    """
    try:
        url = f"{FREE_FIRE_API_BASE}/playerstats"
        params = {"region": region.upper(), "uid": uid}
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch player stats: {str(e)}")

@app.get("/api/account")
async def get_account_info(
    uid: str = Query(..., description="Player UID"),
    region: str = Query("IND", description="Region code (IND, BR, SG, RU, etc.)")
):
    """
    Get account information including nickname, level, and profile details
    
    - **uid**: Free Fire player UID
    - **region**: Region code (default: IND)
    """
    try:
        url = f"{FREE_FIRE_API_BASE}/account"
        params = {"region": region.upper(), "uid": uid}
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch account info: {str(e)}")

@app.get("/api/guild")
async def get_guild_info(
    guild_id: str = Query(..., description="Guild ID"),
    region: str = Query("IND", description="Region code (IND, BR, SG, RU, etc.)")
):
    """
    Get guild/clan information including members, level, and details
    
    - **guild_id**: Free Fire guild ID
    - **region**: Region code (default: IND)
    """
    try:
        url = f"{FREE_FIRE_API_BASE}/guildInfo"
        params = {"region": region.upper(), "guildID": guild_id}
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch guild info: {str(e)}")

@app.get("/api/craftland")
async def get_craftland_profile(
    uid: str = Query(..., description="Player UID"),
    region: str = Query("IND", description="Region code (IND, BR, SG, RU, etc.)")
):
    """
    Get Craftland profile including maps and resources
    
    - **uid**: Free Fire player UID
    - **region**: Region code (default: IND)
    """
    try:
        url = f"{FREE_FIRE_API_BASE}/craftlandProfile"
        params = {"region": region.upper(), "uid": uid}
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch craftland profile: {str(e)}")

@app.post("/api/send-likes")
async def send_likes(
    uid: str = Query(..., description="Player UID to send likes to"),
    api_key: Optional[str] = Query(None, description="API key (optional, will use env var if not provided)")
):
    """
    Send likes to a Free Fire player (requires API key)
    
    - **uid**: Free Fire player UID to send likes to
    - **api_key**: API key (optional, uses FF_API_KEY env variable if not provided)
    
    Note: This endpoint requires a valid API key. Set FF_API_KEY in your environment variables.
    """
    key = api_key or os.getenv("FF_API_KEY")
    
    if not key:
        raise HTTPException(
            status_code=401, 
            detail="API key required. Provide via query parameter or set FF_API_KEY environment variable"
        )
    
    try:
        url = "https://ff-garena.run.place/sendLike"
        payload = {"uid": uid, "key": key}
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to send likes: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Free Fire API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
