import requests
from functools import wraps

class HanditTracker:
    def __init__(self):
        self.tracking_server_url = "https://handit-api-299768392189.us-central1.run.app/api/track"
        self.api_key = None
        self.urls_to_track = []

    def config(self, api_key, tracking_url=None):
        if not api_key:
            raise ValueError("API key is required for configuration.")
        self.api_key = api_key
        if tracking_url:
            self.tracking_server_url = tracking_url
        print("Library configured successfully with API key.")

    def update_tracked_urls(self):
        if not self.api_key:
            raise ValueError("API key not set. Call the config method with your API key.")
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            response = requests.get(f"{self.tracking_server_url}/urls-to-track", headers=headers)
            response.raise_for_status()
            self.urls_to_track = response.json()
        except requests.RequestException as e:
            print(f"Error fetching URLs to track: {e}")

    def intercept_requests(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.update_tracked_urls()
            url = args[0]
            matching_url = next((u for u in self.urls_to_track if u["url"] in url), None)
            if matching_url:
                model_id = matching_url["id"]
                request_body = kwargs.get("json", kwargs.get("data"))
                
                try:
                    response = func(*args, **kwargs)
                    response_body = response.json()
                    self._send_tracked_data(model_id, request_body, response_body)
                    return response
                except Exception as e:
                    print(f"Error tracking request: {e}")
                    raise
            else:
                return func(*args, **kwargs)
        return wrapper

    def capture_model(self, model_id, request_body, response_body):
        try:
            self._send_tracked_data(model_id, request_body, response_body)
        except Exception as e:
            print(f"Error in manual tracking: {e}")

    def _send_tracked_data(self, model_id, request_body, response_body):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "input": request_body,
            "output": response_body,
            "modelId": model_id,
            "parameters": {}
        }
        try:
            response = requests.post(self.tracking_server_url, json=payload, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error sending tracked data: {e}")
