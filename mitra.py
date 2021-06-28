import sys
import qdarkstyle
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLineEdit, QTabWidget, QShortcut


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowIcon(QIcon(os.path.join('images', 'mitra_logo2.png')))
        self.setGeometry(550, 230, 1350, 900)

        # Create toolbar
        toolbar = self.addToolBar("File")
        self.addToolBar(toolbar)
        toolbar.addSeparator()
        toolbar.setMovable(False)

        # Create tab widget
        self.tab = QTabWidget()
        self.setCentralWidget(self.tab)
        self.tab.setDocumentMode(True)
        self.tab.setTabsClosable(True)

        self.tab.tabCloseRequested.connect(self.tab_close)
        self.tab.tabBarDoubleClicked.connect(self.double_click_tab)
        self.tab.currentChanged.connect(self.current_tab_changed)

        # Add buttons to toolbar
        back_button = QAction(QIcon(os.path.join('images', 'sign-left-icon.png')), "Back", self)
        toolbar.addAction(back_button)
        back_button.triggered.connect(lambda: self.tab.currentWidget().back())

        fwd_button = QAction(QIcon(os.path.join('images', 'sign-right-icon.png')), "Forward", self)
        toolbar.addAction(fwd_button)
        fwd_button.triggered.connect(lambda: self.tab.currentWidget().forward())

        home_button = QAction(QIcon(os.path.join('images', 'house-icon.png')), "Home", self)
        toolbar.addAction(home_button)
        home_button.triggered.connect(self.go_home)

        # Create url field
        self.url_field = QLineEdit()
        self.url_field.setTextMargins(10, 0, 0, 0)
        self.url_field.setStyleSheet('padding:2px')

        # When return is pressed go to url
        self.url_field.returnPressed.connect(self.go_to_url)
        self.url_field.setClearButtonEnabled(True)
        # Add url field to our toolbar
        toolbar.addWidget(self.url_field)

        reload_button = QAction(QIcon(os.path.join('images', 'sign-sync-icon.png')), "Reload", self)
        toolbar.addAction(reload_button)
        reload_button.triggered.connect(lambda: self.tab.currentWidget().reload())

        bookmark_button = QAction(QIcon(os.path.join('images', 'star-icon.png')), "Bookmark", self)
        toolbar.addAction(bookmark_button)
        bookmark_button.triggered.connect(self.add_bookmark)

        # Dark Mode
        
        light_bulb_button = QAction(QIcon(os.path.join('images', 'light-bulb-icon.png')), "Dark Mode", self)
        toolbar.addAction(light_bulb_button)
        light_bulb_button.triggered.connect(self.set_stylesheet)

        # Define Shortcuts
        self.exit_shortcut = QShortcut(QKeySequence.Quit, self)
        self.exit_shortcut.activated.connect(lambda: app.quit())

        self.new_tab = QShortcut(QKeySequence.AddTab, self)
        self.new_tab.activated.connect(self.add_new_tab)

        self.bck_shortcut = QShortcut(QKeySequence.Back, self)
        self.bck_shortcut.activated.connect(lambda: self.tab.currentWidget().back())

        self.fwd_shortcut = QShortcut(QKeySequence.Forward, self)
        self.fwd_shortcut.activated.connect(lambda: self.tab.currentWidget().forward())

        self.refresh_shortcut = QShortcut(QKeySequence.Refresh, self)
        self.refresh_shortcut.activated.connect(lambda: self.tab.currentWidget().reload())

        # Open a tab
        self.add_new_tab('')

    def go_home(self):
        self.tab.currentWidget().setUrl(QUrl('https://github.com/zaqas/Mitra'))

    def go_to_url(self):
        address = QUrl(self.url_field.text())

        if address.scheme() == "":
            address.setScheme("http")

        self.tab.currentWidget().setUrl(address)

    def update_url(self, x, browser=None):
        if browser != self.tab.currentWidget():
            return

        self.url_field.setText(x.toString())

    def tab_close(self, i):

        if self.tab.count() < 2:
            return

        self.tab.removeTab(i)

    def double_click_tab(self, i):
        if i == -1:
            self.add_new_tab()

    def add_new_tab(self, my_url=None, label='New tab'):
        if my_url is None:
            my_url = QUrl('')

        browser = QWebEngineView()
        browser.setUrl(QUrl(my_url))
        i = self.tab.addTab(browser, label)
        self.tab.setCurrentIndex(i)

        browser.urlChanged.connect(lambda x_url, x_browser=browser:
                                   self.update_url(x_url, x_browser))
        browser.loadFinished.connect(lambda _, x_i=i, x_browser=browser:
                                     self.tab.setTabText(x_i, x_browser.page().title()))

    def current_tab_changed(self):

        q_url = self.tab.currentWidget().url()
        self.update_url(q_url, self.tab.currentWidget())
        self.update_title(self.tab.currentWidget())

    def update_title(self, browser):
        if browser != self.tab.currentWidget():
            return

        title = self.tab.currentWidget().page().title()

        self.setWindowTitle(title)

    def set_stylesheet(self):
        dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
        self.setStyleSheet(dark_stylesheet)

    def add_bookmark(self):
        # Save bookmarks in a file named bookmarks.txt
        with open('bookmarks.txt', 'a') as bm:
            bm.write(self.tab.currentWidget().url().toString())
            bm.write('\n')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('Mitra')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
