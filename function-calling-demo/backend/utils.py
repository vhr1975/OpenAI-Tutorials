# Logging, error handling, helpers
# Logging is essential for debugging, monitoring, and production reliability.
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("function-calling-demo")

def log_request(request):
    logger.info(f"Request: {request}")

def log_response(response):
    logger.info(f"Response: {response}")

 # Simple logging functions for unit tests
def log_info(msg):
    print(msg)

def log_error(msg):
    print(f"Error: {msg}")
