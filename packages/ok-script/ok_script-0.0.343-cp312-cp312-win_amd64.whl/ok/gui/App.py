import sys

from PySide6.QtCore import QSize, QCoreApplication
from PySide6.QtGui import QIcon
from ok.Util import get_path_relative_to_exe

import ok
from ok.analytics.Analytics import Analytics
from ok.gui.Communicate import communicate
from ok.gui.MainWindow import MainWindow
from ok.gui.MessageWindow import MessageWindow
from ok.gui.StartController import StartController
from ok.gui.common.config import Language
from ok.gui.i18n.GettextTranslator import get_translations
from ok.gui.overlay.OverlayWindow import OverlayWindow
from ok.gui.util.app import init_app_config
from ok.logging.Logger import get_logger
from ok.update.GitUpdater import GitUpdater

logger = get_logger(__name__)


class App:
    def __init__(self, config,
                 exit_event=None):
        super().__init__()
        self.config = config

        self.app, self.locale = init_app_config()
        communicate.quit.connect(self.app.quit)

        # qconfig.theme = cfg.themeMode.value

        self.about = self.config.get('about')
        self.title = self.config.get('gui_title')
        self.app.setApplicationName(self.title)
        self.app.setApplicationDisplayName(self.title)
        self.version = self.config.get('version')
        self.app.setApplicationVersion(self.version)
        self.overlay = self.config.get('debug')
        if self.config.get('git_update'):
            self.updater = GitUpdater(self.config, exit_event)

        logger.debug(f'locale name {self.locale.name()}')

        self.loading_window = None
        self.overlay_window = None
        self.main_window = None
        self.exit_event = exit_event
        self.icon = QIcon(get_path_relative_to_exe(config.get('gui_icon')) or ":/icon/icon.ico")
        if self.config.get('analytics'):
            self.fire_base_analytics = Analytics(self.config, self.exit_event)

        self.start_controller = StartController(self.config, exit_event)
        if self.config.get('debug'):
            self.to_translate = set()
        else:
            self.to_translate = None
        self.po_translation = None
        ok.gui.app = self

    def tr(self, key):
        if not key:
            return key
        if ok_tr := QCoreApplication.translate("app", key):
            if ok_tr != key:
                return ok_tr
        if self.to_translate is not None:
            self.to_translate.add(key)
        if self.po_translation is None:
            try:
                self.po_translation = get_translations(self.locale.name())
                self.po_translation.install()
                logger.info(f'translation installed for {self.locale.name()}')
            except:
                logger.error(f'install translations error for {self.locale.name()}')
                self.po_translation = "Failed"
        if self.po_translation != 'Failed':
            return self.po_translation.gettext(key)
        else:
            return key

    def gen_tr_po_files(self):
        folder = ""
        for locale in Language:
            from ok.gui.i18n.GettextTranslator import update_po_file
            folder = update_po_file(self.to_translate, locale.value.name())
        return folder

    def show_message_window(self, title, message):
        message_window = MessageWindow(self.icon, title, message, exit_event=self.exit_event)
        message_window.show()

    def show_already_running_error(self):
        title = QCoreApplication.translate("app", 'Error')
        content = QCoreApplication.translate("app",
                                             "Another instance is already running")
        self.show_message_window(title, content)

    def show_path_ascii_error(self, path):
        title = QCoreApplication.translate("app", 'Error')
        content = QCoreApplication.translate("app",
                                             "Install dir {path} must be an English path, move to another path.").format(
            path=path)
        self.show_message_window(title, content)

    def update_overlay(self, visible, x, y, window_width, window_height, width, height, scaling):
        if self.overlay_window is None:
            self.overlay_window = OverlayWindow(ok.gui.device_manager.hwnd)
        self.overlay_window.update_overlay(visible, x, y, window_width, window_height, width, height, scaling)

    def show_main_window(self):

        if self.overlay and ok.gui.device_manager.hwnd is not None:
            communicate.window.connect(self.update_overlay)

        self.main_window = MainWindow(self.config, self.icon, self.title, self.version, self.overlay, self.about,
                                      self.exit_event)
        # Set the window title here
        self.main_window.setWindowIcon(self.icon)

        size = self.size_relative_to_screen(width=0.5, height=0.6)
        self.main_window.resize(size)
        self.main_window.setMinimumSize(size)

        self.main_window.show()
        self.main_window.raise_()
        self.main_window.activateWindow()
        logger.debug(f'show_main_window end')

    def size_relative_to_screen(self, width, height):
        screen = self.app.primaryScreen()
        size = screen.size()
        # Calculate half the screen size
        half_screen_width = size.width() * width
        half_screen_height = size.height() * height
        # Resize the window to half the screen size
        size = QSize(half_screen_width, half_screen_height)
        return size

    def exec(self):
        sys.exit(self.app.exec())
