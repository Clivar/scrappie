import logging

def setup_logger_level(debug: bool):
    # Set level of the logger
    logging.getLogger().setLevel(logging.DEBUG if debug else logging.INFO)

    # Update the format and handler of the root logger
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Remove all handlers from the root logger
    logging.getLogger().handlers = []
    # Add the new handler to the root logger
    logging.getLogger().addHandler(console_handler)

