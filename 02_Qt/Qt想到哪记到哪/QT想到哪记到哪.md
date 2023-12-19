#

# post/get/put网络通信

## 1. 创建QNetworkAccessManager对象

### 注意事项

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

### 函数

1. void setTransferTimeout(int timeout = QNetworkRequest::DefaultTransferTimeoutConstant)  
> 设置传输超时时间。如果在超时到期之前没有传输字节，传输将被中止。  
> 零表示未设置计时器。如果未调用此函数，则超时将被禁用且值为 0。

2. **[signal]** void finished(QNetworkReply *reply)
> 网络回复完成时会发出此信号。回复参数将包含一个指向刚刚完成的回复的指针。该信号与 QNetworkReply::finished() 信号一起发出。  
> 注意：不要直接删除连接到该信号的槽中的回复对象。应使用 deleteLater()。

## 2. 创建QNetworkRequest对象，设置请求URL和请求头

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

## 3. 使用QNetworkAcessManager的get()、post()、put()等函数发送请求

## 4. 处理QNetworkReply对象以获取相应数据

### 注意事项

QNetworkReply 类封装了使用 QNetworkAccessManager 发布的请求相关的回复信息。

QNetworkReply 是 QIODevice的子类，这意味着一旦从对象中读取数据，它就不再由设备保留。因此，如果需要，应用程序有责任保留这些数据。

注意：不要删除连接到errorOccurred() 或finished() 信号的槽中的对象。应该使用使用 deleteLater()。

### 错误码

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

### 函数

1. void abort()

> 立即中止操作并关闭所有仍打开的网络连接。仍在进行中的上传会中止，`finished()` 信号也将被发射。   

2. void ignoreSslErrors()

> 如果调用此函数，将忽略与网络连接相关的 SSL 错误，包括证书验证错误。

> [!WARRING]
> 应确保始终让用户检查`sslErrors()`信号报告的错误，并且只有在用户确认继续正常后才调用此方法。如果出现意外错误，则应中止回复。在不检查实际错误的情况下调用此方法很可能会给应用程序带来安全风险。应小心使用此函数！
> 可以从连接到`sslErrors()`信号的插槽调用此函数，该信号指示发现了哪些错误。

> [!NOTE]
> 如果`QNetworkAccessManager`启用了`HTTP Strict Transport Security`，则此功能无效。

3. void close()

> 关闭此设备。未读的数据会被丢弃，但网络资源直到读完才被释放。如果有任何上传正在进行，它将一直持续到完成。当所有操作结束并且网络资源被释放时，`finished()`信号被发出。

4. bool hasRawHeader(const QByteArray &headerName)

> 如果名称`headerName`的原始标头是由远程服务器发送的，则返回 true。

5. void ignoreSslErrors(const QList<QSslError> &errors)
> 列表中给出的 SSL 错误将被忽略。

> [!NOTE]
> 由于大多数SSL错误都与证书相关联，因此对于其中的大多数错误，必须设置与SSL错误相关的预期证书。例如，如果您想向使用自签名证书的服务器发出请求，请考虑以下代码段：

```cpp
 QList<QSslCertificate> cert = QSslCertificate::fromPath(QLatin1String("server-certificate.pem"));
 QSslError error(QSslError::SelfSignedCertificate, cert.at(0));
 QList<QSslError> expectedSslErrors;
 expectedSslErrors.append(error);
 
 QNetworkReply * reply = manager.get(QNetworkRequest(QUrl("https://server.tld/index.html")));
 reply->ignoreSslErrors(expectedSslErrors);
 ```

# QFileSystemWatcher类

`QFileSystemWatcher`类用于提供**监视文件和目录修改**的接口。

`QFileSystemWatcher`通过监控指定路径的列表，监视文件系统中文件和目录的变更。

调用`addPath()`函数可以监控一个特定的文件或目录。如果需要监控多个路径，可以使用`addPaths()`。通过使用`removePath()`和`removePaths()`函数来移除现有路径。

`QFileSystemWatcher`检查添加到它的每个路径，已添加到`QFileSystemWatcher`的文件可以使用的`files()`函数进行访问，目录则使用`directories()`函数进行访问。

当一个文件被修改、重命名或从磁盘上删除时，会发出`fileChanged()`信号。同样，当一个目录或它的内容被修改或​​删除时，会发射`directoryChanged()`信号。需要注意：文件一旦被重命名或从硬盘删除，目录一旦从磁盘上删除，`QFileSystemWatcher`将停止监控。

> [!NOTE]
> 监控文件和目录进行修改的行为会消耗系统资源。这意味着，你的进程同时监控会有文件数量的限制。一些系统限制打开的文件描述符的数量默认为256。也就是说，如果你的进程试使用addPath()和addPaths()函数添加超过256个文件或目录到文件系统将会失败。

## 公共函数

1. bool addPath(const QString & path)

> 如果路径存在，则添加至文件系统监控，如果路径不存在或者已经被监控了，那么不添加。

* 如果路径是一个目录，内容被修改或​​删除时，会发射directoryChanged()信号；否则，当文件被修改、重命名或从磁盘上删除时，会发出fileChanged()信号。
* 如果监控成功，返回true；否则，返回false.
* 监控失败的原因通常依赖于系统，但也包括资源不存在、接入失败、或总的监控数量限制等原因。

2. QStringList addPaths(const QStringList & paths)

> 添加每一个路径至添加至文件系统监控，如果路径不存在或者已经被监控了，那么不添加。

* 返回值是不能被监控的路径列表。

3. QStringList directories() const

