import atexit
import time
import os

from windows import WindowsManager, WindowChecker
from service import WindowService
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()


class ScreenTimer:

    def __init__(self):
        self.window_manager = WindowsManager()
        self.window_service = WindowService()
        self.stat_writer = None

    def run(self):
        while True:
            time.sleep(2)
            self.window_manager.window_manage(self._active_window_name)

    def on_terminate(self):
        windows = self.window_manager.windows
        self.window_service.write_windows(windows)

    @property
    def _active_window_name(self):
        return WindowChecker.get_active_window_title()


app = ScreenTimer()
atexit.register(app.on_terminate)

if __name__ == '__main__':
    app.run()







