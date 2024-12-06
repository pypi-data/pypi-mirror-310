# time-cap
A lightweight Python package to measure and log function execution times.


```python
from time_cap import time_cap


@time_cap
def dummy_func():
    import time
    time.sleep(2)


dummy_func()
