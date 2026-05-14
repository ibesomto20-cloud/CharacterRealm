import requests


class OGSync:
    def __init__(self):
        self.endpoint = "https://indexer-storage-testnet-turbo.0g.ai/file/segment"

    def upload_file(self, file_path):
        try:
            with open(file_path, "rb") as f:
                files = {"file": f}
                response = requests.post(self.endpoint, files=files, timeout=30)

            if response.status_code == 200:
                return True, response.json()

            return False, response.text

        except Exception as e:
            return False, str(e)