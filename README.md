# Drumpler-Mammoth

Drumpler-Mammoth is a robust job processing component of the [Drumpler framework](https://github.com/KarelOmab/Drumpler), designed to handle the asynchronous processing of tasks that are queued by the Drumpler API. It is engineered to automate and simplify the processing of queued jobs, allowing developers to solely focus on implementing custom logic to handle pending jobs as desired.

## Overview

Mammoth works by querying the Drumpler API for pending jobs and processes them according to user-defined functions. It efficiently manages job statuses and logs events related to job processing, making it an essential tool for applications requiring complex workflows and detailed execution tracking.

## Features

-   **Automated Job Fetching**: Regularly polls the Drumpler API to fetch and process pending jobs.
-   **Custom Job Processing**: Allows developers to define custom functions that dictate how jobs should be processed.
-   **Event Logging**: Facilitates the logging of detailed events related to job processing, enhancing traceability and monitoring.
-   **Graceful Shutdown**: Handles shutdown signals to gracefully stop processing and prevent job interruptions.

## Dependencies
Drumpler-Mammoth is installed as part of the [Drumpler framework](https://github.com/KarelOmab/Drumpler).
Ensure that Drumpler is **installed, configured and running** before setting up your Mammoths

## Installation
Mammoth is available via pypi:
`pip install Drumpler-Mammoth`

## Configuration

Mammoth requires the two following variables to communicate with Drumpler. These **should** be defined in a `.env` file in the root directory of the application:

```
DRUMPLER_HOST=127.0.0.1					# this has to be your Drumpler's URL
AUTHORIZATION_KEY=YourAuthorizationKey 	# this has to match with Drumpler's key
```

## Sample Mammoth

To start using Mammoth:
1. Create a python file
2. Define a **custom processing function**
	- **Do not change the name of this method (custom_process_function)**
3. Instantiate Mammoth with the required parameters
	- drumpler_host
	- authorization_key
	- custom_value
	- num_workers

Below is a basic example of how to set up and run a Mammoth:

```
import  os
from  drumpler_mammoth  import  Mammoth

# comment 3 lines below if not using .env file
from dotenv import load_dotenv #pip install python-dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Optional: Offline-logging mechanism is also shipped with Mammoth, feel free to use it
#mammoth  =  None  # This global variable can be shared among all scopes

def  custom_process_function(request) -> bool:
	# I shall write my custom job-processing logic here

	# offline logging
	#mammoth.logger.info(f"I could utilize mammoth's logger for <info> messages") #optional
	#mammoth.logger.error(f"I could utilize mammoth's logger for <error> messages") #optional
	
	# online logging
	#mammoth.insert_event(request.job_id, "My event message goes here")

	# I shall return True in a success-scenario or 	# => job.status = 'Completed'
	# I shall return False in a failure-scenario	# => job.status = 'Error'

	pass

if  __name__  ==  "__main__":
	# the constructor parameters are MANDATORY
	drumpler_host  =  os.environ.get("DRUMPLER_HOST", "localhost")
	authorization_key  =  os.environ.get("AUTHORIZATION_KEY", "AUTH_KEY_HERE")
	custom_value  =  "ApplicationName"
	num_workers  =  None  # None implies os.cpu_count(), otherwise you can manually specify

	# initialize mammoth
	mammoth  =  Mammoth(drumpler_url=drumpler_host, authorization_key=authorization_key, custom_value=custom_value, process_request_data=custom_process_function, num_workers=num_workers)

	print("Starting Mammoth... Press CTRL+C to stop.")

	try:
		mammoth.run()
	except  KeyboardInterrupt:
		print("Shutdown signal received")
		mammoth.stop()
		print("Mammoth application stopped gracefully")
```

## API Interactions

Mammoth interacts with the following Drumpler API endpoints to manage jobs:

-   **GET** `/jobs/next-pending`: Fetch the next pending job.
-   **PUT** `/jobs/{job_id}/update-status`: Update the status of a job.
-   **PUT** `/jobs/{job_id}/mark-handled`: Mark a job as handled.
-   **POST** `/events`: Log an event related to a job.

These interactions are handled internally by Mammoth, allowing developers to focus on implementing the business logic needed for processing jobs.

## Handling Shutdowns

Mammoth listens for shutdown signals and ensures that all active threads are gracefully stopped, ensuring data integrity and proper job completion.

## Offline Logging

Mammoth uses custom implementation of the `logging` module to track its operations and log essential information about job processing and system status, which aids in debugging and monitoring the application in production.

## Contributing

Contributions to the development of Mammoth are welcome. Please follow the standard fork-branch-PR workflow for contributions.

## License

Drumpler-Mammoth is released under the MIT License. For more details, see the LICENSE file included with the Drumpler distribution.