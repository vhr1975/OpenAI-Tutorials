# Logging, error handling, helpers
# Logging is essential for debugging, monitoring, and production reliability.
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("function-calling-demo")

def log_request(request):
    logger.info(f"Request: {request}")

def log_response(response):
    logger.info(f"Response: {response}")

def log_error(error):
    logger.error(f"Error: {error}")
