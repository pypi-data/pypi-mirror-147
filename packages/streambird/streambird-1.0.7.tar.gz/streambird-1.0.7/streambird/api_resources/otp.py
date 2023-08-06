from typing import Dict, Optional


class Otp:
    """Otp class, containing otps information."""

    def __init__(self, client):
        self._client = client
        self.email = Email(client)
        self.sms = SMS(client)

    def verify(
        self,
        otp: str,
        method_id: str,
        session_token: Optional[str] = None,
        session_jwt: Optional[str] = None,
        session_expires_in: Optional[int] = None,
        device_fingerprint: Optional[Dict] = None,
    ):
        req = {
            'otp': otp,
            'method_id': method_id,
        }

        if device_fingerprint:
            req['device_fingerprint'] = device_fingerprint
        if session_expires_in:
            req['session_expires_in'] = session_expires_in
        if session_token:
            req['session_token'] = session_token
        if session_jwt:
            req['session_jwt'] = session_jwt
        return self._client.api.post_request('auth/otps/verify', body=req)


class Email:

    def __init__(self, client):
        self._client = client

    def login_or_create(
        self,
        email: str,
        expires_in: Optional[int] = None,
        device_fingerprint: Optional[Dict] = None,
        requires_verification: Optional[bool] = False,
    ):

        req = {
            'email': email,
            'requires_verification': requires_verification,
        }
        
        if expires_in:
            req['expires_in'] = expires_in
        if device_fingerprint:
            req['device_fingerprint'] = device_fingerprint

        return self._client.api.post_request('auth/otps/email/login_or_create', body=req)

    def send(
        self,
        email: str,
        expires_in: Optional[int] = None,
        device_fingerprint: Optional[Dict] = None,
    ):

        req = {
            'email': email,
        }
        
        if expires_in:
            req['expires_in'] = expires_in
        if device_fingerprint:
            req['device_fingerprint'] = device_fingerprint

        return self._client.api.post_request('auth/otps/email/send', body=req)

class SMS:

    def __init__(self, client):
        self._client = client

    def login_or_create(
        self,
        phone_number: str,
        expires_in: Optional[int] = None,
        device_fingerprint: Optional[Dict] = None,
        requires_verification: Optional[bool] = False,
    ):

        req = {
            'phone_number': phone_number,
            'requires_verification': requires_verification,
        }
        
        if expires_in:
            req['expires_in'] = expires_in
        if device_fingerprint:
            req['device_fingerprint'] = device_fingerprint

        return self._client.api.post_request('auth/otps/sms/login_or_create', body=req)

    def send(
        self,
        phone_number: str,
        expires_in: Optional[int] = None,
        device_fingerprint: Optional[Dict] = None,
    ):

        req = {
            'phone_number': phone_number,
        }
        
        if expires_in:
            req['expires_in'] = expires_in
        if device_fingerprint:
            req['device_fingerprint'] = device_fingerprint

        return self._client.api.post_request('auth/otps/sms/send', body=req)
