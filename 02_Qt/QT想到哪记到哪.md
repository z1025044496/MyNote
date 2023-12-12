# 创建QNetworkAccessManager对象

## 注意事项

1. Qt网络访问 API 是围绕 QNetworkAccessManager 对象构建的，该对象保存它发送的请求的通用配置和设置。一个 QNetworkAccessManager 实例应该足以满足整个 Qt 应用程序网络访问的需求。 由于 QNetworkAccessManager 是基于 QObject 的，所以只能在它所属的线程中使用。 
    
2. 一旦创建了 QNetworkAccessManager 对象，应用程序就可以使用它通过网络发送请求。它提供了一组标准函数，它们接受一个请求和可选数据，每个函数都返回一个 QNetworkReply 对象。返回的对象用于获取响应相应请求而返回的任何数据。 
> 可以通过以下方式完成简单的网络下载：
> ```cpp
> QNetworkAccessManager *manager = new QNetworkAccessManager(this);
> connect(manager, &QNetworkAccessManager::finished, this, &MyClass::replyFinished);
> manager->get(QNetworkRequest(QUrl("http://qt-project.org")));
> ```
3. NetworkAccessManager 有一个异步 API。 当上面的 `replyFinished` 槽函数被调用时，它采用的参数是 QNetworkReply 对象，包含下载的数据以及元数据（标题等）。  
> 注意：请求完成后，用户有责任在适当的时候删除 QNetworkReply 对象。不要在连接到finished()的slot里面直接删除，可以使用 `deleteLater()` 函数。  
注意： QNetworkAccessManager 将它收到的请求排入队列。 并行执行的请求数量取决于协议。 目前，对于桌面平台上的 HTTP 协议，一个主机/端口组合并行执行 6 个请求。  
```c++
 QNetworkRequest request;
 request.setUrl(QUrl("http://qt-project.org"));
 request.setRawHeader("User-Agent", "MyOwnBrowser 1.0");
 
 QNetworkReply *reply = manager->get(request);
 connect(reply, &QIODevice::readyRead, this, &MyClass::slotReadyRead);
 connect(reply, &QNetworkReply::errorOccurred,this, &MyClass::slotError);
 connect(reply, &QNetworkReply::sslErrors,this, &MyClass::slotSslErrors);
```

## 函数

1. void setTransferTimeout(int timeout = QNetworkRequest::DefaultTransferTimeoutConstant)  
> 设置传输超时时间。如果在超时到期之前没有传输字节，传输将被中止。  
> 零表示未设置计时器。如果未调用此函数，则超时将被禁用且值为 0。

2. **[signal]** void finished(QNetworkReply *reply)
> 网络回复完成时会发出此信号。回复参数将包含一个指向刚刚完成的回复的指针。该信号与 QNetworkReply::finished() 信号一起发出。  
> 注意：不要直接删除连接到该信号的槽中的回复对象。应使用 deleteLater()。

# 创建QNetworkRequest对象，设置请求URL和请求头

1. void setUrl(const Qurl &url)  
> 设置此网络请求所指的URL  

2. void setRawHeader(const QByteArray &headerName, const QByteArray &headerValue)
> 设置表头的值。两次设置相同的标题会覆盖之前的设置。要完成多个同名 HTTP 标头的行为，应该连接这两个值，用逗号 (",") 分隔它们并设置一个原始标头。  
```c++
request.setRawHeader(QByteArray("Last-Modified"), QByteArray("Sun, 06 Nov 1994 08:49:37 GMT"));
```

3. void setTransferTimeout(int timeout = DefaultTransferTimeoutConstant)
> 设置传输超时时间（毫秒）。如果在超时到期之前没有传输字节，传输将被中止。零表示未设置计时器。 如果未提供参数，则超时为 QNetworkRequest::DefaultTransferTimeoutConstant。如果未调用此函数，则超时将被禁用且值为 0。  
> 注意：Qt5.1以上支持

# 使用QNetworkAcessManager的get()、post()、put()等函数发送请求

# 处理QNetworkReply对象以获取相应数据

## 注意事项

QNetworkReply 类封装了使用 QNetworkAccessManager 发布的请求相关的回复信息。

