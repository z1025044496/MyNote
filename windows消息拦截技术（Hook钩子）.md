# 什么是钩子（hook）

钩子（Hook）是Windows消息处理机制的一个很重要的内容，谁叫Windows是基于消息的呢。应用程序可以通过钩子机制截获处理Window消息或是其他一些特定事件。  

当事件发生时，应用程序可以在相应的钩子Hook上设置多个钩子子程序（Hook Procedures），由其组成一个与钩子相关联的指向钩子函数的指针列表（钩子链表）。当钩子所监视的消息出现时，Windows首先将其送到调用链表中所指向的第一个钩子函数中,钩子函数将根据其各自的功能对消息进行监视、修改和控制，并在处理完成后把消息传递给下一钩子函数直至到达钩子链表的末尾。在钩子函数交出控制权后，被拦截的消息最终仍将交还给窗口处理函数  

# 钩子作用域

大多数人或者网上文章认为全局钩子都要依赖于一个DLL才能正常工作的，常常会看到很多人在论坛上长期争论一个话题：“全局钩子一定要在DLL里面吗？”。实际上这里有一个概念的问题，究竟上面提到的全局钩子是指什么。通过对上面各种钩子的作用域的理解就会发现这个问题的答案。  

上面一共提到了15种钩子，他们的作用域请看下表： 

|Hook|Scope|
|---|---|
|WH_CALLWNDPROC|Thread or global|
|WH_CALLWNDPROCRET|Thread or global|
|WH_CBT|Thread or global|
|WH_DEBUG|Thread or global|
|WH_FOREGROUNDIDLE|Thread or global|
|WH_GETMESSAGE|Thread or global|
|WH_JOURNALPLAYBACK|Global only|
|WH_JOURNALRECORD|Global only|
|WH_KEYBOARD|Thread or global|
|WH_KEYBOARD_LL|Global only|
|WH_MOUSE|Global only|
|WH_MOUSE_LL|Global only|
|WH_MSGFILTER|Thread or global|
|WH_SHELL|Thread or global|
|WH_SYSMSGFILTER|Global only|

WH_JOURNALPLAYBACK，WH_JOURNALRECORD，WH_KEYBOARD_LL，WH_MOUSE_LL、WH_SYSMSGFILTER这5种钩子本身的作用域就是全局的，不管钩子是直接写在应用程序的代码里还是放在DLL中，他们都能够钩住系统的消息。剩下的10种钩子，他们的作用域既可以是线程的又可以是全局的，当将相应的钩子直接写在应用程序的代码中时，他们只能捕获当前线程上下文的消息。那么他们如何实现捕获全局消息的功能呢？当把钩子写入到一个单独的DLL中再引用后，系统自动将该DLL映射到受钩子函数影响的所有进程的地址空间中，即将这个DLL注入了那些进程，从而达到捕获全局消息的目的。相对来说，前面5种钩子本身就是全局的，是不需要注入的。

因此，对于前面问题的答案就是：要实现捕获全局消息功能的钩子，是否要写在单独的DLL里面，取决于钩子的类型以及相应的作用域。

如果对于同一事件既安装了线程勾子又安装了全局勾子，那么系统会自动先调用线程勾子，然后调用全局勾子。

# 钩子工程

为了利用某种特定类型的钩子，开发者提供了钩子子程。可以使用`SetWindowsHookEx`方法将该钩子子程安装到和该钩子相关联的钩子链表中。钩子子程必须具有下面的语法：

```c++
LRESULT CALLBACK HookProc
(
    int nCode, 
    WPARAM wParam, 
    LPARAM lParam
);
```
参数nCode：钩子代码，钩子子程通过该代码来决定执行什么动作。该值取决于钩子的类型，每种类型都拥有自己特有的钩子代码集合。

参数wParam和lParam的值，都取决于钩子代码。但是一般都包含发送或者传递的消息的信息。

`SetWindowsHookEx`总是在钩子链的开始位置安装钩子子程。当被某种类型的钩子监视的事件发生时，系统调用和该钩子相关的位于钩子链表开始位置的钩子子程。每个钩子链表中的钩子子程决定是否将该事件传递给下一个钩子子程。钩子子程通过调用方法`CallNextHookEx`向下一个钩子子程传递事件。

注意：某些类型的钩子子程仅仅能够监视消息，系统不管是否有特殊的钩子子程调用CallNextHookEx方法，都将把消息传递给每个钩子子程，

