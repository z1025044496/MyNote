#

# 动画

## 动画元素

|元素|效果|
|---|---|
|PropertyAnimation（属性动画）|使用属性值改变播放的动画|
|NumberAnimation（数字动画）|使用数字改变播放的动画|
|ColorAnimation（颜色动画）|使用颜色改变播放的动画|
|RotationAnimation（旋转动画）|使用旋转改变播放的动画|
|PauseAnimation（停止动画）|运行暂停一个动画|
|SequentialAnimation（顺序动画）|允许动画有序播放|
|ParallelAnimation（并行动画）|允许动画同时播放|
|AnchorAnimation（锚定动画）|使用锚定改变播放的动画|
|ParentAnimation（父元素动画）|使用父对象改变播放的动画|
|SmotthedAnimation（平滑动画）|跟踪一个平滑值播放的动画|
|SpringAnimation（弹簧动画）|跟踪一个弹簧变换的值播放的动画|
|PathAnimation（路径动画）|跟踪一个元素对象的路径的动画|
|Vector3dAnimation（3D容器动画）|使用QVector3d值改变播放的动画|

当使用更加复杂的动画时，我们可能需要在播放动画时中改变属性或者运行脚本。

|动作元素|效果|
|---|---|
|PropertyAction（属性动作）|在播放动画时改变属性|
|ScriptAction（脚本动作）|在播放动画时运行脚本|