import time

class RateLimiter:
    """
    A class to enforce a rate limit for a specific number of requests per minute.
    """
    def __init__(self, nb_of_req_per_min=30):
        """
        Initializes the rate limiter.

        :param nb_of_req_per_min: Number of requests allowed per minute (default: 30).
        """
        self.sec = 60 / nb_of_req_per_min
        self.last_request_time = time.time() - self.sec  # Allow immediate first request
        self.nb_of_req_per_min = nb_of_req_per_min
    
    def wait(self):
        """
        Waits if necessary to enforce the rate limit.
        Logs time spent waiting and ensures compliance with the rate limit.
        """
        elapsed = time.time() - self.last_request_time
        if elapsed < self.sec:
            time_to_wait = self.sec - elapsed
            print(f"RateLimiter: Waiting for {time_to_wait:.2f} seconds to stay within {self.nb_of_req_per_min} requests/minute limit.")
            time.sleep(time_to_wait)
        else:
            print("RateLimiter: No wait needed, proceeding immediately.")
        self.last_request_time = time.time()
