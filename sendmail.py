import smtplib
import argparse
from decouple import config

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

FROM_ADDRESS = config('FROM_ADDRESS', default=None)
TO_ADDRESS = config('TO_ADDRESS', default=None)
PASSWORD = config('PASSWORD',default=None)
SERVER_ADDRESS =config('SERVER_ADDRESS',default=None)
SERVER_PORT = config('SERVER_PORT',default=587, cast=int)
SUBJECT = config('SUBJECT', default="Python SMTP")

def main(from_address, to_address, server_address, password, server_port, subject):
    smtp = smtplib.SMTP(
        host=server_address,
        port=server_port
    )
    smtp.starttls()
    smtp.login(from_address, password)

    email =  MIMEMultipart()
    email['From']=from_address
    email['To']=";".join(to_address)
    email['Subject']=subject

    content = input()

    email.attach(MIMEText(content, 'plain'))

    smtp.send_message(email)
    

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send SMTP e-mail')
    parser.add_argument(
        '--from-address',
        nargs='*' if FROM_ADDRESS else '+',
        metavar='F',
        type=str,
        help='from address',
        default=FROM_ADDRESS
    )
    parser.add_argument(
        '--to-address',
        nargs='+',
        metavar='T',
        type=str,
        help='to address',
        default=FROM_ADDRESS
    )
    parser.add_argument(
        '--subject',
        nargs="*" if SUBJECT else '+',
        metavar='C',
        type=str,
        help='e-mail subject',
        default=SUBJECT
    )
    parser.add_argument(
        '--server',
        nargs='*',
        metavar='S',
        type=str,
        help='smtp server address',
        default=SERVER_ADDRESS
    )
    parser.add_argument(
        '--password',
        nargs='*',
        type=str,
        help='from address password',
        default=PASSWORD
    )
    parser.add_argument(
        "--port",
        nargs="*" if SERVER_PORT else '+',
        metavar='P',
        type=int,
        help='smtp server port',
        default=SERVER_PORT
    )
    args = parser.parse_args()
    print(args)
    print(vars(args))
    #main(**args)