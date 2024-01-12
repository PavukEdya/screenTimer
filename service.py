from models import Window as mWindow, Session as mSession
from windows import Window
from sessions import Session
from db_manager import WindowDBManager, SessionDBManager


class WindowService:
    def __init__(self):
        self.db_manager = WindowDBManager()
        self.session_service = SessionService()

    def write_windows(self, windows):
        for window in windows:
            if window.active:
                window.deactivate()
            self._write_window(window)

    def _write_window(self, window: Window):
        founded_window = self.db_manager.get_by_fullname(window.fullname)
        if founded_window is None:
            model = self.convert_to_model(window)
            self.db_manager.add(model)
            founded_window = model
        self._write_window_sessions(founded_window, window.sessions)

    def _write_window_sessions(self, window: mWindow, sessions):
        for session in sessions:
            self.session_service.write(window, session)

    def get_all(self):
        return self.db_manager.get_all()

    def convert_to_model(self, window: Window) -> mWindow:
        model = mWindow(
            name=window.name,
            fullname=window.fullname)
        return model


class SessionService:

    def __init__(self):
        self.db_manager = SessionDBManager()

    def convert_to_model(self, session: Session, window: mWindow) -> mSession:
        model = mSession(
            window=window,
            start_time=session.start_time,
            end_time=session.stop_time)
        return model

    def write(self, window: mWindow, session):
        model = self.convert_to_model(session, window)
        self.db_manager.add(model)

    def get_all(self):
        return self.db_manager.get_all()
