import json
from typing import Callable

from PySide6.QtCore import QEventLoop, QUrl
from PySide6.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply, QHttpMultiPart, QHttpPart
from PySide6.QtWidgets import QApplication

from ..core import Qt
from ..widgets import MessageBar

access = QNetworkAccessManager()


class MIME:
    JSON = 'application/json'
    MultipartForm = 'multipart/form-data'
    Form = 'application/x-www-form-urlencoded'


class Request(QNetworkRequest):
    def __init__(self, url: str,
                 method='GET', *,
                 params: dict | QHttpMultiPart = None,
                 headers: dict = None,
                 ):
        super().__init__()
        self.method = method.upper()
        self.params = params or {}
        self.headers = headers or {}

        for header, value in self.headers.items():
            self.setHeader(header, f'{value}')

        if self.method == 'GET':
            if query := '&'.join(f'{k}={v}' for k, v in self.params.items()):
                url += f'?{query}'
        self.setUrl(url)

    def send(self, finished: bool | Callable[[QNetworkReply], None] = None, *,
             download_progress: Callable[[int, int], None] = None,
             upload_progress: Callable[[int, int], None] = None,
             ) -> QNetworkReply:
        if self.method == 'POST':
            reply = access.post(self, self.data())
        else:
            reply = access.get(self)

        if upload_progress: reply.uploadProgress.connect(upload_progress)
        if download_progress: reply.downloadProgress.connect(download_progress)

        if finished is None:  # 同步请求
            QApplication.setOverrideCursor(Qt.CursorShape.Wait)
            loop = QEventLoop()

            reply.finished.connect(loop.quit)
            loop.exec(QEventLoop.ProcessEventsFlag(3))

            QApplication.restoreOverrideCursor()
            return self.finished(reply)

        if isinstance(finished, Callable):
            reply.finished.connect(
                lambda:
                reply.error().value != 5 and finished(self.finished(reply))
            )
        return reply

    @staticmethod
    def finished(reply: QNetworkReply) -> QNetworkReply:
        if reply.error().value not in (0, 5):
            MessageBar.error('错误', reply.errorString())
        return reply

    def data(self) -> bytes | QHttpMultiPart:
        data = self.params
        if isinstance(data, QHttpMultiPart):
            return data

        if self.header('Content-Type') == MIME.JSON:
            return json.dumps(data).encode()

        it = (f'{k}={v}' for k, v in data.items())
        return '&'.join(it).encode()

    def setHeader(self, header: QNetworkRequest.KnownHeaders | str, value: str) -> None:
        if isinstance(header, str):
            self.setRawHeader(header, value)
            return
        super().setHeader(header, value)

    def header(self, header: QNetworkRequest.KnownHeaders | str) -> str:
        if isinstance(header, str):
            return self.rawHeader(header)
        return super().header(header)

    def setRawHeader(self, header: str, value: str) -> None:
        super().setRawHeader(header.encode(), value.encode())

    def rawHeader(self, header: str) -> str:
        return super().rawHeader(header).toStdString()

    def urlString(self, options=QUrl.ComponentFormattingOption.PrettyDecoded) -> str:
        if not isinstance(options, QUrl.ComponentFormattingOption):
            options = QUrl.ComponentFormattingOption(options)
        return self.url().toString(options)


class HttpPart(QHttpPart):
    def __init__(self,
                 body: str | bytes = None, *,
                 headers: dict[QNetworkRequest.KnownHeaders | str, str] = None,
                 other: QHttpPart = None
                 ):
        if other:
            super().__init__(other)
        else:
            super().__init__()

        for key, value in headers.items():
            if isinstance(key, str):
                self.setRawHeader(key.encode(), value.encode())
                continue
            self.setHeader(key, value)

        if body is not None:
            if isinstance(body, int | float | bool | str):
                body = f'{body}'.lower() if isinstance(body, bool) else body
                body = f'{body}'.encode()
            self.setBody(body)


class HttpMultiPart(QHttpMultiPart):
    def __init__(self, *part: QHttpPart,
                 ct=QHttpMultiPart.ContentType.FormDataType,
                 parent=None
                 ):
        super().__init__(ct, parent)
        if part:
            if isinstance(first := part[0], list):
                part = first
            self.append(*part)

    def append(self, *part: QHttpPart) -> None:
        for x in part:
            super().append(x)
