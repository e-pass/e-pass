import requests
from celery import shared_task
from django.conf import settings


@shared_task
def send_sms_with_code(phone_number: str, code: int) -> dict:
    try:
        url = f'https://sms.ru/sms/send?api_id={settings.SMSRU_API_TOKEN}&to={phone_number}&msg={code}&json=1'
        response = requests.get(url=url)
        result = {'server_status': response.status_code,
                  'message_status': response.json()}
    except requests.RequestException as ex:
        result = {'server_status': str(ex)}
    return result
