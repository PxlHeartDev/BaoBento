# Other stuff
import os.path
import ssl
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email = os.environ['email']
password = os.environ['password']

def sendEmail(recipient: str, subject: str, body = "", attachment = None):
    if(recipient == "r"): return
    # Set up the email
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = recipient
    html_part = MIMEText(body)
    msg.attach(html_part)
    
    # Add attachment if it's been defined
    if(attachment):
        with open(attachment, "rb") as att:
            # Add the attachment to the message
            part = MIMEBase("application", "octet-stream")
            part.set_payload(att.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {attachment}",
        )
        msg.attach(part)
    
    # Get SSL context
    context = ssl.create_default_context()
    
    # Connect to Gmail's public SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(email, password)
        server.sendmail(email, recipient, msg.as_string())

#json.loads(str(THINGY).removeprefix('b\'').removesuffix('\''))