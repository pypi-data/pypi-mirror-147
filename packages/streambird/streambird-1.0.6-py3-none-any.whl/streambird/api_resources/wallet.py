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
    ):
        req = {
            'wallet_type': wallet_type,
            'public_address': public_address,
            'signature': signature,
        }

        return self._client.api.post_request('auth/wallets/verify', body=req)
