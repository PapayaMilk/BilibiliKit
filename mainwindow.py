import sys
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QDialog, QLabel,
    QHBoxLayout
    )

import tools
from config import config
from schema import VideoData, DashData
from Parser import BilibiliParser, BilibiliDownloader


class DownloadeWorker(QThread):
    sig = pyqtSignal()

    def __init__(self, parent, file_name, audio_url, video_url):
        super().__init__(parent)
        self.file_name = file_name
        self.audio_url = audio_url
        self.video_url = video_url

    def run(self):
        downloader = BilibiliDownloader(self.file_name, self.audio_url, self.video_url)
        downloader.download()
        self.sig.emit()


class mainwindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("bilibili.ui", self)

        self.initConfig()
        self.connectSlots()

        self.show()

        self.manuscript_info: VideoData = None
        self.manuscript_dash: DashData = None
        self.audio_map = None
        self.video_map = None

    def initConfig(self):
        self.lineEdit_2.setText(config.download_path)
        self.lineEdit_3.setText(config.cookie)

    def connectSlots(self):
        # home tab
        self.pushButton.clicked.connect(self._search)
        self.pushButton_2.clicked.connect(self._download)
        # config tab
        self.toolButton.clicked.connect(self.setDownloadPath)
        self.pushButton_3.clicked.connect(self.saveConfig)

    def showDialog(self, message):
        dialog = QDialog()
        dialog.resize(100, 100)
        dialog.setWindowTitle("提示")
        QLabel(message, dialog)
        dialog.exec()

    def _search(self):
        if not self.lineEdit.text():
            return
        text = self.lineEdit.text()
        parser = BilibiliParser()
        video_data, dash_data = parser.parse_html(text)
        self.manuscript_info = video_data
        self.manuscript_dash = dash_data
        self.showManuscriptInfo()

    def _download(self):
        if not self.manuscript_info:
            self._search()
        if self.manuscript_info.videos > 1:
            return
        filename = self.manuscript_info.pages[self.manuscript_info.embedPlayer.p-1].part if self.manuscript_info.embedPlayer.p > 1 else self.manuscript_info.title
        thread = DownloadeWorker(self, filename, self.manuscript_dash.audio[0].base_url, self.manuscript_dash.video[0].base_url)
        thread.sig.connect(self.downloadFinish)
        thread.start()
        # self.tabWidget.setCurrentIndex(1)

    def showManuscriptInfo(self):
        if not self.manuscript_info:
            return
        self.bvEdit.setText(self.manuscript_info.bvid)
        self.avEdit.setText(f"av{self.manuscript_info.aid}")
        self.titleEdit.setText(self.manuscript_info.title)
        self.pageEdit.setText(str(self.manuscript_info.videos))
        self.tagEdit.setText(self.manuscript_info.tname)
        self.pubdateEdit.setText(tools.timestamp2str(self.manuscript_info.pubdate))
        self.upEdit.setText(self.manuscript_info.owner.name)
        self.coverEdit.setText(self.manuscript_info.pic)
        self.barrageEdit.setText(self.manuscript_info.get_barrage)
        self.descEdit.setText(self.manuscript_info.desc)

    def setDownloadPath(self):
        path = QFileDialog.getExistingDirectory(self, "", config.download_path)
        if not path:
            return
        self.lineEdit_2.setText(path)

    def saveConfig(self):
        config.download_path = self.lineEdit_2.text().strip()
        config.cookie = self.lineEdit_3.text().strip()
        config.update_config()
        self.initConfig()

    def downloadFinish(self):
        self.showDialog("下载完成")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = mainwindow()
    sys.exit(app.exec_())