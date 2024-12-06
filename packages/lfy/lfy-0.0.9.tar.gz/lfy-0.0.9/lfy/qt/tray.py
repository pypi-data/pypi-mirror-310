'托盘图标'
from gettext import gettext as _

from PyQt6.QtGui import QAction, QClipboard
from PyQt6.QtWidgets import QApplication, QMenu, QMessageBox, QSystemTrayIcon

from lfy import APP_NAME, PACKAGE_URL, PACKAGE_URL_BUG, VERSION
from lfy.qt.preference import PreferenceWindow
from lfy.qt.translate import TranslateWindow
from lfy.utils import cal_md5
from lfy.utils.settings import Settings


class TrayIcon(QSystemTrayIcon):
    def __init__(
        self,
        parent,
        app,
        icon
    ) -> None:
        QSystemTrayIcon.__init__(self, icon, parent)
        # QSystemTrayIcon also tries to save parent info but it screws up the type info
        self.w: TranslateWindow = parent
        self.app: QApplication = app
        self.setToolTip(APP_NAME)
        self.sg = Settings()

        # 创建托盘菜单
        tray_menu = QMenu(parent)
        open_action = QAction(_("Open"), self)
        open_action.triggered.connect(self.w.show)
        tray_menu.addAction(open_action)

        self.cb: QClipboard = self.app.clipboard()

        self.auto_action = QAction(
            _('Copy to translate'), triggered=self.copy2translate)
        self.auto_action.setEnabled(True)
        self.auto_action.setCheckable(True)
        self.auto_action.setChecked(
            self.sg.g("copy-auto-translate", d=True, t=bool))
        self.copy2translate()

        tray_menu.addAction(self.auto_action)

        pf_action = QAction(_("Preference"), self)
        pf_action.triggered.connect(self.show_setting_window)
        tray_menu.addAction(pf_action)

        about_action = QAction(_("About"), self)
        about_action.triggered.connect(self.show_about_window)
        tray_menu.addAction(about_action)

        quit_action = QAction(_("Quit"), self)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(quit_action)

        self.setContextMenu(tray_menu)

        self.img_md5 = ""
        self.text_last = ""

    def _on_clipboard_data_changed(self):

        if self.cb.mimeData().hasImage():
            # 如果是图片，处理图片
            image = self.cb.image()
            if not image.isNull():
                file_path = "/tmp/lfy.png"
                image.save(file_path, "PNG")

                md5_hash = cal_md5(file_path)
                if self.img_md5 == md5_hash:
                    return
                self.img_md5 = md5_hash

                if not self.w.isVisible():
                    self.w.show()
                self.w.ocr_image(file_path)
        elif self.cb.mimeData().hasText():
            text = self.cb.text()
            if text == self.text_last:
                return
            self.text_last = text

            if not self.w.isVisible():
                self.w.show()
            self.w.translate_text(text)

    def quit_app(self):
        """退出程序
        """
        re = QMessageBox.warning(self.w, _("warn"), _("quit?"),
                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                 QMessageBox.StandardButton.No)
        if re == QMessageBox.StandardButton.Yes:
            self.setVisible(False)  # 隐藏托盘控件，托盘图标刷新不及时，提前隐藏
            self.app.quit()  # 退出程序

    def show_about_window(self):
        """关于窗口
        """
        s = f'''<h3>{APP_NAME}</h3>
            <p>{VERSION}</p>
            <p><a href="{PACKAGE_URL}">home</a> < /p >
            <p><a href="{PACKAGE_URL_BUG}">bug report</a></p>
            <p>&copy; 2024 yuhldr</p>
            <p>'''
        s += _("Translation software for read paper")
        s += "</p>"
        QMessageBox.about(
            self.w,
            "About",
            s
        )

    def show_setting_window(self):
        self.prf = PreferenceWindow(self.cb, self)
        self.prf.show()

    def show_msg(self, title, msg):
        self.showMessage(
            title, msg, QSystemTrayIcon.MessageIcon.Information, 2000)

    def copy2translate(self):
        """复制即翻译可以选择暂停，并且会记住选择
        """
        auto_translate = self.auto_action.isChecked()
        self.sg.s("copy-auto-translate", auto_translate)
        if auto_translate:
            t = _("Copy to translate")
            m = _("Copy detected, translate immediately")
            n = QSystemTrayIcon.MessageIcon.Warning
            self.cb.dataChanged.connect(self._on_clipboard_data_changed)
        else:
            self.cb.disconnect()
            t = _("Stop copy to translate")
            m = _("Copy detected, not automatically translated")
            n = QSystemTrayIcon.MessageIcon.Critical
        self.showMessage(t, m, n, 2000)
