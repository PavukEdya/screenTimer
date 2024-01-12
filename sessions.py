from datetime import datetime


class Session:
    def __init__(self):
        self._active = False
        self._stop_time = None
        self._start_time = None

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, _time: datetime):
        self._start_time = _time

    @property
    def stop_time(self):
        return self._stop_time

    @stop_time.setter
    def stop_time(self, _time: datetime):
        self._stop_time = _time

    @property
    def active_time(self):
        if self._stop_time:
            return self._stop_time - self._start_time
        return datetime.now() - self._start_time

    def start(self):
        if self._stop_time is not None:
            raise SessionStartException()
        if self._start_time is None:
            self._start_time = datetime.now()
        self._active = True

    def stop(self):
        if self._start_time is None:
            raise SessionStopException()
        self._stop_time = datetime.now()
        self._active = False


class SessionStartException(Exception):
    def __init__(self):
        self.message = 'You cannot start a session that has already stopped'

    def __str__(self):
        return self.message


class SessionStopException(Exception):
    def __init__(self):
        self.message = 'You cannot stop a session that has not started'

    def __str__(self):
        return self.message
