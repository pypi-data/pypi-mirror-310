import json

from PySide6.QtCore import QByteArray

from fluentui.network import Request, HttpMultiPart, HttpPart
from fluentui.widgets import App


def fetch():
    def loads(a: QByteArray):
        d = json.loads(a.data())
        print(f'{d, type(d)=}')

    class Model:
        file_xx: str = ''

    r = Request(
        'https://dog.ceo/api/breeds/image/random',
    )

    reply = r.send(
        False,
        # download_progress=lambda c, t: print(c, t)
    )


if __name__ == '__main__':
    print()
    app = App()

    fetch()

    print('exec..')
    app.exec()
