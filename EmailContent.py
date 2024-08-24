# email.py
from Config import *
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
api_key = os.getenv("API_KEY")
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

# Use the environment variables in your code

def email_generator(excel_file_name):
    from_email = 'ajithkumar@newgendigital.com'
    from_password = os.getenv("DB_PASSWORD")
    to_email=os.getenv("TO_EMAIL")
    cc_email=os.getenv("CC_EMAIL")
    subject = '<Re: Daily Threshold Update>'

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Cc'] = cc_email
    msg['Subject'] = subject

    # Email body
    body = f'''
        <html>
        <head>
            <style>
                body {{
                    font-family: Verdana, sans-serif;
                    font-size: 14px;
                    color: black;
                }}
                p {{
                    margin: 10px 0;
                }}
            </style>
        </head>
        <body>
            <p>Hi Prashanth,</p>
            <p>Please refer to the attachment below for details regarding the threshold master,threshold feeds and threshold lead overflow for {current_date}.</p>
            <b style="color: blue;">Thanks & Regards,<br></b>
            <p>Ajithkumar Sekar | Technical support executive<br>
            Newgen Digital Works Pvt. Ltd.</p>
        </body>
        </html>
    '''
    msg.attach(MIMEText(body, 'html'))

    # Attach the Excel file
    excel_attachment = open(excel_file_name, 'rb')
    excel_part = MIMEApplication(excel_attachment.read(), Name=excelName)
    excel_attachment.close()
    excel_part['Content-Disposition'] = f'attachment; filename="{excel_file_name}"'
    msg.attach(excel_part)

    try:
        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)

        # Send the email
        recipients = [to_email] + cc_email.split(', ')
        server.sendmail(from_email, recipients, msg.as_string())
        print("Email sent successfully!")
        logging.info(f"Email sent successfully!, to{to_email}")

    except Exception as e:
        print("An error occurred:", str(e))
        logging.error("An error occurred:%s", str(e))

    finally:
        server.quit()
