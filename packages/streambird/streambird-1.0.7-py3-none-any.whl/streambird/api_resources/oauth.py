from typing import Dict, Optional


class OAuth:
    """OAuth class, containing oauth information."""

    def __init__(self, client):
        self._client = client

    def verify(
        self,
        token: str,
        session_type: Optional[str] = None,
        session_token: Optional[str] = None,
        session_jwt: Optional[str] = None,
        session_expires_in: Optional[int] = None,
    ):
        req = {
            'token': token,
        }

        if session_type:
            req['session_type'] = session_type
        if session_expires_in:
            req['session_expires_in'] = session_expires_in
        if session_token:
            req['session_token'] = session_token
        if session_jwt:
            req['session_jwt'] = session_jwt

        return self._client.api.post_request('auth/oauth/verify', body=req)
