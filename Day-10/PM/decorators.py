import time
from functools import wraps
from typing import Any, Callable


def timer(func: Callable) -> Callable:
    """Measure and print execution time of a function.

    Args:
        func: Function to decorate.

    Returns:
        Wrapped function.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} executed in {end - start:.6f} seconds")
        return result

    return wrapper


def logger(func: Callable) -> Callable:
    """Log function name, arguments, and return value.

    Args:
        func: Function to decorate.

    Returns:
        Wrapped function.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Calling {func.__name__}")
        print(f"Args: {args}, Kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"Returned: {result}")
        return result

    return wrapper


def retry(max_attempts: int = 3) -> Callable:
    """Retry a function if it raises an exception.

    Args:
        max_attempts: Maximum number of attempts.

    Returns:
        Decorator function.

    Raises:
        ValueError: If max_attempts is less than 1.
    """
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_error = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_error = exc
                    print(f"Attempt {attempt} failed: {exc}")
                    if attempt == max_attempts:
                        raise last_error

        return wrapper

    return decorator


# Demo usage
if __name__ == "__main__":
    @timer
    def slow_add(a: int, b: int) -> int:
        time.sleep(0.1)
        return a + b

    @logger
    def greet(name: str, greeting: str = "Hello") -> str:
        return f"{greeting}, {name}"

    counter = {"tries": 0}

    @retry(max_attempts=3)
    def unstable() -> str:
        counter["tries"] += 1
        if counter["tries"] < 3:
            raise ValueError("Temporary failure")
        return "Success"

    print(slow_add(2, 3))
    print(greet("Amit", greeting="Hi"))
    print(unstable())