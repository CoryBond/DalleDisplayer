from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QToolBar, QAction

from utils.pageUtils import PageMetaDecorator


class MainWindow(QMainWindow):

    def __init__(self, *arg: PageMetaDecorator):
        super(MainWindow, self).__init__()               

        self.pages = dict((pageMeta.pageName, pageMeta) for pageMeta in arg)

        self.init_ui()


    def init_ui(self):
        # Set up the main window
        self.setWindowTitle('Full Screen UI')
        self.showFullScreen()

        # Toolbar
        self.init_toolbar()

        self.central_widget = QStackedWidget()
        
        for page in self.pages.values():
            self.central_widget.addWidget(page.widget)

        self.setCentralWidget(self.central_widget)


    def init_toolbar(self):
        # Toolbar
        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        for page in self.pages.values():
            page_routing_button = QAction(page.pageCaption, self)
            page_routing_button.setStatusTip(page.hint)
            # Use default arg trick in lambdas to save current variables value rather then the variable itself in the lambda scope
            page_routing_button.triggered.connect(lambda _, pageWidget=page.widget: self.route_to_page(pageWidget))
            toolbar.addAction(page_routing_button)


    def route_to_page(self, widget):
        self.central_widget.setCurrentWidget(widget)