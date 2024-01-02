import time


class Window:
    def __init__(self, title):
        self._sessions = []
        self.title = title
        self._current_session = None
        self.is_active = False

    @property
    def current_active_time(self):
        if self._current_session:
            return self._current_session.active_time
        return 0

    @property
    def work_time(self):
        work_time = 0
        for session in self._sessions:
            work_time += session.active_time
        return work_time

    def activate(self):
        self.is_active = True
        self._current_session = self.Session()
        self._sessions.append(self._current_session)

    def deactivate(self):
        self.is_active = False
        self._current_session.end_session()
        self._current_session = None

    class Session:
        def __init__(self):
            self.is_active = True
            self.end_time = None
            self.start_time = int(time.time())

        @property
        def active_time(self):
            if self.end_time:
                return self.end_time - self.start_time
            return int(time.time()) - self.start_time

        def end_session(self):
            self.end_time = int(time.time())
            self.is_active = False


class WindowsManager:
    def __init__(self):
        self.windows = {}
        self._current_window = None

    @property
    def current_window(self):
        if self._current_window:
            return self._current_window.title
        return None

    def activate_window(self, title):
        if title != self.current_window:
            if self._current_window:
                self._current_window.deactivate()
            if title in self.windows:
                self._current_window = self.windows[title]
                self._current_window.activate()
            else:
                new_window = Window(title)
                new_window.activate()
                self.windows[title] = new_window
                self._current_window = new_window
