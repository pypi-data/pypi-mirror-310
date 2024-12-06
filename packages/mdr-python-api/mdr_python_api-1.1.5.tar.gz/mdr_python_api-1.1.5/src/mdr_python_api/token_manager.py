from .token_generator import create_token
import os.path

TOKEN_LIVENESS_TIME = 9 * 60
TOKEN_FILE_PATH = "/tmp/mdr_client_token.txt"


class TokenManager:
    def read_token(self):
        with open(TOKEN_FILE_PATH, "r") as file:
            return file.read()

    def generate_token(self):
        token = create_token()
        with open(TOKEN_FILE_PATH, "w") as text_file:
            text_file.write(token)
        return token

    def token_exists(self):
        return os.path.exists(TOKEN_FILE_PATH)

    """
    If the token is not stored on the file or if it is expired (new_token is true) then generate new token
    """

    def get_token(self, new_token=False):
        if new_token:
            return self.generate_token()
        if self.token_exists():
            return self.read_token()
        else:
            return self.generate_token()
