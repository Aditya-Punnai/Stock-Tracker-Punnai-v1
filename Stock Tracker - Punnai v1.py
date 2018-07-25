# --- Stock Tracker - Punnai v1 ---

# Step1: getting inputs from users with Tkinter

import tkinter as tk

#instance
window = tk.Tk()

#setting the window size
window.geometry("600x600")

#title
title_name = "Stock Tracker - Punnai v1"
window.title(title_name)

# last step after creating button 
#adding a function to return global values when hit is submitted (command = "finctionName")
#setting global values so we can use it for future steps (beyond tkinter)
def getValue():
    global start_date
    global end_date
    global stock_list
    global send_email
    
    start_date = entry1.get()
    end_date = entry2.get()
    stock_list = entry3.get()
    send_email = entry4.get()
    
    return start_date, end_date, stock_list, send_email

#labels
label1 = tk.Label(text = "Enter start date in the format year-month-day (eg: 2016-1-1): ")
label1.grid(column = 0, row = 0)

label2 = tk.Label(text = "Enter end date in the format year-month-day (eg: 2017-12-1): ")
label2.grid(column = 0, row = 1)

label3 = tk.Label(text = "Please enter valid US stock ticker names separated by \",\" (eg: amzn,tsla,aapl): ")
label3.grid(column = 0, row = 2)

label4 = tk.Label(text = "Please enter your valid Gmail address: ")
label4.grid(column = 0, row = 3)

#entry
entry1 = tk.Entry()
entry1.grid(column = 1,row = 0)

entry2 = tk.Entry()
entry2.grid(column = 1,row = 1)

entry3 = tk.Entry()
entry3.grid(column = 1,row = 2)

entry4 = tk.Entry()
entry4.grid(column = 1,row = 3)

#button
button1 = tk.Button(text = "SUBMIT", command = getValue)
button1.grid(column = 1, row = 4)

#looping the window
window.mainloop()



# Step2: Using the above information to extract data from Morningstar

#converting string of stocks to list
stock_list = stock_list.split(",") 

#need the following 2 lines to work around the version problem in datareader
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like 

#datareader is used to extract data from web
import pandas_datareader as web

#extracting data and assigning it to stock_df
stock_df = web.DataReader(stock_list,'morningstar',start_date, end_date)



# Step3: converting the data to csv and saving it

#generating unique file & path name
import datetime as dt
time_stamp = dt.datetime.now()
df_name = ""
for i in str(time_stamp)[:19]:
    if i in [".",":"]:
        df_name += "_"
    else:
        df_name += i
df_name += ".csv"

path = "C:\\Users\\Public\\Downloads\\" + df_name

#converting the df to csv and saving it in path
stock_df.to_csv(path) 



# Step 4: Sending the user the csv on Email

 #To work with cc, bcc, to, from we import these 2 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# https://myaccount.google.com/lesssecureapps
from_email = input("enter your email ") # I will input my email 
password = input("enter password of the email ") # I will input my password
to_address = list(send_email)

msg = MIMEMultipart() #Creates an instance of message part
msg["From"] = from_email
msg["To"] = send_email
msg["Subject"] = title_name + "-" + df_name

#body of email
body = """Dear User,
Please find the attached document which contains the stock price data for the following tickers:
{} 
starting from {} to {}. 
Hope you find it useful! - Aditya Punnai""".format(stock_list, start_date, end_date)

msg.attach(MIMEText(body,'plain'))

# Need help with attachment, most probably error with attachment
# =============================================================================
# # to attach file <- having problem attaching the csv to the email
# 
# # ** having issues in setting the path # also, PermissionError: [Errno 13] Permission denied:
# f = open(path, "rb")        
# 
# 
# attachment = MIMEText(f.read())
# attachment.add_header("Content-Disposition", "attachment", filename = df_name)
# msg.attach(attachment)
# =============================================================================

#send the email
import smtplib
server = smtplib.SMTP("smtp.gmail.com",587)
server.ehlo() #verify
server.starttls() #security
server.login(from_email,password)
text = msg.as_string()
server.sendmail(from_email,send_email,text)
server.quit()    






