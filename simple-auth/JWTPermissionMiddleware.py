
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import datetime

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from passlib.context import CryptContext


# def validate_jwt(token: str) -> bool:
#     try:
#         decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
#         print("✅ Token is valid.")
#         print("Decoded claims:")
#         for key, value in decoded.items():
#             print(f"  {key}: {value}")
#         return True
#     except ExpiredSignatureError:
#         print("Token has expired")
#         return False
#     except InvalidTokenError:
#         print("Invalid token")
#         return False
    
# DON'T have the secret in the code like, this is for demonstration purposes only. Read it from a safe place.
SECRET_KEY = "your-secret-key-for-generating-jwt-tokens" # put this in env variable
REQUIRED_PERMISSION = "User.Read"
TOKEN_EXPIRATION_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

USERS_DB = {
    "alice": {
        "username": "alice",
        "hashed_password": pwd_context.hash("password123"),
        "role": "admin",
    },
    "bob": {
        "username": "bob",
        "hashed_password": pwd_context.hash("bobpass"),
        "role": "viewer",
    },
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = USERS_DB.get(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_jwt_token(username: str, permissions: list) -> str:
    payload = {
        "sub": username,
        "permissions": permissions,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRATION_MINUTES),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

class JWTPermissionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print(f"🔍 Checking permissions for path: {request.url.path} | request {request.url.path in ['/auth/token']}")
        if request.url.path in ['/auth/token']:
            return await call_next(request)
        
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse({"error": "Missing or invalid Authorization header"}, status_code=401)

        token = auth_header.split(" ")[1]
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return JSONResponse({"error": "Token expired"}, status_code=401)
        except jwt.InvalidTokenError:
            return JSONResponse({"error": "Invalid token"}, status_code=401)

        permissions = decoded.get("permissions", [])
        if REQUIRED_PERMISSION not in permissions:
            return JSONResponse({"error": "Permission denied"}, status_code=403)

        request.state.user = decoded
        return await call_next(request)

async def login(request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    user = authenticate_user(username, password)
    if not user:
        return JSONResponse({"error": "Invalid credentials"}, status_code=401)

    permissions = ["User.Read"] if user["role"] == "viewer" else ["User.Read", "User.Write"]
    token = create_jwt_token(user["username"], permissions)
    return JSONResponse({"access_token": token})