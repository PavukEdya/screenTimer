import datetime
import pygetwindow
from sessions import Session


class Window:
    def __init__(self, fullname):
        self.name_preparer = WindowNamePreparer()
        self._sessions = []
        self._fullname = fullname
        self._name = self.name_preparer.name(fullname)
        self._current_session = None
        self._active = False

    @property
    def fullname(self):
        return self._fullname

    @fullname.setter
    def fullname(self, w_fullname):
        self._fullname = w_fullname

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, w_name):
        self._name = w_name

    @property
    def sessions(self):
        return self._sessions

    @property
    def current_active_time(self):
        if self._current_session:
            return self._current_session.active_time
        return 0

    @property
    def active(self):
        return self._active

    @property
    def work_time(self):
        work_time = 0
        for session in self._sessions:
            work_time += session.active_time
        return work_time

    def activate(self):
        self._active = True
        self._current_session = Session()
        self._current_session.start()
        self._sessions.append(self._current_session)

    def deactivate(self):
        self._active = False
        self._current_session.stop()
        self._current_session = None


class WindowsManager:
    def __init__(self):
        self.current_day = datetime.date.today()
        self._windows = {}
        self._current_window = None

    @property
    def current_window_fullname(self):
        if self._current_window:
            return self._current_window.fullname
        return None

    @property
    def windows(self):
        return list(self._windows.values())

    def window_manage(self, w_fullname):
        if w_fullname != self.current_window_fullname:
            if self._current_window is not None:
                self._current_window.deactivate()
            if w_fullname in self._windows:
                self._current_window = self._windows[w_fullname]
                self._current_window.activate()
            else:
                self._activate_new_window(w_fullname)

    def _activate_new_window(self, title):
        new_window = Window(title)
        new_window.activate()
        self._windows[title] = new_window
        self._current_window = new_window


class WindowChecker:
    @staticmethod
    def get_active_window_title():
        return pygetwindow.getActiveWindow().title


class WindowNamePreparer:
    def __init__(self, input_separator='-', output_separator='-'):
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
        root = WindowName(names[-1])
        current = root
        for i in range(len(names) - 2, -1, -1):
            current.child = WindowName(names[i])
            current = current.child
        return root


class WindowName:
    def __init__(self, name: str, child: 'WindowName' = None):
        self.name = name
        self.child = child
