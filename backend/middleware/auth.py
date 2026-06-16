import os
from typing import Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient

from database import DbSession
from services.accounts.query_functions import get_user

security = HTTPBearer()

def get_current_auth_claims(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict[str, Any]:
    logto_endpoint = os.environ["LOGTO_ENDPOINT"]
    logto_api_resource = os.environ["LOGTO_API_RESOURCE"]

    token = credentials.credentials
    jwks_client = PyJWKClient(f"{logto_endpoint}/oidc/jwks")

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        return jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256", "ES384"],
            audience=logto_api_resource,
            issuer=f"{logto_endpoint}/oidc",
        )

    except jwt.PyJWTError as err:
        print(err)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )

def get_current_auth_sub(
    claims: dict[str, Any] = Depends(get_current_auth_claims),
) -> str:
    auth_sub = claims.get("sub")

    if not auth_sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token subject",
        )

    return auth_sub

def get_current_user(
    db: DbSession,
    auth_sub: str = Depends(get_current_auth_sub),
):
    user = get_user(auth_sub=auth_sub, db=db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user
