# Qml与C++混合编程

## 背景

组内界面开发为前后端分离，这个季度开始界面开始使用Qml开发，主要介绍Qml与C++之间的通信方法。

## 1. connect()函数链接qml中的信号（槽）与c++中的槽（信号）
所有QML对象类型都是源自QObject类型，无论它们是由引擎内部实现还是第三方定义。因此可以在c++中使用connect()函数对链接qml元对象中的信号（槽）与c++中的槽（信号）

> 示例代码：

rectangle.qml内设置了两个按钮，其中这一部分只会用到按钮1：

```qml
import QtQuick 2.9
import QtQuick.Controls 2.15

Rectangle
{
    id: root
    width: 120
    height: 240
    x: 0
    y: 0
    color: "white"
    
    property int colorNum_1: 0;
    property int colorNum_2: 0;
    property int colorNum_3: 0;
    
    signal firstButtnoClicked()
    signal secondButtnoClicked()
    
    function changeFirstBtnColor() {
        colorNum_1 = colorNum_1 + 1;
        if (colorNum_1 > 2) {
            colorNum_1 = 0;
        }
    }

    function changeSeconedBtnColor() {
        colorNum_2 = colorNum_2 + 1;
        if (colorNum_2 > 2) {
            colorNum_2 = 0;
        }
    }

    Button {
        id: firstButton
        text: qsTr("按钮1")
        width: 96
        height: 32
        anchors.left: root.left
        anchors.top: root.top
        background: Rectangle{
            color: {
                var colorVar="gray";
                if (colorNum_1===1) {
                    colorVar="blue"
                }else if (colorNum_1===2) {
                    colorVar="yellow"
                }
                return colorVar;
            }
            border.width: 1
            border.color: "red"
        }
        onClicked: {
            firstButtnoClicked();
        }
    }
    Button {
        id: secondButton
        text: qsTr("按钮2")
        width: 96
        height: 32
        anchors.left: firstButton.right
        anchors.top: root.top
        background: Rectangle{
            id: secondBtnColor
            color: "gray"
            border.width: 1
            border.color: "red"
        }
        onClicked: {
        }
    }
}
```

QML_learning是主窗口类，在这里链接信号与槽

QML_learning.h:

```cpp
#pragma once

#include <QtWidgets/QMainWindow>
#include "ui_QML_learning.h"

class QML_learning : public QMainWindow
{
	Q_OBJECT

public:
	QML_learning(QWidget *parent = Q_NULLPTR);

	void Init();

private:
	void InitUI();
	void InitConnects();

private:
	Ui::QML_learningClass ui;

	int m_nFirstBtnClickedNum = 0;

signals:
	void Sig_ChangeFirstBtnColor();

private slots:
	void Slt_FirstBtnClicked();
};
```

QML_learning.cpp:

```cpp
#include "QML_learning.h"
#include <QDebug>
#include <QQuickItem>
#include <QQmlContext>
#include <QQmlEngine>
#include "RegisterToQml.h"
#include "ConnectToQml.h"

QML_learning::QML_learning(QWidget *parent)
	: QMainWindow(parent)
{
	ui.setupUi(this);
}

void QML_learning::Init()
{
	InitUI();
	InitConnects();
}

void QML_learning::InitUI()
{
	QUrl source("qrc:/QML_learning/qml/rectangle.qml");
	ui.quickWidget->setResizeMode(QQuickWidget::SizeRootObjectToView);
	ui.quickWidget->setSource(source);
}

void QML_learning::InitConnects()
{
	bool bRet = false;
	bRet = connect(ui.quickWidget->rootObject(), SIGNAL(firstButtnoClicked()), this, SLOT(Slt_FirstBtnClicked()));
	bRet = connect(this, SIGNAL(Sig_ChangeFirstBtnColor()), ui.quickWidget->rootObject(), SLOT(changeFirstBtnColor()));
	return;
}

void QML_learning::Slt_FirstBtnClicked()
{
	QString strText = QString("按钮1被点击了%1次").arg(++m_nFirstBtnClickedNum);
	ui.label_1->setText(strText);
	emit Sig_ChangeFirstBtnColor();
}

```

