
import requests


VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'


def verify(secret, response):
    url = f"{VERIFY_URL}?secret={secret}&response={response}"
    response = requests.post(url)
    result = response.json()
    return result.get('success')