上面的字面意思为：全局钩子监视同一桌面下所有做为调用线程的线程消息。线程钩子仅仅监视该单个线程的消息。全局钩子子程可以在所在桌面下任何应用程序的上下文中被调用，因此，该钩子子程序须在一个单独的动态链接库DLL中。(译者注：在DLL中，可以映射到内存中，从而被所有程序调用)。线程钩子的钩子子程只能在本线程的上下文中被调用。如果应用程序为他自己线程中的某个安装钩子子程，钩子子程能够放在本模块中、应用程序代码的其它部分、Dll中。如果应用程序为另外一个不同的应用程序安装钩子子程，钩子子程必须放在Dll中。参照 DLL 查找更多信息。

# 钩子类型

1. `WH_CALLWNDPROC `和`WH_CALLWNDPROCRET`：WH_CALLWNDPROC 和 WH_CALLWNDPROCRET钩子使你能够监视发送到window程序的消息。系统在将消息传递给正在接收的window程序之前，调用WH_CALLWNDPROC钩子子程；在window程序处理完消息之后，调用WH_CALLWNDPROCRET钩子子程。

2. `WH_CBT `: 在以下事件发生之前，系统会调用WH_CBT 钩子子程：

    * 窗口被激活、创建、销毁、最小化、最大化、移动或者改变大小；

    * 执行完系统命令；

    * 从系统消息队列中移除鼠标或者键盘事件；

    * 设置输入焦点；

    * 同步系统消息队列；

钩子子程的返回值决定了系统是允许了还是阻止了这些操作中的一个。WH_CBT钩子主要是用在CBT 程序中。

3. `WH_DEBUG`：
在调用与系统中任何其他钩子关联的钩子子程之前，系统会调用WH_DEBUG 钩子子程。使用该钩子来决定是否允许系统调用与其他类型的钩子相关联的钩子子程。(我的理解是调试钩子的钩子)

4. `WH_FOREGROUNDIDLE`： 
WH_FOREGROUNDIDLE 钩子允许当前台线程空闲时，执行低权限的任务。系统在应用程序的前台线程即将空闲时，调用WH_FOREGROUNDIDLE钩子子程。

5. `WH_GETMESSAGE`：
WH_GETMESSAGE程序允许应用程序监视即将由方法GetMessage 或者PeekMessage返回的消息。可以使用WH_GETMESSAGE钩子监视鼠标和键盘输入，以及其他传递给消息队列的消息。

6. `WH_JOURNALPLAYBACK`：WH_JOURNALPLAYBACK钩子允许应用程序将消息插入到系统消息队列中。使用该钩子回放先前使用WH_JOURNALRECORD 钩子记录的一系列鼠标和键盘事件。在WH_JOURNALPLAYBACK被安装后，常规的鼠标和键盘输入被禁用。WH_JOURNALPLAYBACK钩子是全局钩子，不能被用作线程钩子。WH_JOURNALPLAYBACK钩子返回一个超时值。该值告诉系统在处理来自回放钩子的当前消息之前等待了多少毫秒。这允许该钩子控制回放事件的速度。

7. `WH_JOURNALRECORD`：WH_JOURNALRECORD钩子允许监视并且记录输入事件。典型的，使用该钩子来记录顺序的的鼠标和键盘事件，以后可以使用WH_JOURNALPLAYBACK.钩子进行回放。 该钩子是全局钩子，不能被用作进程钩子。

8. `WH_KEYBOARD_LL`：WH_KEYBOARD_LL钩子监视在线程输入队列中，即将被传递的键盘输入事件。

9. `WH_KEYBOARD`：WH_KEYBOARD钩子允许应用程序监视即将被GetMessage 或者PeekMessage方法返回的WM_KEYDOWN 或者 WM_KEYUP消息。使用WH_KEYBOARD钩子可以监视传递到消息队列中的键盘输入。

10. `WH_MOUSE_LL`：WH_MOUSE_LL钩子监视在线程输入队列中，即将被传递的鼠标输入事件。

11. `WH_MOUSE`：WH_MOUSE钩子允许监视即将被GetMessage或者 PeekMessage方法返回的鼠标消息。使用该钩子监视传递到线程输入队列的鼠标输入。

