from typing import Dict, Optional


class Totp:
    """Otp class, containing otps information."""

    def __init__(self, client):
        self._client = client

    def create(
        self,
        user_id: str,
    ):
        req = {
            'user_id': user_id,
        }
        return self._client.api.post_request('auth/totps/create', body=req)
    
    def recovery_codes(
        self,
        user_id: str,
    ):
        req = {
            'user_id': user_id,
        }
        return self._client.api.post_request('auth/totps/recovery_codes', body=req)

    def verify(
        self,
        totp: str,
        user_id: str,
        session_token: Optional[str] = None,
        session_jwt: Optional[str] = None,
        session_expires_in: Optional[int] = None,
        device_fingerprint: Optional[Dict] = None,
    ):
        req = {
            'totp': totp,
            'user_id': user_id,
        }

        if device_fingerprint:
            req['device_fingerprint'] = device_fingerprint
        if session_expires_in:
            req['session_expires_in'] = session_expires_in
        if session_token:
            req['session_token'] = session_token
        if session_jwt:
            req['session_jwt'] = session_jwt
        return self._client.api.post_request('auth/totps/verify', body=req)

    def recovery(
        self,
        recovery_code: str,
        user_id: str,
        session_token: Optional[str] = None,
        session_jwt: Optional[str] = None,
        session_expires_in: Optional[int] = None,
        device_fingerprint: Optional[Dict] = None,
    ):
        req = {
            'recovery_code': recovery_code,
            'user_id': user_id,
        }

        if device_fingerprint:
            req['device_fingerprint'] = device_fingerprint
        if session_expires_in:
            req['session_expires_in'] = session_expires_in
        if session_token:
            req['session_token'] = session_token
        if session_jwt:
            req['session_jwt'] = session_jwt
        return self._client.api.post_request('auth/totps/recovery', body=req)


