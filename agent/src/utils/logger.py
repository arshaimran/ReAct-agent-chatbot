import logging

logging.basicConfig(level=logging.INFO)

def log_with_request_id(request_id, message):
    logging.info(f"[{request_id}] {message}")
