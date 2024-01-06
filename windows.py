import datetime
import time
import json
import pygetwindow


class Window:
    def __init__(self, fullname):
        self.name_preparer = WindowNamePreparer()
        self._sessions = []
        self.fullname = fullname
        self.name = self.name_preparer.name(fullname)
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
        self._current_session = Session()
        self._current_session.start()
        self._sessions.append(self._current_session)

    def deactivate(self):
        self.is_active = False
        self._current_session.stop()
        self._current_session = None


class Session:
    def __init__(self):
        self.is_active = False
        self.stop_time = None
        self.start_time = None

    @property
    def active_time(self):
        if self.stop_time:
            return self.stop_time - self.start_time
        return int(time.time()) - self.start_time

    def start(self):
        if self.stop_time is not None:
            raise self.SessionStartException()
        if self.start_time is None:
            self.start_time = int(time.time())
        self.is_active = True

    def stop(self):
        if self.start_time is None:
            raise self.SessionStopException()
        self.stop_time = int(time.time())
        self.is_active = False

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


class WindowsManager:
    def __init__(self):
        self.windows = {}
        self._current_window = None

    @property
    def current_window(self):
        if self._current_window:
            return self._current_window.name
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


class WindowChecker:
    @staticmethod
    def get_active_window_title():
        return pygetwindow.getActiveWindow().title


class WindowNamePreparer:
    def __init__(self, input_separator='–', output_separator=''):
        self.input_separator = input_separator
        self.output_separator = output_separator

    def name(self, fullname):
        names = [n.strip() for n in fullname.split(self.input_separator)]
        return names[-1]

    def fullname(self, fullname) -> str:
        current = self._create_window_name_linked_list(fullname)
        names = []
        while current is not None:
            names.append(current.name)
            current = current.child
        return self.output_separator.join(names)

    def _create_window_name_linked_list(self, name: str):
        names = [n.strip() for n in name.split(self.input_separator)]
        root = WindowName(names[-1])  # Создаем корневой элемент списка
        current = root
        # Проходим по элементам массива, начиная с предпоследнего
        for i in range(len(names) - 2, -1, -1):
            # Создаем элемент списка и связываем его с текущим элементом
            current.child = WindowName(names[i])
            current = current.child
        return root


class WindowName:
    def __init__(self, name: str, child: 'WindowName' = None):
        self.name = name
        self.child = child
