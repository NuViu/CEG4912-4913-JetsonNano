import smtplib, ssl

class snail:

    def run(self):
        message = """\
Subject: Nuviu alert!

Device has detected a fall.
"""

        # Create a secure SSL context
        context = ssl.create_default_context()

        # Try to log in to server and send email
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender, pad)
        server.sendmail(sender, receiver, message)
        server.quit() 
