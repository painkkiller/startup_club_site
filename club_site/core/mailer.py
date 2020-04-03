from django.core.mail import EmailMultiAlternatives


def mail_to_users(mail_subject, html_content, txt_content, mails):
    sender = "postmaster@startup-club.tech"
    email = EmailMultiAlternatives(mail_subject, txt_content, sender, mails)
    if html_content:
        email.attach_alternative(html_content, "text/html")
    resp = email.send()
    return resp