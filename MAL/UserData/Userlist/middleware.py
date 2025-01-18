# middleware.py

import logging
import time
from django.utils.timezone import localtime
from datetime import datetime

# Configure the logger
logger = logging.getLogger('django')

class APILoggingMiddleware:
    """
    Middleware to log API requests and responses.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the request details
        request_method = request.method
        request_path = request.path
        request_data = self.get_request_data(request)

        # Log incoming request
        logger.info(f"Request: {request_method} {request_path} - Data: {request_data}")

        # Record the time before processing the response
        start_time = time.time()

        # Get the response
        response = self.get_response(request)

        # Calculate time taken for the request to process
        time_taken = time.time() - start_time

        # Log the response details
        logger.info(f"Response: {request_method} {request_path} - Status: {response.status_code} - "
                     f"Time Taken: {time_taken:.2f}s")

        return response

    def get_request_data(self, request):
        """
        Get request body or query parameters for logging.
        """
        if request.method == 'POST' or request.method == 'PUT':
            return request.body.decode('utf-8')  # For POST/PUT requests, log the body
        else:
            return request.GET.dict()  # For GET requests, log the query parameters
