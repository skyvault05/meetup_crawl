#%%
import smtplib

gmail_user = '@gmail.com'
gmail_password = ''


sent_from = "@gmail.com"
to = ["@gmail.com"]
subject = "smtp test"
body = "hey, waht's up"

email_text = """
From: %s  
To: %s  
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to,'subject:'+subject+"\n"+body)
    server.close()

    print("email sent!")
except:
    print('Something went wrong...')




#%%
