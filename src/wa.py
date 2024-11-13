import os, json, twilio.rest as rest


mainDir = os.path.abspath(os.path.dirname(__file__))
settingsFilePath = os.path.join(mainDir, 'settings.json')
    

class WaBot:
    def __init__(self, credentials: dict, about: str, manual: str, verbose: bool = False):
        self.account_sid = credentials['account-sid']
        self.auth_token = credentials['auth-token']
        self.phone = credentials["phone-number"]
        self.client = rest.Client(self.account_sid, self.auth_token)

    def send_message(self, message: str, to_number: str):
        msg = self.client.messages.create(
            body=message,
            from_=self.phone,
            to=f"whatsapp:{to_number.replace(' ', '')}"
        )

        return msg.sid

    def read_message(self, to_number: str):
        messages = self.client.messages.list(
            to=f"whatsapp:{to_number.replace(' ', '')}",
            limit=1
        )
        if messages:
            return messages[0].body

        return None

    def message_jenerator(self, msg: str, subject: str, reveal: bool = False):
        if reveal:
            add = "This is a machine generated message. Please do not reply."

        return f"```Subject: {subject}```\n\n{msg}\n\n*{add}*"
    
    def main(self):
        pass
