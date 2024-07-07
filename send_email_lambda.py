import json
import smtplib
import os

def send_email(email_address: str,sender_email_id: str,sender_email_pass: str, subject: str, body: str):
    try: 
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email_id, sender_email_pass)
        server.sendmail("email_address", email_address,"Subject: {}\n\n{}".format(subject, body))
        server.quit()
        return 1
    except Exception as e:
        return 0
    
def lambda_handler(event, context):
    bucket_name=event["Records"][0]["s3"]["bucket"]["name"]
    object_name=event["Records"][0]["s3"]["object"]["key"]
    action_performed=event["Records"][0]["eventName"]
    sender_email_id=os.environ.get("EMAIL_MAIL")
    sender_pass_email=os.environ.get("EMAIL_PASS")
    subject="Action performed on s3 bucket"
    body="%s perfromed on bucket %s with object %s" %(action_performed,bucket_name,object_name)
    rec_email_address="receiver_email"
    try:
        response=send_email(rec_email_address,sender_email_id,sender_email_pass,subject,body)
        if response:
            print("Notification sent successfully")
        else:
            print("Notification failed to send")
    except Exception as e:
        print(str(e))
