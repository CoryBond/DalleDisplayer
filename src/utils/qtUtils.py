from PyQt5.QtWidgets import QLayout


def clear_layout(layout: QLayout):
    """
    Takes a QLayout and completely removes all of the widgets attached to it. 
    Decoupled widgets will also have their parents set to nothing.

    This function is useful for replacing contents of a layout without completely replacing the layout if its hard coupled
    to another widget.
    """
    if layout:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)