上述代码是在qml中单击按钮后将信号传至cpp修改ui文本，然后将cpp中的信号传至qml修改按钮背景颜色。效果如下：

![](../Image/c++与qml信号槽直接连接.gif)

## 2. QML使用C++类

Qt官方文档中介绍，可以在C++代码中使用特定的宏和函数接口来拓展QML。由上一节所介绍的，所有QML对象类型都是源自QObject类型，可以从QML代码访问由QObject派生类的放开功能，这样C++类中的属性和方法可以直接从QML中访问。

任何QML代码都可以访问QObject派生类中的一下成员：
* 属性（需要使用Q_PROPERTY宏注册）
  
    Q_PROPERTY使用：

    ```cpp
    Q_PROPERTY(type name
               (READ getFunction [WRITE setFunction] |
               MEMBER memberName [(READ getFunction | WRITE setFunction)])
               [RESET resetFunction]
               [NOTIFY notifySignal]
               [REVISION int]
               [DESIGNABLE bool]
               [SCRIPTABLE bool]
               [STORED bool]
               [USER bool]
               [CONSTANT]
               [FINAL])
    ```
    > * 如果MEMBER关键字没有被指定，则一个READ访问函数是必须的。它被用来读取属性值。理想的情况下，一个const函数用于此目的，并且它必须返回的是属性类型或const引用。比如：QWidget::focus是一个只读属性，通过READ函数QWidget::hasFocus()访问。
    > * WRITE访问函数是可选的，用于设置属性的值。它必须返回void并且只能接受一个参数，属性的类型是类型指针或引用，例如：QWidget::enabled具有WRITE函数QWidget::setEnabled()。只读属性不需要WRITE函数，例如：QWidget::focus没有WRITE函数。
    > * 如果READ访问函数没有被指定，则MEMBER变量关联是必须的。这使得给定的成员变量可读和可写，而不需要创建READ和WRITE访问函数。如果需要控制变量访问，仍然可以使用READ和WRITE函数而不仅仅是MEMBER（但别同时使用）。
    > * RESET函数是可选的，用于将属性设置为上下文指定的默认值。例如：QWidget::cursor有READ和WRITE函数QWidget::cursor()和QWidget::setCursor()，同时也有一个RESET函数QWidget::unsetCursor()，因为没有可用的QWidget::setCursor()调用可以确定的将cursor属性重置为上下文默认的值。RESET函数必须返回void类型，并且不带任何参数。
    > * NOTIFY信号是可选的。如果定义了NOTIFY，则需要在类中指定一个已存在的信号，该信号在属性值发生改变时发射。与MEMBER变量相关的NOTIFY信号必须有零个或一个参数，而且必须与属性的类型相同。参数保存的是属性的新值。NOTIFY信号应该仅当属性值真正的发生变化时发射，以避免被QML重新评估。例如：当需要一个没有显式setter的MEMBER属性时，Qt会自动发射信号。
    > * REVISION数字是可选的。如果包含了该关键字，它定义了属性并且通知信号被特定版本的API使用（通常是QML）；如果没有包含，它默认为0。
    > * DESIGNABLE属性指定了该属性在GUI设计器（例如：Qt Designer）里的编辑器中是否可见。大多数的属性是DESIGNABLE （默认为true）。除了true或false，你还可以指定boolean成员函数。
    > * SCRIPTABLE属性表明这个属性是否可以被一个脚本引擎操作（默认是true）。除了true或false，你还可以指定boolean成员函数。
    > * STORED属性表明了该属性是否是独立存在的还是依赖于其它属性。它也表明在保存对象状态时，是否必须保存此属性的值。大多数属性是STORED（默认为true）。但是例如：QWidget::minmunWidth()的STROED为false，因为它的值从QWidget::minimumSize()（类型为QSize）中的width部分取得。
    > * USER属性指定了属性是否被设计为用户可见和可编辑的。通常情况下，每一个类只有一个USER属性（默认为false）。例如： QAbstractButton::checked是（checkable）buttons的用户可修改属性。注意：QItemDelegate获取和设置widget的USER属性。
    > * CONSTANT属性的出现表明属性是一个常量值。对于给定的object实例，常量属性的READ函数在每次被调用时必须返回相同的值。对于不同的object实例该常量值可能会不同。一个常量属性不能具有WRITE函数或NOYIFY信号。
    > * FINAL属性的出现表明属性不能被派生类所重写。有些情况下，这可以用于效率优化，但不能被moc强制执行。必须注意不能覆盖一个FINAL属性。