> 返回一个被监控的目录路径列表。

4. QStringList files() const

> 返回一个被监控的文件路径列表。

5. bool removePath(const QString & path)

> 从文件系统监控中删除指定的路径。如果监控被成功移除，返回true。

* 删除失败的原因通常是与系统相关，但可能是由于路径已经被删除。

6. QStringList removePaths(const QStringList & paths)

> 从文件系统监控中删除指定的路径。返回值是一个无法删除成功的路径列表。

## 信号

1. void fileChanged(const QString & path)

> 当在指定路径中的文件被修改、重命名或从磁盘上删除时，这个信号被发射。

2. void directoryChanged(const QString & path)

> 当在指定路径中的文件被修改、重命名或从磁盘上删除时，这个信号被发射。

> [!DANGER]
> 以上两个信号均为私有信号，可以用于信号连接但不能由用户发出。

## 实例

FileSystemWatcher.h

```cpp
#ifndef FILE_SYSTEM_WATCHER_H
#define FILE_SYSTEM_WATCHER_H

#include <QObject>
#include <QMap>
#include <QFileSystemWatcher>

class FileSystemWatcher : public QObject
{
    Q_OBJECT

public:
    static void addWatchPath(QString path);

public slots:
    void directoryUpdated(const QString &path);  // 目录更新时调用，path是监控的路径
    void fileUpdated(const QString &path);   // 文件被修改时调用，path是监控的路径

private:
    explicit FileSystemWatcher(QObject *parent = 0);

private:
    static FileSystemWatcher *m_pInstance; // 单例
    QFileSystemWatcher *m_pSystemWatcher;  // QFileSystemWatcher变量
    QMap<QString, QStringList> m_currentContentsMap; // 当前每个监控的内容目录列表
};

#endif // FILE_SYSTEM_WATCHER_H
```

FileSystemWatcher.cpp

```cpp
#include <QDir>
#include <QFileInfo>
#include <qDebug>
#include "FileSystemWatcher.h"

FileSystemWatcher* FileSystemWatcher::m_pInstance = NULL;

FileSystemWatcher::FileSystemWatcher(QObject *parent)
    : QObject(parent)
{

}

// 监控文件或目录
void FileSystemWatcher::addWatchPath(QString path)
{
    qDebug() << QString("Add to watch: %1").arg(path);

    if (m_pInstance == NULL)
    {
        m_pInstance = new FileSystemWatcher();
        m_pInstance->m_pSystemWatcher = new QFileSystemWatcher();

        // 连接QFileSystemWatcher的directoryChanged和fileChanged信号到相应的槽
        connect(m_pInstance->m_pSystemWatcher, SIGNAL(directoryChanged(QString)), m_pInstance, SLOT(directoryUpdated(QString)));
        connect(m_pInstance->m_pSystemWatcher, SIGNAL(fileChanged(QString)), m_pInstance, SLOT(fileUpdated(QString)));
    }

    // 添加监控路径
    m_pInstance->m_pSystemWatcher->addPath(path);

    // 如果添加路径是一个目录，保存当前内容列表
    QFileInfo file(path);
    if (file.isDir())
    {
        const QDir dirw(path);
        m_pInstance->m_currentContentsMap[path] = dirw.entryList(QDir::NoDotAndDotDot | QDir::AllDirs | QDir::Files, QDir::DirsFirst);
    }
}

// 只要任何监控的目录更新（添加、删除、重命名），就会调用。
void FileSystemWatcher::directoryUpdated(const QString &path)
{
    qDebug() << QString("Directory updated: %1").arg(path);

    // 比较最新的内容和保存的内容找出区别(变化)
    QStringList currEntryList = m_currentContentsMap[path];
    const QDir dir(path);

    QStringList newEntryList = dir.entryList(QDir::NoDotAndDotDot  | QDir::AllDirs | QDir::Files, QDir::DirsFirst);

    QSet<QString> newDirSet = QSet<QString>::fromList(newEntryList);
    QSet<QString> currentDirSet = QSet<QString>::fromList(currEntryList);

    // 添加了文件
    QSet<QString> newFiles = newDirSet - currentDirSet;
    QStringList newFile = newFiles.toList();

    // 文件已被移除
    QSet<QString> deletedFiles = currentDirSet - newDirSet;
    QStringList deleteFile = deletedFiles.toList();

    // 更新当前设置
    m_currentContentsMap[path] = newEntryList;

    if (!newFile.isEmpty() && !deleteFile.isEmpty())
    {
        // 文件/目录重命名
        if ((newFile.count() == 1) && (deleteFile.count() == 1))
        {
            qDebug() << QString("File Renamed from %1 to %2").arg(deleteFile.first()).arg(newFile.first());
        }
    }
    else
    {
        // 添加新文件/目录至Dir
        if (!newFile.isEmpty())
        {
            qDebug() << "New Files/Dirs added: " << newFile;

            foreach (QString file, newFile)
            {
                // 处理操作每个新文件....
            }
        }

        // 从Dir中删除文件/目录
        if (!deleteFile.isEmpty())
        {
            qDebug() << "Files/Dirs deleted: " << deleteFile;

            foreach(QString file, deleteFile)
            {
                // 处理操作每个被删除的文件....
            }
        }
    }
}

// 文件修改时调用
void FileSystemWatcher::fileUpdated(const QString &path)
{
    QFileInfo file(path);
    QString strPath = file.absolutePath();
    QString strName = file.fileName();

    qDebug() << QString("The file %1 at path %2 is updated").arg(strName).arg(strPath);
}
```