from fastapi import Header, HTTPException
from services.AuthService import AuthService


authService = AuthService()


async def verify_token(Authorization : str = Header(default='')):
    if not Authorization.split(' ')[0] == 'Bearer':
        raise HTTPException(status_code=401, detail="Token required for authentication")
    
    token = Authorization.split(' ')[1]
    
    payload = authService.decode_token_jwt(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
        
    return payload