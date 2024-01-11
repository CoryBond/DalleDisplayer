import sys
from PyQt5.QtWidgets import QSplashScreen, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QPinchGesture, QGraphicsItem
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPixmap, QTransform


class ImageViewer(QGraphicsView):
    def __init__(self, startingImage: str):
        super().__init__()

        self.init_ui(startingImage)

    def init_ui(self, startingImage: str):

        self.setDragMode(QGraphicsView.ScrollHandDrag)

        # Create a graphics view and scene
        if startingImage is not None:
            self.replaceimage(startingImage)
        
        # Enable pinch gestures

        # self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        #self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
 
        # Set initial zoom level
        #self.scale_factor = 1.0

    
    def replaceimage(self, imagePath: str):
        scene = QGraphicsScene(self)

        # Add an image to the scene
        pixmap = QPixmap(imagePath)  # Replace with the path to your image
        splash = QSplashScreen(pixmap)
        splash.show()
        self.pixmapItem = QGraphicsPixmapItem(pixmap)
        self.pixmapItem.setFlag(QGraphicsItem.ItemIsMovable)

        self.fitInView()

        scene.addItem(self.pixmapItem)
        self.setScene(scene)

    
    def hasPhoto(self):
        return True


    # From https://stackoverflow.com/questions/35508711/how-to-enable-pan-and-zoom-in-a-qgraphicsview
    def fitInView(self, scale=True):
        rect = QRectF(self.pixmapItem.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0
        

    def pinchEvent(self, event):
        pinch = event.gesture(QPinchGesture)
        if pinch:
            # Calculate the scale factor from the pinch ge-sture
            scale_factor = pinch.scaleFactor()

            # Adjust the scale factor and update the transformation
            self.scale_factor *= scale_factor
            self.setTransform(QTransform().scale(self.scale_factor, self.scale_factor))