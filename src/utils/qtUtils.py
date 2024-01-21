from PyQt5.QtWidgets import QLayout


def clear_layout(layout: QLayout):
    # Remove the current layout from the widget
    if layout:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)