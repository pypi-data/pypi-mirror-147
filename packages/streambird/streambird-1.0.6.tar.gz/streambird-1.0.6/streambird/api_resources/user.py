from typing import Dict, Optional, List


class User:
    """User class, containing users information."""

    def __init__(self, client):
        self._client = client

    def create(
        self,
        email: Optional[str] = None,
        phone_number: Optional[str] = None,
        first_name: Optional[str] = None,
        middle_name: Optional[str] = None,
        last_name: Optional[str] = None,
        requires_verification: Optional[bool] = False,
    ):
        req = {
            'requires_verification': requires_verification,
        }

        if email:
            req['email'] = email
        if phone_number:
            req['phone_number'] = phone_number
        if first_name:
            req['first_name'] = first_name
        if middle_name:
            req['middle_name'] = middle_name
        if last_name:
            req['last_name'] = last_name
        return self._client.api.post_request('auth/users/create', body=req)

    def get(self, user_id: str):
        return self._client.api.get_request('auth/users/{}'.format(user_id))

    def update(
        self,
        user_id: str,
        emails: Optional[List[str]] = None,
        phone_numbers: Optional[List[str]] = None,
        first_name: Optional[str] = None,
        middle_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ):

        req = {}
        if emails:
            req['emails'] = []
            for email in emails:
                req['emails'].append({'email': email})

        if phone_numbers:
            req['phone_numbers'] = []
            for phone_number in phone_numbers:
                req['phone_numbers'].append({'phone_number': phone_number})

        if first_name:
            req['first_name'] = first_name
        if middle_name:
            req['middle_name'] = middle_name
        if last_name:
            req['last_name'] = last_name
        return self._client.api.put_request('auth/users/{}/update'.format(user_id), body=req)

    def delete(self, user_id: str):
        return self._client.api.delete_request('auth/users/{}/delete'.format(user_id))

    def delete_email(self, email_id: str):
        return self._client.api.delete_request('auth/users/emails/{}/delete'.format(email_id))

    def delete_phone_number(self, phone_number_id: str):
        return self._client.api.delete_request('auth/users/phone_numbers/{}/delete'.format(phone_number_id))
