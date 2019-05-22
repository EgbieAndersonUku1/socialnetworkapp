import yagmail

# To use the Email sender you must first turn on secure less app in gmail account
_GMAIL_EMAIL = "ADD YOUR GMAIL EMAIL ADDRESS"
_GMAIL_PASSWD = "ADD YOUR GMAIL PASSWORD HERE"


class EmailSender(object):

    def __init__(self, recipient, subject, content):
        self._recipient = recipient
        self._subject = subject
        self._content = content

    def send(self):
        """Allows the application to send emails to any account"""

        yag = yagmail.SMTP(_GMAIL_EMAIL, _GMAIL_PASSWD)
        yag.send(to=self._recipient, subject=self._subject, contents=self._content)

