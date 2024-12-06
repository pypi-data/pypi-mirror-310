class Origin:

    @staticmethod
    def create_request_body() -> dict:
        return {
            "product": "SDK",
            "source": "python",
            "sourceVersion": "1.1.62",
            "system": "doku-python-library",
            "apiFormat": "SNAP"
        }