# install libraries using pip3 install smtplib ,email

# importing smtplib and email libraries
import smtplib  
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# provide subject line, df to attach and toaddr list of email strings
# subject = "auto generated email"
# df = pd.DataFrame()
# toaddr = ['abc@xyz.com' , 'def@xyz.com']
def send_mail_html_adress(subject,df1,df2,toaddr):   
    # from address - specific to the SMTP server being used
    fromaddr = "noreply@xyz.com"
    
    # instance of MIMEMultipart 
    msg = MIMEMultipart() 

    # storing the senders email address   
    msg['From'] = fromaddr

    # storing the receivers email address  
    msg['To'] = ', '.join(toaddr)

    # the email body is sent as an html page attached to the MIMEmultipart instance
    html = """\
    <html>
      <head></head>
      <body>
        <p><br> Heading 1<br>
           <br> Sub Heading 1<br>
           {0}
           <br> Sub Heading 2<br>
           {1}           
        </p>
        <br>Regards
      </body>
    </html>

    """.format(df1.to_html(), df2.to_html()) # use df1.to_html(index=False) to ignore index while attaching df


    # storing the subject  
    msg['Subject'] = subject


    # attach the body with the msg instance 
    msg.attach(MIMEText(html, 'html')) 


    # creates SMTP session 
    s = smtplib.SMTP('pqr@xyz.com',25) 

    # start TLS for security 
    s.starttls() 

    # Authentication 
    try :
        s.login(fromaddr,"p@ssword") 
    except Exception as err:
        print("Authentication error detected")

    text = msg.as_string() 

    s.sendmail(fromaddr, toaddr,text)

    s.quit()
