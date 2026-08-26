import time

class Timer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.elapsed = time.time() - self.start

def run_with_timing(func, *args, **kwargs):
    try:
        with Timer() as t:
            result = func(*args, **kwargs)
        return {"success": True, "result": result, "latency_seconds": round(t.elapsed, 2), "error": None}
    except Exception as e:
        return {"success": False, "result": None, "latency_seconds": None, "error": str(e)}