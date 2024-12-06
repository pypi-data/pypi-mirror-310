from fluentui.gui import Font
from fluentui.widgets import App, Widget, Textarea, Row

if __name__ == '__main__':
    print()
    app = App(font=Font(pixel=14))

    html_content = """
<html>
    <style>
        img { text-align: center; }
    </style>
    <body>
        <p>美丽的图片</p>
        
        <img src="https://haowallpaper.com/link/common/file/previewFileImg/15851046182949184" style="text-align: center; display: block; ">
        <div class="img" style="text-align: center;">
            <p>标签：孤独摇滚 波奇酱 | 分类：动漫 二次元 | 分辨率：4096x2692 | 大小：319K</p>
        </div><br/>
        
        <div class="img">
            <img src="https://haowallpaper.com/link/common/file/previewFileImg/15812065827459392">
            <p>标签：书房 夜晚 | 分类：自制 艺术 | 分辨率：4096x3070 | 大小：689K</p>
        </div><br/>
    </body>
</html>
    """

    area = Textarea(html_content)

    w = Widget(
        Row(area, margin='8'),
        size='1000',
    )

    w.show()
    app.exec()
