# this application will fetch crypto currency data drom coingeko site
# find top 10 to sell
# find top 10 to buy
# send mail to me everyday at 8AM

# task:
# 1. download the datasets from the coingeko
# 2. send mail
# 3. schedule taks 8 AM

# importing libraries
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

import requests
import schedule
from datetime import datetime
import time
import pandas as pd

def send_mail(subject, html_body, file_name):
    # SendGrid credentials
    smtp_server = "smtp.sendgrid.net"
    smtp_port = 587
    username = "apikey"
    password = "xxxxxxx" #enter your own api secret key
    sender_mail = "dev.gupta@mail.com"
    receiver_mail = "gupta55dev@gmail.com"

    # compose the mail
    message = MIMEMultipart()
    message['From'] = sender_mail
    message['To'] = receiver_mail
    message['Subject'] = subject

    # attaching body of the mail
    message.attach(MIMEText(html_body, 'html'))
 
    # attach csv file
    with open(file_name, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)  #this line encodes the file in base64
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(file_name)}",
            )
            message.attach(part)

    # start server
    try:
        # setup 
        with smtplib.SMTP(smtp_server,smtp_port) as server:
            server.starttls()   #start the server
            # login to our account
            server.login(username, password)

            # send mail
            server.sendmail(sender_mail, receiver_mail, message.as_string())
            print("mail sent successfully!")

    except Exception as e:
        print(f"Unable to send mail {e}")

# Getting Crypto Data
def get_crypto_data():

    #API Information
    url = "https://api.coingecko.com/api/v3/coins/markets"
    param = {
        'vs_currency' : 'usd',
        'order' : 'market_cap_desc',
        'per_page': 250,
        'page': 1
    }

    # Sending Requests
    response = requests.get(url, params = param)

    # Checking response
    if response.status_code ==200:
        print("Connection Successful!\nGetting the Data...")

        # storing the response into data
        data = response.json()

        # creating dataframe
        df = pd.DataFrame(data)

        # filtering data, getting important columns
        df = df[[
            'id', 'current_price', 'market_cap', 'price_change_percentage_24h','high_24h', 'low_24h','ath', 'atl'
        ]]

        # creating new columns
        today = datetime.now().strftime('%d-%m-%Y__%Hh%Mm%Ss')
        df['time_stamp'] = today

        # getting top 10
        top_neg_10 = df.nsmallest(10, 'price_change_percentage_24h')
        top_neg_10.to_csv(f'Top 10 Crypto_Negative{today}.csv', index = False)

        top_pos_10 = df.nlargest(10, 'price_change_percentage_24h')
        top_pos_10.to_csv(f'Top 10 Crypto_Positive{today}.csv', index = False)

        top_pos_html = top_pos_10.to_html(index=False, border=1)
        top_neg_html = top_neg_10.to_html(index=False, border=1)

        
        # saving data
        file_name = f'crypto_data{today}.csv'
        df.to_csv(file_name, index = False)
        print(f'Data Saved Successfully as {file_name}')

        

   
        # Call Email Function to Send Email
        subject = f'Top 10 Crypto Currency to Invest for {today}'
        html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; color: #333;">
                <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; border: 1px solid #ccc;">
                <h2 style="color: #2c3e50;">Good Morning!</h2>
                <p>Here's your Crypto Report for <strong>{today}</strong></p>

                <h3 style="color: #2c3e50;">Top 10 Gainers in 24H</h3>
                {top_pos_html}

                <h3 style="color: #2c3e50;">Top 10 Losers in 24H</h3>
                {top_neg_html}

                <p style="margin-top: 20px;">
                    Check out how the other 200+ Crypto Currencies moved in the past 24H. (CSV file is attached below)
                </p>

                <p style="margin-top: 30px; font-size: 14px; color: #555;">
                    Regards,<br>
                    <strong>Your Python Application</strong><br>
                    Built by Dev Gupta
                </p>
                </div>
            </body>
            </html>
            """
        send_mail(subject, html_body, file_name)
    
    else:
        print(f'connection not established {response.status_code}')

# This runs only if the function is called.
if __name__ == '__main__':

    # call the function
    # get_crypto_data()

    # scheduling the task at 8 AM everyday
    schedule.every().day.at('8:00').do(get_crypto_data)

    while True:
        schedule.run_pending()
        time.sleep(120)  # Check every 120 seconds
