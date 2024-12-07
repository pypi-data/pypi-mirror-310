from fluentui.gui import Font
from fluentui.widgets import App, Widget, Textarea, Row

if __name__ == '__main__':
    print()
    app = App(font=Font(pixel=14))

    html_content = """
<html>
    <style>
        .hor-center { text-align: center; }
    </style>
    <body>
        <p>美丽的图片</p>
        
        <div class="hor-center">
            <img src="https://w.wallhaven.cc/full/vq/wallhaven-vq6x28.jpg">
            <p>标签：女性 裙子 | 分类：人物 | 分辨率：2000×1429 | 大小： 918K</p>
        </div><br/>
        
        <div class="hor-center">
            <img src="https://haowallpaper.com/link/common/file/previewFileImg/15851046182949184">
            <p>标签：孤独摇滚 波奇酱 | 分类：动漫 二次元 | 分辨率：4096x2692 | 大小：319K</p>
        </div><br/>
        
        <div class="hor-center">
            <img src="https://haowallpaper.com/link/common/file/previewFileImg/15812065827459392">
            <p>标签：书房 夜晚 | 分类：自制 艺术 | 分辨率：4096x3070 | 大小：689K</p>
        </div><br/>
    </body>
</html>
    """

    w = Widget(
        Row(Textarea(html_content), margin='8'),
        size='1438,1048',
    )

    w.show()
    app.exec()
