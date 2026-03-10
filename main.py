from fastapi import FastAPI
import requests
import time

app = FastAPI(
    title="Free Fire Global API",
    version="1.0"
)

API_BASE = "https://free-ff-api-src-5plp.onrender.com/api/v1"

# tất cả region
REGIONS = [
    "IND","BR","ID","VN","TH","SG","ME","EU","NA","PK","CIS"
]


# tìm region của UID
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
def root():
    return {
        "message": "Free Fire Global API running",
        "usage": "/api/check?uid="
    }


@app.get("/api/check")
def check(uid: str):

    start = time.time()

    region, account = find_region(uid)

    if not region:
        return {"error": "UID not found"}

    stats = requests.get(
        f"{API_BASE}/playerstats",
        params={"uid": uid, "region": region}
    ).json()

    s = stats.get("result", {})

    result = f"""
┌ THÔNG TIN CƠ BẢN
├─ Tên: {account.get("nickname")}
├─ UID: {uid}
├─ Cấp độ: {account.get("level")}
├─ Khu vực: {region}
├─ Lượt thích: {account.get("likes")}
├─ Điểm uy tín: {account.get("creditScore")}
└─ Chữ ký: {account.get("signature")}

┌ HOẠT ĐỘNG TÀI KHOẢN
├─ Phiên bản gần nhất: {account.get("releaseVersion")}
├─ Huy hiệu BP hiện tại: {account.get("badgeCnt")}
├─ Rank BR: {s.get("rank")}
├─ Rank CS: {s.get("csRank")}
├─ Ngày tạo: {account.get("createAt")}
└─ Đăng nhập gần nhất: {account.get("lastLoginAt")}

┌ TỔNG QUAN
├─ Avatar ID: {account.get("avatarId")}
├─ Banner ID: {account.get("bannerId")}
├─ Pin ID: {account.get("pinId")}
└─ Kỹ năng được trang bị: {account.get("skills")}

┌ THÚ CƯNG
├─ Đang dùng?: {account.get("pet", {}).get("isSelected")}
├─ ID thú cưng: {account.get("pet", {}).get("id")}
├─ Kinh nghiệm: {account.get("pet", {}).get("exp")}
└─ Cấp độ: {account.get("pet", {}).get("level")}
"""

    end = round(time.time() - start, 2)

    return {
        "uid": uid,
        "region": region,
        "result": result,
        "process_time": f"{end}s"
    }