QNetworkReply 是 QIODevice的子类，这意味着一旦从对象中读取数据，它就不再由设备保留。因此，如果需要，应用程序有责任保留这些数据。

注意：不要删除连接到errorOccurred() 或finished() 信号的槽中的对象。应该使用使用 deleteLater()。

## 错误码

* `NoError`：**没有错误**。（当 HTTP 协议返回重定向时，不会报告错误。可以使用 QNetworkRequest::RedirectionTargetAttribute 属性检查是否存在重定向）
* `ConnectionRefusedError`：**远程服务器拒绝连接**。
* `RemoteHostClosedError`：**远程服务器在接收和处理整个回复之前过早关闭了连接**。
* `HostNotFoundError`：**未找到远程主机名（无效主机名）**。
* `TimeoutError`：**与远程服务器的连接超时**。
* `OperationCanceledError`：**操作在完成之前通过调用 abort() 或 close() 被取消**。
* `SslHandshakeFailedError`：**SSL/TLS 握手失败，无法建立加密通道。 sslErrors() 信号应该已经发出**。
* `TemporaryNetworkFailureError`：**由于与网络断开连接，连接中断，但系统已开始漫游到另一个接入点。 应重新提交请求，并在重新建立连接后立即进行处理**。
* `NetworkSessionFailedError`：**由于与网络断开连接或无法启动网络，连接中断**。
* `BackgroundRequestNotAllowedError`：**由于平台政策，当前不允许后台请求**。
* `TooManyRedirectsError`：**在跟随重定向时，达到了最大限制。 该限制默认设置为 50 或由NetworkRequest::setMaxRedirectsAllowed() 设置**。
* `InsecureRedirectError`：**在跟踪重定向时，网络访问 API 检测到从加密协议 (https) 到未加密协议 (http) 的重定向**。
* `ProxyConnectionRefusedError`：**与代理服务器的连接被拒绝（代理服务器不接受请求）**。  
* `ProxyConnectionClosedError`：**代理服务器在接收和处理整个回复之前过早地关闭了连接**。
* `ProxyNotFoundError`：**未找到代理主机名（无效的代理主机名）**。  
* `ProxyTimeoutError`：**与代理的连接超时或代理没有及时回复发送的请求**。
* `ProxyAuthenticationRequiredError`：**代理需要身份验证才能满足请求，但不接受任何提供的凭据（如果有）**。  
* `ContentAccessDenied`：**对远程内容的访问被拒绝**（类似于 HTTP 错误 403）。
* `ContentOperationNotPermittedError`：**不允许对远程内容请求的操作**。
* `ContentNotFoundError`：**在服务器上找不到远程内容**（类似于 HTTP 错误 404）。  
* `AuthenticationRequiredError`：**远程服务器需要身份验证才能提供内容，但不接受提供的凭据（如果有）**。  
* `ContentReSendError`：**需要再次发送请求，但由于无法再次读取上传数据而失败**。  
* `ContentConflictError`：**由于与资源的当前状态冲突，无法完成请求**。  
* `ContentGoneError`：**请求的资源在服务器上不再可用**。  
* `InternalServerError`：**服务器遇到意外情况，无法完成请求**。  
* `OperationNotImplementedError`：**服务器不支持满足请求所需的功能**。  
* `ServiceUnavailableError`：**服务器此时无法处理请求**。  
* `ProtocolUnknownError`：**网络访问 API 无法接受请求，因为协议未知**。  
* `ProtocolInvalidOperationError`：**请求的操作对该协议无效**。  
* `UnknownNetworkError`：**检测到与网络相关的未知错误**。  
* `UnknownProxyError`：**检测到与代理相关的未知错误**。  
* `UnknownContentError`：**检测到与远程内容相关的未知错误**。  
* `ProtocolFailure`：**检测到协议故障**（解析错误、无效或意外响应等）。  
* `UnknownServerError`：**检测到与服务器响应相关的未知错误**。

## 函数

1. void abort()
> 立即中止操作并关闭所有仍打开的网络连接。仍在进行中的上传会中止，`finished()` 信号也将被发射。   
