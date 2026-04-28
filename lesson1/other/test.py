from typing import TypeVar, Any
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - here is the message: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("log.txt")
    ]
)

logging.debug("debug message")
logging.info("info message")
logging.warning("warning message")

try:
    raise Exception("This is a test exception")
except Exception as e:
    logging.warning("warning message")
    logging.error(f"Error: {e}")

logging.critical("critical message")









# StringIntegerFloatType = TypeVar("StringIntegerFloatType", str, int, float) 


# def concatanate(a: int, b: Any) -> Any:
#     print("concatanate", a, b)
#     return a + b


# print(concatanate("Hello", "World"))
# print(concatanate(1, 2))
# print(concatanate(1.0, 2.0))
