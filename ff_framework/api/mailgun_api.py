import os
import requests
from ff_framework.models.mailgun_models import MailGunEmail

class MailgunAPI:
    def __init__(self, logger, database):
        self.logger = logger
        self.database = database
        self.__endpoint = "https://api.mailgun.net/v3/sandbox120b4df04aa94f039ce98cc8eca1b8f9.mailgun.org/messages"
        self.__auth = ("api", os.getenv('MAILGUN_API_KEY'))
        self.default_from_email = "Mailgun Sandbox <postmaster@sandbox120b4df04aa94f039ce98cc8eca1b8f9.mailgun.org>"
        
    def send(self, email: MailGunEmail):
        def handle_attachments(email: MailGunEmail):
            raw_attachment = []
            if email.attachments is not None:
                for attachment in email.attachments:
                    raw_attachment.append(('attachment', (attachment, open(attachment, 'rb'))))
            return raw_attachment
        attachments = handle_attachments(email)
        if attachments == []:
            attachments = None
        if not email.from_email:
            email.from_email = self.default_from_email
        if not email.to_email:
            self.logger.log("No 'to' email address provided.", level='error')
            return None
        if not email.subject:
            email.subject = "Hello from FormFlow"
        if not email.text:
            email.text = "Hello! \nThank you for using FormFlow. \nSincerely, \nThe FormFlow Team"
        try:
            for to_email in email.to_email:
                response = requests.post(
                    self.__endpoint,
                    auth=self.__auth,
                    files=attachments,
                    data={
                        "from": email.from_email,
                        "to": to_email,
                        "subject": email.subject,
                        "text": email.text
                    }
                )
                if response.status_code == 200:
                    self.logger.log(f"Email sent successfully to {to_email}", level='info')
                else:
                    self.logger.log(f"Failed to send email to {to_email}: {response.text}", level='error')
        except Exception as e:
            self.logger.log(f"Failed to send email: {e}", level='error')
            return None
    