from fastapi import Security, HTTPException
from starlette.status import HTTP_403_FORBIDDEN
from fastapi.security.api_key import APIKeyHeader

api_key_header = APIKeyHeader(name = "auth_token", auto_error = False)
async def get_api_key(api_key_header: str = Security(api_key_header)):

    if api_key_header == "auth_key": # change to a proper hashed key-value pair, best practice is to use keyvault mechanism
        return api_key_header
    else:
        raise HTTPException(status_code = HTTP_403_FORBIDDEN, detail="Could not validate API KEY")