from Config import *
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
current_date = datetime.now().strftime('%d/%m/%Y')
def NullEmail(rowquery1,rowquery2,rowquery3):
    from_email = 'ajithkumar@newgendigital.com'
    from_password = os.getenv("DB_PASSWORD")
    #to_email="ajithkumaraji9047@gmail.com"
    to_email = 'arun.reddy@newgendigital.com'
    #cc_email=''
    cc_email = 'punitha@newgendigital.com, priyadharshini@newgendigital.com, prasanth@newgendigital.com'
    subject = '<Re:Daily Threshold Update>'

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
            <p>Hi Arun,</p>
            <p>Please refer to the count  regarding the threshold master : {rowquery1} and threshold feeds :{rowquery2} and Total null: {rowquery3} for {current_date}.</p>
            <p>We update those null values</p>
            <b style="color: blue;">Thanks & Regards,<br></b>
            <p>Ajithkumar Sekar | Technical support executive<br>
            Newgen Digital Works Pvt. Ltd.<br>
            M: (+91) 8072467327<br>
            W: <a href="http://www.newgen.co">www.newgen.co</a><br>
            A:  Chennai - 600041.</p>
        </body>
        </html>
    '''
    msg.attach(MIMEText(body, 'html'))
    try:
        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)

        # Send the email
        recipients = [to_email] + cc_email.split(', ')
        server.sendmail(from_email, recipients, msg.as_string())
        print("Email sent successfully!")
        logging.info("Count Email sent successfully!")

    except Exception as e:
        print("An error occurred:", str(e))
        logging.error("An error occurred:%s", str(e))

    finally:
        server.quit()