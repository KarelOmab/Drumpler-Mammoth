import requests
import json
import threading
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
from .http_request import HttpRequest  # Make sure to import your HttpRequest class
from .config import Config
import traceback

class Mammoth:
    def __init__(self, process_request_data, drumpler_url=Config.DRUMPLER_URL, workers=1, custom_value=None):
        self.drumpler_url = drumpler_url
        self.auth_key = Config.AUTHORIZATION_KEY  # Default value if not set
        self.workers = workers if workers is not None else multiprocessing.cpu_count()
        self.stop_signal = threading.Event()  # Use an event to signal workers to stop
        self.user_process_request_data = process_request_data
        self.custom_value = custom_value

    def fetch_next_pending_job(self):
        headers = {"Authorization": f"Bearer {self.auth_key}"}
        params = {'custom_value': self.custom_value} if self.custom_value else {}
        response = requests.get(f"{self.drumpler_url}/jobs/next-pending", headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            # Ensure request_raw is parsed from JSON only if it's a string
            request_raw = data['request_raw']
            if isinstance(request_raw, str):
                request_raw = json.loads(request_raw)

            return HttpRequest(
                id=data['request_id'],
                job_id=data['job_id'],
                source_ip=data['source_ip'],
                user_agent=data['user_agent'],
                method=data['method'],
                request_url=data['request_url'],
                request_raw=request_raw,
                custom_value=data['custom_value']
            )
        else:
            print(f"Failed to fetch next pending job: {response.status_code}")
            return None
        
    def insert_event(self, job_id, message):
        headers = {"Authorization": f"Bearer {self.auth_key}"}
        event_data = {
            "job_id": job_id,
            "message": message
        }
        response = requests.post(f"{self.drumpler_url}/events", json=event_data, headers=headers)
        if response.status_code == 201:
            print(f"Event logged successfully for job {job_id}")
        else:
            print(f"Failed to log event for job {job_id}: {response.status_code}")

    def run(self):
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            future = executor.submit(self.worker_task)
            try:
                future.result()  # This will wait until the callable completes
            except Exception as e:
                traceback.print_exc()
                print(f"Worker task raised an exception: {e}")

    def worker_task(self):
        while not self.stop_signal.is_set():
            request = self.fetch_next_pending_job()
            if request:
                print(f"Fetched next pending job {request.job_id}")
                if self.user_process_request_data(request):
                    self.insert_event(request.job_id, "Request processed successfully")
                else:
                    self.insert_event(request.job_id, "Failed to process request")


    def stop(self):
        self.stop_signal.set()

# Setup signal handling to gracefully handle shutdowns
if __name__ == "__main__":
    mammoth = Mammoth(process_request_data=lambda req: True)  # Sample process_request_data function
    print("Starting Mammoth application...")
    try:
        mammoth.run()
    except KeyboardInterrupt:
        print("Shutdown signal received")
        mammoth.stop()
        print("Mammoth application stopped gracefully")
