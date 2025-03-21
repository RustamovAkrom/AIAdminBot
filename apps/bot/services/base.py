import requests
from core import settings


class APIClient:
    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.headers = {
            "Content-Type": "application/json"
        }
    
    def _request(self, method, endpint, data=None):
        url = f"{self.base_url}/{endpint}"

        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                headers=self.headers
            )
            # response.raise_for_status()
            try:
                data = response.json()
            except:
                data = None

            return response.status_code, data
        except requests.exceptions.RequestException as e:
            print(f"API error: {e}")
            return None, {"error": str(e)}
    