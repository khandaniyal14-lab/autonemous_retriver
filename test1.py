import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP configuration
smtp_server = "smtp.gmail.com"
port = 587
sender_email = "daniyal@irp.edu.pk"
password = "tywcfigthpjjzwnt"

receiver_email = "khandaniyal1144@gmail.com"

# Create message
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = "Test Email from Smart Attendance"

body = "This is a test email to verify Gmail SMTP configuration."
msg.attach(MIMEText(body, "plain"))

try:
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

    print("✅ Email sent successfully!")

except Exception as e:
    print("❌ Error:", e)