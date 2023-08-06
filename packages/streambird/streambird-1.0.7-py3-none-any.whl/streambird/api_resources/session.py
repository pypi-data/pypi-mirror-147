from typing import Dict, Optional


class Session:
    """Session class, containing sessions information."""

    def __init__(self, client):
        self._client = client

    def verify(
        self,
        session_token: Optional[str] = None,
        session_jwt: Optional[str] = None,
        session_expires_in: Optional[int] = None,
    ):
        req = {}

        if session_token:
            req['session_token'] = session_token
        if session_jwt:
            req['session_jwt'] = session_jwt
        if session_expires_in:
            req['session_expires_in'] = session_expires_in

        return self._client.api.post_request('auth/sessions/verify', body=req)

    def list(
        self,
        user_id: str,
    ):
        params = {
            'user_id': user_id,
        }

        return self._client.api.get_request('auth/sessions/list', params=params)

    def delete(
        self,
        session_token: Optional[str] = None,
        session_jwt: Optional[str] = None,
        session_id: Optional[str] = None,
    ):
        req = {}
        if session_token:
            req['session_token'] = session_token
        if session_jwt:
            req['session_jwt'] = session_jwt
        if session_id:
            req['session_id'] = session_id

        return self._client.api.delete_request('auth/sessions/delete', body=req)
