import os
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


def send_email(**kwargs):
    """
    This function sends an email based on the arguments provided. Arguments
    include template, data, subject and to_email. template is the full
    path of the email template. data is a dictionary containing all
    the variables required by the template.
    :param kwargs:
    :return:
    """

    from_email = os.getenv("EMAIL_HOST_SENDER")

    # render with dynamic value
    html_content = render_to_string(kwargs['template'], kwargs['data'])

    # Strip the html tag. So people can see the pure text at least.
    text_content = strip_tags(html_content)

    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives(kwargs['subject'], text_content, from_email, [kwargs['to_email']])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    response = {"message": "email sent"}

    return response

