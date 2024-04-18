import requests
import json
import signal
import threading
import multiprocessing
from .http_request import HttpRequest  # Make sure to import your HttpRequest class
from .mylogger import MyLogger

class Mammoth:
    def __init__(self, drumpler_url, authorization_key, custom_value, process_request_data, num_workers=None):
        self.drumpler_url = drumpler_url
        self.auth_key = authorization_key
        self.custom_value = custom_value
        self.user_process_request_data = process_request_data
        
        # Initialize custom logger
        self.logger = MyLogger.get_logger()
        
        self.num_workers = num_workers if num_workers is not None else multiprocessing.cpu_count()
        
        # Signal handling to gracefully shutdown on SIGINT (CTRL+C)
        self.stop_signal = threading.Event()  # Use an event to signal workers to stop
        signal.signal(signal.SIGINT, self.signal_handler)

        # Simplified run method using threads directly
        self.worker_threads = []

    def get_logger(self):
        return self.logger

    def signal_handler(self, signum, frame):
        print("Shutdown signal received, stopping workers...")
        self.stop_signal.set()  # Signal all threads to stop

    def fetch_next_pending_job(self):
        try:
            headers = {"Authorization": f"Bearer {self.auth_key}"}
            params = {'custom_value': self.custom_value} if self.custom_value else {}
            response = requests.get(f"{self.drumpler_url}/jobs/next-pending", headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                return HttpRequest(
                    id=data['request_id'],
                    job_id=data['job_id'],
                    source_ip=data['source_ip'],
                    user_agent=data['user_agent'],
                    method=data['method'],
                    request_url=data['request_url'],
                    request_raw=json.loads(data['request_raw']),
                    custom_value=data['custom_value']
                )
            else:
                self.logger.error(f"Failed to fetch next pending job: {response.status_code} - {response.text}")
                return None
        except requests.ConnectionError as e:
            self.logger.error(f"Network problem occurred: {str(e)}")
            return None
        except requests.Timeout as e:
            self.logger.error(f"Request timed out: {str(e)}")
            return None
        except requests.RequestException as e:
            self.logger.error(f"HTTP request failed: {str(e)}")
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

    def mark_request_as_handled(self, job_id):
        """
        Mark the request as handled when the job is completed.
        """
        headers = {"Authorization": f"Bearer {self.auth_key}"}
        response = requests.put(f"{self.drumpler_url}/jobs/{job_id}/mark-handled", headers=headers)
        if response.status_code == 200:
            print(f"Request marked as handled for job {job_id}")
        else:
            print(f"Failed to mark request as handled for job {job_id}: {response.status_code}")
        
    def update_status(self, job_id, new_status):
        headers = {"Authorization": f"Bearer {self.auth_key}"}
        data = {"status": new_status}
        try:
            response = requests.put(f"{self.drumpler_url}/jobs/{job_id}/update-status", json=data, headers=headers)
            if response.status_code == 200:
                self.logger.info(f"Status updated to {new_status} for job {job_id}")
                if new_status == "Completed":
                    self.mark_request_as_handled(job_id)
            else:
                self.logger.error(f"Failed to update status for job {job_id}: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            self.logger.error(f"Failed to update status due to HTTP error: {str(e)}")

    def worker_task(self):
        while not self.stop_signal.is_set():
            request = self.fetch_next_pending_job()
            if request:
                if self.user_process_request_data(request):
                    self.insert_event(request.job_id, "Request processed successfully")
                    self.update_status(request.job_id, "Completed")
                    self.logger.info(f"Request processed successfully for job {request.job_id}")
                else:
                    self.insert_event(request.job_id, "Failed to process request")
                    self.update_status(request.job_id, "Error")
                    self.logger.error(f"Failed to process request for job {request.job_id}")
            if self.stop_signal.wait(timeout=0.1):
                break

    def stop(self):
        self.stop_signal.set()
        for thread in self.worker_threads:
            thread.join()

    def run(self):
        self.worker_threads = [threading.Thread(target=self.worker_task) for _ in range(self.num_workers)]
        for thread in self.worker_threads:
            thread.start()
        for thread in self.worker_threads:
            thread.join()
    

if __name__ == "__main__":
    mammoth = Mammoth(process_request_data=lambda req: True)
    print("Starting Mammoth application...")
    try:
        mammoth.run()
    except KeyboardInterrupt:
        print("Shutdown signal received")
        mammoth.stop()
        print("Mammoth application stopped gracefully")