* 函数（public slots或Q_INVOKABLE注册的函数）
  > Q_INVOKABLE使用只需要在对应函数前声明即可
* 信号
  > 所有的信号都可以在QML中使用

将类注册到QML中需要用到`qmlRegisterType`函数，使用方法如下：
```cpp
#include <QtQml>
qmlRegisterType<RegisterToQml>("com.data.RegisterToQml", 1, 0, "RegisterToQml");
```

第一个参数`com.data.RegisterToQml`指的是QML中import后的内容，相当于模块名，第二个第三个参数分别是主次版本号，第四个`RegisterToQml`指的是QML中类的名字。

示例代码：

QML_Learning.cpp:

```cpp
void QML_learning::InitUI()
{
	qmlRegisterType<RegisterToQml>("com.data.RegisterToQml", 1, 0, "RegisterToQml");
	QUrl source("qrc:/QML_learning/qml/rectangle.qml");
	ui.quickWidget->setResizeMode(QQuickWidget::SizeRootObjectToView);
	ui.quickWidget->setSource(source);
}
```

RegisterToQml.h:

```cpp
#ifndef REGISTERTOQML_H
#define REGISTERTOQML_H

#include <QObject>

class RegisterToQml : public QObject
{
    Q_OBJECT
    Q_PROPERTY(int num MEMBER m_nNum WRITE setNum NOTIFY numChanged)
public:
    explicit RegisterToQml(QObject* parent = Q_NULLPTR);

    void setNum(const int nNum);

    Q_INVOKABLE void SecondBtnClicked();

signals:
    void numChanged(int nNum);

private: 
    int m_nNum = 0;

};

#endif // REGISTERTOQML_H
```

RegisterToQml.cpp:

```cpp
#include "RegisterToQml.h"

RegisterToQml::RegisterToQml(QObject* parent)
    : QObject(parent)
{
}

void RegisterToQml::setNum(const int nNum)
{
    m_nNum = nNum;
}

void RegisterToQml::SecondBtnClicked()
{
    ++m_nNum;
    emit numChanged(m_nNum);
}
```

rectangle.qml:

```qml
import com.data.RegisterToQml 1.0 // 版本号和模块名要和注册时保持一致

Rectangle
{
    // 定义元对象
    RegisterToQml {
        id: cppClass
    }

    Button {
        id: secondButton
        text: qsTr("按钮2")
        width: 96
        height: 32
        anchors.left: firstButton.right
        anchors.top: root.top
        background: Rectangle{
            id: secondBtnColor
            color: "gray"
            border.width: 1
            border.color: "red"
        }
        onClicked: {
            // 按钮2直接调用Q_INVOKABLE声明的函数
            connectionToCpp.SecondBtnClicked();
        }
    }

    Component.onCompleted: {
        // numChanged信号连接槽函数
        cppClass.numChanged.connect(onChangeSecondBtnColor);
    }

    function onChangeSecondBtnColor(num) {
        changeSeconedBtnColor();
        var colorVar="gray";
        if (colorNum_2===1) {
            colorVar="blue"
        }else if (colorNum_2===2) {
            colorVar="yellow"
        }
        secondBtnColor.color = colorVar;
    }
}

```

效果：
![](../Image/QML使用C++类.gif)

## 3. QML使用C++对象

