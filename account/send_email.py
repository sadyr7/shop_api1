from django.core.mail import send_mail
from django.utils.html import format_html


# 1 вариант
# def send_confirmation_email(email, code):
#     send_mail(
#         'Здравствуйте, активируйте ващ аккаунт!',
#         f'Чтобы активировать ваш аккаунт скопируйте и введите на сайте код:'
#         f'\n{code}'
#
#         f'\nне передавайте ему никому',
#         'elchacha@gmail.com',
#         [email],
#         fail_silently=False
#     )

# 2 вариант
def send_confirmation_email(email, code):
    activation_url = f'http://127.0.0.1:8000/api/account/activate/?u={code}'
    message = format_html(
        'Здравствуйте, активируйте ваш аккаунт! '
        'Чтобы активировать ваш аккаунт, перейдите по ссылке:'
        '<br>'
        '<a href="{}">{}</a>'
        '<br>'
        'Не передавайте этот код никому!',
        activation_url, activation_url
    )

    send_mail(
        'Здравствуйте, активируйте ваш аккаунт!',
        message,
        'johnsnowtest73@gmail.com',
        [email],
        fail_silently=False,
    )