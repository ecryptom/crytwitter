import random, datetime
from smtplib import SMTP_SSL

#email info for verifaction code
o = SMTP_SSL('mail.applier.ir', 465)
def send_email(reciever, code, sender='info@applier.ir'):
    o.connect('mail.applier.ir', 465)
    message = f"""From: crypto <{sender}>
    To: To Person <{reciever}>
    Subject: SMTP e-mail test

    your code to sign up in crypto:
    {code}
    """
    print(message[116:125])
    o.login('info@applier.ir', '4420888024ZyDJnYe5')
    o.sendmail(sender, reciever, message)

send_email('mr.mirshamsi.78@gmail.com', 45632)