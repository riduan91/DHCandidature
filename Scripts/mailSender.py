#!/usr/bin/python
# -*- coding: utf-8 -*-

# import module to send email through gmail smtp
import smtplib
from smtplib import SMTP

# import modules to define email content
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

# constants
SENDER = 'candidature@donghanh.net'
SUBJECT = 'Hồ sơ học bổng Đồng Hành'
PASSWRD = 'Dh20152016'
DEFAULT_FOLDER = '/var/www/html/HOSO'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587 # or 465

# make a connection to gmail account to send email
# Arguments(0)
def openMailServer():
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT) #port 465 or 587
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(SENDER, PASSWRD)
    return server

# close a server connection
# Arguments(1):
#   - server: holds the connection object to be closed
def closeMailServer(server):
    server.close()

# send a file to a recipient
# Arguments(3):
#   - filename: path to file to be attached
#   - recipient: email of recipient
#   - server: email server
def send(schoolname, filename, recipient, server):
    # Headers
    msg = MIMEMultipart()
    msg['Subject'] = SUBJECT
    msg['From'] = SENDER
    msg['To'] = recipient
    msg.preamble = 'Multipart massage.\n'

    # This is the textual part:
    part = MIMEText("Thân chào bạn,\n\nTrong đường dẫn dưới đây là hồ sơ chính thức mà bạn đã gửi cho Quỹ học bổng Đồng Hành.\n\n http://docs.riduan.fr/HOSO/" + schoolname + "/" + filename + ".pdf" + "\n\nNếu hồ sơ của bạn có thư xin học bổng, đó là hồ sơ hợp lệ và sẽ được sơ tuyển bởi đại diện Đồng Hành tại trường.\n\nĐồng Hành xin trân trọng mời bạn trả lời phiếu khảo sát tại địa chỉ sau http://goo.gl/forms/RPCega7dc5 để giúp chúng tôi hoàn thiện hơn về quy trình nhận hồ sơ ở mỗi học kì. Bạn chỉ cần dành 5 phút để trả lời các câu hỏi.\n\nĐại diện Đồng Hành sẽ liên hệ nếu bạn được gọi phỏng vấn. Xin vui lòng chuẩn bị tất cả những giấy tờ cần thiết mà bạn đã ghi trong hồ sơ để đối chiếu trong ngày phỏng vấn. \n\nChúc bạn sức khỏe và học tập tốt!")
    msg.attach(part)
    # This is the binary part(The Attachment):
    # part = MIMEApplication(open(DEFAULT_FOLDER + schoolname + "/" + filename + ".pdf","rb").read())
    # part.add_header('Content-Disposition', 'attachment', filename = filename + ".pdf")
    # msg.attach(part)
    server.sendmail(SENDER, recipient, msg.as_string())
    print "Mail sent to " + recipient

def do(schoolname, filename, recipient):
    server = openMailServer()
    send(schoolname, filename, recipient, server)
    closeMailServer(server)
