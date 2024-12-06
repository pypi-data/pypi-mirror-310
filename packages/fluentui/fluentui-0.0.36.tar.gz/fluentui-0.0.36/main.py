import json

from fluentui.network import Request
from fluentui.widgets import App
from PySide6.QtCore import QByteArray


def fetch():
    def loads(a: QByteArray):
        d = json.loads(a.data())
        print(f'{d=}')

    r = Request('https://dog.ceo/api/breeds/image/random')
    reply = r.send()
    # reply = r.send(lambda: loads(reply.readAll()))
    loads(reply.readAll())


if __name__ == '__main__':
    print()
    app = App()

    fetch()

    print('exec..')
    app.exec()
