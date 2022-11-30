import smtplib, ssl
from getpass import getpass

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = ""
password = getpass("Type your password and press enter: ")
receiver_email = ""

message = """Subject: Test IV

content"""

# Create a secure SSL context
context = ssl.create_default_context()

# Try to log in to server and send email
try:
	server = smtplib.SMTP(smtp_server,port)
	server.ehlo() # Can be omitted
	server.starttls(context=context) # Secure the connection
	server.ehlo() # Can be omitted
	server.login(sender_email, password)
	server.sendmail(sender_email, receiver_email, message)

except Exception as e:
	# Print any error messages to stdout
	print(e)
finally:
	server.quit() 