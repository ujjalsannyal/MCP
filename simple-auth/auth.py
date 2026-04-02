from urllib import response
from urllib.request import Request

def valid_token(self, token: str) -> bool:
    # In a real application, you would validate the token properly
    if token.startswith("Bearer "):
        token = token[7:]  # Remove "Bearer " prefix
        return token == "valid-token123"
    return False


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        has_header = request.headers.get("Authorization")
        if not has_header:
            print("-> missing Authorization header")
            return response(content="Unauthorized", status_code=401)
        if not valid_token(has_header):
            print("-> invalid token")
            return response(content="Forbidden", status_code=403)
        
        print("-> valid token")
        return await call_next(request)
    
starlette_app.add_middleware(AuthMiddleware)