from fastapi import FastAPI
import requests
import time

app = FastAPI(
    title="Free Fire Global API",
    version="1.0"
)

API_BASE = "https://free-ff-api-src-5plp.onrender.com/api/v1"

REGIONS = [
    "IND","BR","ID","VN","TH","SG","ME","EU","NA","PK","CIS"
]


def find_region(uid):
    for region in REGIONS:
        try:
            r = requests.get(
                f"{API_BASE}/account",
                params={"uid": uid, "region": region},
                timeout=5
            )

            data = r.json()

            if data.get("result"):
                return region, data["result"]

        except:
            continue

    return None, None


@app.get("/")
def home():
    return {
        "status": "API Running",
        "usage": "/api/check?uid="
    }


@app.get("/api/check")
def check(uid: str):

    start = time.time()

    region, account = find_region(uid)

    if not region:
        return {
            "error": "UID not found"
        }

    stats = requests.get(
        f"{API_BASE}/playerstats",
        params={"uid": uid, "region": region}
    ).json()

    s = stats.get("result", {})

    result = {
        "basic_info": {
            "name": account.get("nickname"),
            "uid": uid,
            "level": account.get("level"),
            "region": region,
            "likes": account.get("likes"),
            "credit_score": account.get("creditScore"),
            "signature": account.get("signature")
        },

        "activity": {
            "version": account.get("releaseVersion"),
            "badge": account.get("badgeCnt"),
            "rank_br": s.get("rank"),
            "rank_cs": s.get("csRank"),
            "created_at": account.get("createAt"),
            "last_login": account.get("lastLoginAt")
        },

        "overview": {
            "avatar": account.get("avatarId"),
            "banner": account.get("bannerId"),
            "pin": account.get("pinId"),
            "skills": account.get("skills")
        },

        "pet": {
            "selected": account.get("pet", {}).get("isSelected"),
            "pet_id": account.get("pet", {}).get("id"),
            "exp": account.get("pet", {}).get("exp"),
            "level": account.get("pet", {}).get("level")
        }
    }

    process = round(time.time() - start, 2)

    return {
        "uid": uid,
        "region": region,
        "data": result,
        "process_time": f"{process}s"
    }
        "region": region,
        "result": result,
        "process_time": f"{end}s"
    }
