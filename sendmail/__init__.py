import os
import smtplib
import argparse
from decouple import config

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

SMTP_USER = config('SMTP_USER', default=None)
SMTP_PASSWORD = config('SMTP_PASSWORD', default=None)
FROM_ADDRESS = config('FROM_ADDRESS', default=None)
TO_ADDRESS = config('TO_ADDRESS', default=None)
SMTP_HOST = config('SMTP_HOST', default=None)
SERVER_PORT = config('SERVER_PORT', default=587, cast=int)
SUBJECT = config('SUBJECT', default="Python SMTP")


def sendmail(
        from_address,
        to_address,
        server,
        user,
        password,
        port,
        subject,
        attachments):
    from_address = from_address or user
    content = []
    while True:
        try:
            line = input()
            if not line:
                break
            content.append(line)
        except EOFError:
            break

    smtp = smtplib.SMTP(
        host=server,
        port=port,
    )
    smtp.starttls()
    smtp.login(user, password)

    email = MIMEMultipart()
    email['From'] = from_address
    email['To'] = ";".join(to_address)
    email['Subject'] = subject

    email.attach(MIMEText("\n".join(content), 'plain'))

    for attach in attachments:
        abs_path = os.path.abspath(attach)
        file_name = os.path.basename(attach)
        part =  MIMEBase('application', 'octet-stream')
        part.set_payload(open(abs_path,'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {file_name}')
        email.attach(part)
    smtp.send_message(email)


def main():
    parser = argparse.ArgumentParser(description='Send SMTP e-mail')
    parser.add_argument(
        '--user',
        nargs='?',
        metavar='F',
        required=not (SMTP_USER or FROM_ADDRESS),
        type=str,
        help='smtp user',
        default=SMTP_USER or FROM_ADDRESS
    )
    parser.add_argument(
        '--from-address',
        nargs='?',
        metavar='F',
        required=False,
        type=str,
        help='from address',
        default=SMTP_USER or FROM_ADDRESS
    )
    parser.add_argument(
        '--to-address',
        nargs='+',
        metavar='T',
        required=not TO_ADDRESS,
        type=str,
        help='to address',
        default=TO_ADDRESS
    )
    parser.add_argument(
        '--subject',
        nargs="?",
        metavar='C',
        required=not SUBJECT,
        type=str,
        help='e-mail subject',
        default=SUBJECT
    )
    parser.add_argument(
        '--server',
        nargs='?',
        required=not SMTP_HOST,
        metavar='S',
        type=str,
        help='smtp server address',
        default=SMTP_HOST
    )
    parser.add_argument(
        '--password',
        nargs='?',
        type=str,
        required=not SMTP_PASSWORD,
        help='from address password',
        default=SMTP_PASSWORD
    )
    parser.add_argument(
        "--port",
        nargs='?',
        metavar='P',
        type=int,
        required=not SERVER_PORT,
        help='smtp server port',
        default=SERVER_PORT,
    )
    parser.add_argument(
        "--attach",
        dest='attachments',
        nargs='+',
        type=str,
        help='attachment files',
        required=False,
        default=[],
    )
    args = parser.parse_args()
    sendmail(**vars(args))


if __name__ == '__main__':
    main()