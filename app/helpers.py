import time
import logging


def processing_time_logger(funk):
    def wrapper(value):
        start_time = time.time()
        result = funk(value)
        end_time = time.time()
        processing_time = end_time - start_time
        logging.info(
            f"Обработка {result.__name__} заняла {processing_time:.2f} секунд."
        )

    return wrapper
