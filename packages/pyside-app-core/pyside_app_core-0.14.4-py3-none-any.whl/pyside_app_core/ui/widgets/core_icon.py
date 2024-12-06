from typing import cast

from PySide6.QtCore import QRect, QSize
from PySide6.QtGui import QColor, QGuiApplication, QIcon, QIconEngine, QPainter, QPalette, QPixmap
from PySide6.QtSvg import QSvgRenderer

from pyside_app_core.utils.painter import safe_paint


class _SvgIconEngine(QIconEngine):
    def __init__(self, on_state: str, off_state: str | None):
        super().__init__()
        self._on_file = on_state
        self._off_file = off_state

    def clone(self) -> "_SvgIconEngine":
        return self.__class__(self._on_file, self._off_file)

    def pixmap(self, size: QSize, mode: QIcon.Mode, state: QIcon.State) -> QPixmap:
        pixmap = QPixmap(size)
        pixmap.fill(QColor(0, 0, 0, 0))

        painter = QPainter(pixmap)
        self.paint(painter, pixmap.rect(), mode, state)
        painter.end()

        return pixmap

    def paint(self, painter: QPainter, rect: QRect, mode: QIcon.Mode, state: QIcon.State) -> None:
        app_palette = cast(QGuiApplication, QGuiApplication.instance()).palette()

        renderer = (
            QSvgRenderer(self._on_file) if state == QIcon.State.On else QSvgRenderer(self._off_file or self._on_file)
        )

        if mode == QIcon.Mode.Normal:
            color = app_palette.color(QPalette.ColorRole.Text)
        elif mode == QIcon.Mode.Disabled:
            color = app_palette.color(QPalette.ColorRole.PlaceholderText)
        elif mode == QIcon.Mode.Active:
            color = app_palette.color(QPalette.ColorRole.Accent)
        elif mode == QIcon.Mode.Selected:
            color = app_palette.color(QPalette.ColorRole.Highlight)
        else:
            color = app_palette.color(QPalette.ColorRole.Text)

        with safe_paint(painter):
            painter.setClipRect(rect)
            renderer.render(painter)
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
            painter.fillRect(rect, color)


class CoreIcon(QIcon):
    def __init__(self, on_state: str, off_state: str | None = None):
        super().__init__(_SvgIconEngine(on_state, off_state))
