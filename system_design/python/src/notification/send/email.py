import smtplib, os
from email.message import EmailMessage

def notification(message):
    try:
        message = json.loads(message)
        mp3_fid = message["mp3_fid"]
        sender_address = os.environ.get('GMAIL_ADDRESS')
        sender_password = os.environ.get('GMAIL_PASSWORD')
        receiver_address = message["username"]
        
        msg = EmailMessage()
        msg.set_content(f'mp3 file id: {mp3_fid} is now ready')
        msg["Subject"] = "Mp3 ready"
        msg["From"] = sender_address
        msg["To"] = receiver_address

        session = smtplib.SMTP("smtp.gmail.com", 587) #587 is the port for tls and start tls
        session.starttls()
        session.login(sender_address, sender_password)
        session.send_message(msg)
        print("Mail Sent")
    except Exception as err:
        print(err)
        return err