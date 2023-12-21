# 

`QQuickImageProvider`提供了一种更加好用的图像加载方式（**QML限定**），和直接通过`Image.source`加载主要有以下几方面差异

1. 加载方式差异

* 相比本地资源的加载方式：`source : "qrc:///前缀/demo.jpg"`。
* ImageProvider方式: `source : "image://imageproviderid/image id"`。

2. 更好用

* 异步加载，不会阻塞UI线程
* 可以加载内存图像（QPixmap）

# 例子说明

## 1、定义一个继承于QQuickImageProvider类的图像提供程序并实现，注意需要重写requestPixmap或函数requestImage

myimageprovider.h

```cpp
#ifndef MYIMAGEPROVITER_H
#define MYIMAGEPROVITER_H
#include <QQuickImageProvider>

class MyImageProviter:public QQuickImageProvider    //图像提供程序
{
public:
    MyImageProviter() : QQuickImageProvider(QQuickImageProvider::Pixmap)    //构造函数
    {

    }

    QPixmap requestPixmap(const QString &id, QSize *size, const QSize &requestedSize);  //重写requestPixmap函数
    QImage requestImage(const QString &id, QSize *size, const QSize &requestedSize);    //重写requestImage函数
};

#endif // MYIMAGEPROVITER_H
```

myimageprovider.cpp

```cpp
#include "myimageproviter.h"
#include <QPixmap>
#include <QCoreApplication>
#include <QPainter>
#include <QDebug>

//requestPixmap函数的重写，在qml中使用source加载图片时会自动调用requestPixmap或requestImage函数（根据图片类型不同），返回QPixmap或QImage对象
QPixmap MyImageProviter::requestPixmap(const QString &id, QSize *size, const QSize &requestedSize)
{
    QString s=":/ima/" + id;        //本地图片加载路径的拼接，根据id不同可以调用不同图片
    QPixmap pix;                //新建一个QPixmap对象
    pix.load(s);                //加载图片
    pix=pix.scaled(150,250);    //图片缩放
    return pix;                 //返回QPixmap对象
}

QImage MyImageProviter::requestImage(const QString &id, QSize *size, const QSize &requestedSize)
{
    QImage im;
    im.load(":/ima/R-C.png");
    return im;
}
```

## 2、使用QQmlEngine::addImageProvider 函数将图片提供类的对象（注册）到qml引擎中， 并且指定标识符， 该标识符在qml中使用。

main.cpp

```cpp
#include "myimageprovider.h"
 
int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);
 
    QQuickView view;
    QQmlEngine *engine = view.engine();
    MyImageProvider *imageProvider = new MyImageProvider();
    engine->addImageProvider("myprovider", imageProvider );
    view.setSource(QUrl(QStringLiteral("qrc:///Main.qml")));
    view.setResizeMode(QQuickView::SizeRootObjectToView);
    view.show();
    return app.exec();
}
```

## 3、在qml中调用加载图片

需要使用 source: "image://标识符/图片id" 的格式来加载

main.qml

```qml
//Image图片控件
Image 
{
    id: hhhhh
    x:200
    y:200
    // width: 135
    // height: 150
    // sourceSize.width: 120
    // sourceSize.height: 120
    // 指定资源信息。会自动调用图片提供类的requestPixmap或requestImage函数，
    source: "image://ima33/R-C.png"
    // 将id、QSize等信息传给requestPixmap或requestImage函数的形参，返回QPixmap或QImage对象，并自动把图片画出来（加载出来）
    // source: "image://标识符/图片id" 
}
```