QML使用C++对象的方式与QML使用C++类基本相同，仅仅在注册方式和使用上存在差异：

```cpp
QQmlContext::setContextProperty(const QString & name, QObject * object);
```

第一个参数`name`是注册到QML中的ID，第二个参数`object`是注册到QML中的对象指针。

使用时：

```qml
Connections {
    target: name
    // 假如其中类对象中定义了信号clicked
    function onClicked () {
        // 这里实现clicked的槽函数
    }
}
```

使用这种方式的好处是在QML中和C++中操作的是同一个对象，尤其注册的是一个单例对象的时候，可以随便操作。

示例代码：

QML_learning.cpp:

```cpp
void QML_learning::InitUI()
{
	// qmlRegisterType<RegisterToQml>("com.data.RegisterToQml", 1, 0, "RegisterToQml");
	QUrl source("qrc:/QML_learning/qml/rectangle.qml");
	ui.quickWidget->setResizeMode(QQuickWidget::SizeRootObjectToView);
	ui.quickWidget->setSource(source);
	ui.quickWidget->engine()->rootContext()->setContextProperty("connectionToCpp", ConnectToQml::GetInstance());
}

void QML_learning::InitConnects()
{
	bool bRet = false;
	bRet = connect(ui.quickWidget->rootObject(), SIGNAL(firstButtnoClicked()), this, SLOT(Slt_FirstBtnClicked()));
	bRet = connect(this, SIGNAL(Sig_ChangeFirstBtnColor()), ui.quickWidget->rootObject(), SLOT(changeFirstBtnColor()));
	bRet = connect(ConnectToQml::GetInstance(), SIGNAL(secondBtnClicked()), this, SLOT(Slt_SecondBtnClicked()));
	return;
}

void QML_learning::Slt_SecondBtnClicked()
{
	QString strText = QString("按钮2被点击了%1次").arg(++m_nSecondBtnClickedNum);
	ui.label_2->setText(strText);
}
```

ConnectToQml.h:

```cpp
#ifndef CONNECTTOQML_H
#define CONNECTTOQML_H

#include <QObject>

class ConnectToQml : public QObject
{
    Q_OBJECT
public:
    ConnectToQml(QObject* parent);

    static ConnectToQml* GetInstance();

    Q_INVOKABLE void SecondBtnClicked();

private:
    static ConnectToQml* m_pInstance;

signals: 
    void secondBtnClicked();
};

#endif // CONNECTTOQML_H
```

ConnectToQml.cpp:

```cpp
#include "ConnectToQml.h"

ConnectToQml* ConnectToQml::m_pInstance = nullptr;

ConnectToQml::ConnectToQml(QObject* parent)
    : QObject(parent)
{

}

ConnectToQml* ConnectToQml::GetInstance()
{
    if (m_pInstance == nullptr)
    {
        m_pInstance = new(std::nothrow) ConnectToQml(nullptr);
    }
    
    return m_pInstance;
}

void ConnectToQml::SecondBtnClicked()
{
    emit secondBtnClicked();
}
```

rectangle.qml
```qml
Rectangle
{
    Button {
        id: secondButton
        text: qsTr("按钮2")
        width: 96
        height: 32
        anchors.left: firstButton.right
        anchors.top: root.top
        background: Rectangle{
            id: secondBtnColor
            color: "gray"
            border.width: 1
            border.color: "red"
        }
        onClicked: {
            // cppClass.SecondBtnClicked();
            connectionToCpp.SecondBtnClicked();
        }
    }

    Connections {
        target: connectionToCpp
        function onSecondBtnClicked () {
            changeSeconedBtnColor();
            var colorVar="gray";
            if (colorNum_2===1) {
                colorVar="blue"
            }else if (colorNum_2===2) {
                colorVar="yellow"
            }
            secondBtnColor.color = colorVar;
        }
    }

    Component.onCompleted: {
        // cppClass.numChanged.connect(onChangeSecondBtnColor);
    }
}
```

效果：
![](../Image/QML使用C++对象.gif)