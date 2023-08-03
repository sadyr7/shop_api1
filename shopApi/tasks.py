from account.send_email import send_confirmation_email
from account.send_sms import send_activation_sms
from .celery import app

@app.task()
def send_confirmation_email_task(email, code):
    send_confirmation_email(email, code)

@app.task()
def send_activation_sms_task(phone_number, activation_code):
    send_activation_sms(phone_number, activation_code)

@app.task()
def send_order_notifaction_task(user_email, order_id):
    send_order_notifaction(user_email, order_id)