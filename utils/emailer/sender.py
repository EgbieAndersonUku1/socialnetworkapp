import yagmail
from flask import current_app


class EmailSender(object):

    def __init__(self, recipient, subject, content):
        self._recipient = recipient
        self._subject = subject
        self._content = content

    def send(self):

        yag = yagmail.SMTP("abbys348@gmail.com", "egbiereleuku14789")
        yag.send(to=self._recipient, subject=self._subject, contents=self._content)

    def _is_app_in_test_mode(self):
        if current_app.config.get("TESTING"):
            return False