from typing import Dict, Optional


class Wallet:
    """Wallet class, containing wallets information."""

    def __init__(self, client):
        self._client = client

    def begin_registration(
        self,
        wallet_type: str,
        public_address: str,
        user_id: Optional[str] = None,
    ):
        req = {
            'wallet_type': wallet_type,
            'public_address': public_address,
        }

        if user_id:
            req['user_id'] = user_id

        return self._client.api.post_request('auth/wallets/registrations/begin', body=req)

    def verify(
        self,
        wallet_type: str,
        public_address: str,
        signature: str,
        session_token: Optional[str] = None,
        session_jwt: Optional[str] = None,
        session_expires_in: Optional[int] = None,
    ):
        req = {
            'wallet_type': wallet_type,
            'public_address': public_address,
            'signature': signature,
        }

        if session_token:
            req['session_token'] = session_token
        if session_jwt:
            req['session_jwt'] = session_jwt
        if session_expires_in:
            req['session_expires_in'] = session_expires_in
        return self._client.api.post_request('auth/wallets/verify', body=req)
