
from datetime import datetime

from .timer import TimerMeasurement


class Measurer:
    all_measurements = {}
    running_instance = None

    def __new__(cls, name, *args, **kwargs):
        deapth = 0
        if cls.running_instance is not None:
            name = f"{cls.running_instance.name}/{name}"
            deapth = cls.running_instance.deapth + 1

        if name in cls.all_measurements:
            instance = cls.all_measurements[name]
        else:
            instance = super().__new__(cls)
            instance.name = name
            instance.deapth = deapth
            instance.timer = TimerMeasurement()
            instance.create_time = datetime.now()
            instance.call_count = 0
            cls.all_measurements[name] = instance
        return instance


    def __enter__(self):
        self.parent = Measurer.running_instance
        Measurer.running_instance = self
        self.timer.start()
        self.call_count += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.timer.stop()
        Measurer.running_instance = self.parent

    def duration(self):
        return self.timer.total_time

    def __str__(self):
        return f"{'--'*self.deapth}{self.name : <30} {self.duration() : .3f}s ({self.call_count} calls)"

    @classmethod
    def print_all(cls):
        strs = [str(mzr) for mzr in sorted(cls.all_measurements.values(), key=lambda m: m.create_time)]
        print('\n'.join(strs))