12. `WH_MSGFILTER`和`WH_SYSMSGFILTER`：WH_MSGFILTER 和 WH_SYSMSGFILTER钩子允许监视即将由菜单、滚动条、消息框、对话框处理的消息，并且在用户按下了ALT+TAB 或者ALT+ESC组合键后，检测何时一个不同的窗口将被激活。WH_MSGFILTER钩子仅仅能监视传递到菜单、滚动条、消息框或者由安装了钩子子程的应用程序建立的对话框的消息。WH_SYSMSGFILTER钩子监视所有应用程序的这类消息。  
WH_MSGFILTER 和WH_SYSMSGFILTER钩子允许在模式循环期间执行消息过滤，这和在主消息循环中执行过滤是等效的。例如，应用程序在它从队列中收到消息到分派消息期间，经常在主循环中检查新的消息，执行适当的处理。然而，在模式循环期间，系统会收到、分派消息，但是并不给应用程序机会去过滤主消息循环中的消息。如果应用程序安装了WH_MSGFILTER 或者 WH_SYSMSGFILTER钩子子程，系统会在模式循环期间调用钩子子程。  
应用程序可以通过调用CallMsgFilter方法直接调用WH_MSGFILTER钩子。通过使用该方法，应用程序可以像在主消息循环中一样，使用同样的代码来过滤消息。这样做呢，可以在WH_MSGFILTER钩子子程中封装过滤的操作，在调用GetMessage和 DispatchMessage方法期间调用CallMsgFilter。  
```c++
while (GetMessage(&msg, (HWND) NULL, 0, 0))
{
    if (!CallMsgFilter(&qmsg, 0))
    {
        DispatchMessage(&qmsg);
    }
}
```
CallMsgFilter的最后一个参数简单的传递给钩子子程；可以输入任何值。钩子子程，通过定义像MSGF_MAINLOOP一样的常量，可以使用该值来决定钩子子程是被哪里调用的。

`WH_SHELL`： shell application可以使用WH_SHELL钩子来接收重要的通知。当shell application即将被激活时、当处在最顶层的窗口被创建或者销毁时，系统会调用WH_SHELL钩子子程。  
注意：常规shell application并不接收WH_SHELL消息。因此，任何将自己注册为默认外壳的应用程序必须在它（或者任何其它应用程序）能够接收WH_SHELL消息之前调用带有SPI_SETMINIMIZEDMETRICS 的SystemParametersInfo方法。

# 各类钩子工程回调函数

1. CallMsgFilter
   
   CallMsgFilter方法传递特定的消息和钩子代码到与WH_SYSMSGFILTER 和WH_MSGFILTER钩子相关联的钩子子程。 WH_SYSMSGFILTER或者WH_MSGFILTER钩子子程是应用程序定义的回调函数，该回调函数用来检验、选择、修改传递给对话框、消息框、菜单或者滚动条的消息，

   ```c++
   BOOL CallMsgFilter(LPMSG lpMsg, int nCode);
   /*
   lpMsg: 指向MSG结构的指针，该结构包含有即将传递给钩子子程的消息。
   nCode: 指定应用程序定义的代码，钩子子程使用该代码来决定如何处理消息。该代码不能与系统定义的与WH_SYSMSGFILTER 和 WH_MSGFILTER钩子相关的钩子代码(MSGF_ and HC_)相同。
   Return Value: 如果应用程序应该进一步处理该消息，返回值为0；如果不处理，返回非0值。
   Remarks: 系统调用CallMsgFilter方法来允许应用程序检查、控制在对话框、消息框、菜单、滚动条内部处理中的消息的流动，或者当用户通过按下ALT+TAB组合键激活不同的窗口时的信息流动。
   */
   ```

2. CallNextHookEx 
   `CallNextHookEx`方法将钩子信息传递给当前钩子链表中的下一个钩子子程。钩子子程能够在处理钩子信息之前或者之后调用该方法。

   ```c++
   LRESULT CallNextHookEx(HHOOK hhk, int nCode, WPARAM wParam, LPARAM lParam);
   /*
   hhk: 忽略
   nCode/wParam/Param: 这三个参数分别指定传递给当前钩子子程的code/wParam/lParam值。参数的意义取决于与当前钩子链表相关联的钩子类型。
   Return Value: 该值由钩子链表中的下一个钩子子程返回。当前钩子子程也必须返回该值。返回值的意义取决于钩子类型。
   Remarks: 钩子子程为了特定的钩子类型而被安装。CallNextHookEx方法调用钩子链表中的下一个钩子。调用CallNextHookEx是可选的，但是强烈要求调用该函数；否则，其他已经安装有钩子的应用程序将收不到钩子通知，从而可能导致不正确的行为。除非绝对需要阻止通知被其他应用程序看到，其它情况下都应该调用CallNextHookEx方法。
   */
   ```