from typing import List

class MailGunEmail:
    def __init__(self, to: List[str], subject: str, text: str, from_: str = None, attachments: list = None):
        if not isinstance(to, list):
            raise ValueError("The 'to' parameter must be a list of email addresses.")
        if not all(self._check_email_format(email) for email in to):
            raise ValueError("One or more email addresses in 'to' are not valid.")
        self.to_email = to
        self.from_email = from_
        self.subject = subject
        self.text = text
        self.attachments = attachments
        
    def _check_email_format(self, email: str) -> bool:
        if "@" in email and "." in email.split("@")[-1]:
            return True
        return False