from threading import Event, Timer


def set_interval(interval: float, times=-1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            stop_event = Event()

            def loop():
                i = 0
                while not stop_event.is_set() and i != times:
                    func(*args, **kwargs)
                    i += 1
                    stop_event.wait(interval)

            timer = Timer(0, loop)
            timer.daemon = True
            timer.start()

            return stop_event

        return wrapper

    return decorator
