# 版本控制
> 版本迭代，管理多人开发的技术

* 实现跨区域多人协同开发
* 追踪和记载一个或多个文件的历史记录
* 组织和保护你的源代码和文档
* 统计工作量
* 并行开发、提高开发效率
* 跟踪记录整个软件的开发过程
* 减轻开发人员的负担，节省时间，同时降低人为错误

> 常见的版本控制工具

* Git
* SVN
* VSS
* TFS
* Visual Studio Online

> 版本控制分类

**1、本地版本控制**

记录文件每次的更新，可以对每个版本做一个快照，或是记录补丁文件，适合个人用，如RCS   
![](MyNote/image/Git-个人版本控制.png)

**2、集中版本控制**

所有的版本数据都保存在服务器上，协同开发者从服务器上同步更新或者上传自己的修改   
![](MyNote/image/Git-集中版本控制.png)   
所有的版本数据都在服务器上，用户的本地只有自己以前的版本，如果不联网的话，用户就看不到历史的版本，也不能切换版本验证问题，或者在不同分支下工作。而且，所有的数据都保存在单一的服务器上，有很大的分线这个服务器会坏，这样就会丢失所有的数据，当然可以定期备份。代表产品：SVN、CVS、VSS   

**3、分布式版本控制**

所有的版本信息仓库全部同步到本地的每个用户，这样就可以在本地查看所有的版本历史，可以离线在本地提交，只需在联网时push到相应的服务器或者其他用户那里。由于每个用户那里保存的都是所有的版本数据，只要由一个用户的设备没有问题就可以恢复所有的数据，但这增加了本地存储空间的占用。代表作品：Git   
不会因为服务器损坏或者网络问题，造成不能工作的情况   
![](MyNote/image/Git-分布式版本控制.png)

> Git和SVN的主要区别

SVN是集中式版本控制系统

Git是分布式版本控制系统

# Git环境配置

> 软件下载  

[Git官网](https://git-scm.com)   
[淘宝镜像下载](http://npm.taobao.org/mirrors/)   
[清华大学开源镜像网站](https://mirrors.tuna.tsinghua.edu.cn/)

> 先卸载

直接反安装即可、清理环境变量、卸载   
下载对应的版本即可安装   
安装：无脑下一步即可！安装完毕即可使用

> 启动Git

安装成功后在开始菜单中会有Git项，菜单下有3个程序：  
Git Bash:Unix和Linux风格的命令行，使用最多，推荐最多  
Git CMD :Winsows风格的命令行  
Git GUI :图形界面的Git，不建议初学者使用，尽量先熟悉常用的命令

> 基本Linux命令

1. cd: 改变目录
2. cd..: 回退到上一个目录，直接cd进入默认目录
3. pwd: 显示当前所在的目录路径
4. ls(ll): 都是列出当前目录中的所有文件，只不过(ll)会更详细
5. touch: 新建一个文件，如`touch index.js`就会在当前目录下新建一个index.js文件
6. rm: 删除一个文件，如`rm index.js`就会把当前目录下的index.js文件删除 
7. mkdir: 新建一个目录，就是新建一个文件夹
8. rm -r: 删除一个文件夹，`rm -r src`就是删除当前目录下的src文件夹  
   `rm -rf /` 强制删除根目录，不要手贱
9.  mv: 移动文件，`mv index.html src`，index.html是我们要移动的文件，src是目标文件夹，这样写，必须目标文件和目标文件夹在同一目录下
10. reset: 重新初始化终端/清屏。
11. clear: 清屏
12. history: 查看命令历史
13. help: 帮助
14. exit: 退出
15. #: 表示注释

> Git配置

* ` git config -l`              查看Git配置
* ` git config --system --list` 查看系统配置
* `git config --global --list`  查看当前用户配置

**Git相关的配置文件**

1. Git\etc\gitconfig:         Git安装目录下的Gitconfig  --system系统级
2. c:\Users\Administraror\.gitconfig: 只适用于当前登录用户的配置 --global全局

这里可以直接编辑配置文件，通过命令设置后会响应到这里

> 设置用户名与邮箱（用户标识，必要）

`git config --global user.name "用户名"` 设置用户名   
`git config --global user.email "邮箱"`  设置邮箱

# Git基本理论

> 工作区域

Git本地有三个工作区域：工作目录（Working Directory）、暂存区（Stage/Index）、资源库（Repository或Git Directory）。如果在加上远程的Git仓库（Remote Directory）既可以分为四个工作区域。文件在这四个区域之间的转换关系如下所示：   
![](image/Git-四个工作区域.png)

* Workspace:   工作区，平时放代码的地方
* Index/Stage: 暂存区，用于临时存放你的改动，事实上它只是一个文件，保存及将提交的文件列表信息
* Repository:  本地仓库区，就是安全存放数据的地方，这里有提交的所有的版本的数据。其中HEAD指向最新放入仓库的版本
* Remote:      远程仓库，托管代码的服务器，可以简单的认为是项目组中的一台电脑用于远程数据交换

本地的三个区域确切的叔应该是git仓库中HJEAD指向的版本   
![](image/Git-本地的三个区域.png)   
![](image/Git-.git文件夹.png)

> 工作流程

Git的工作流程一般是这样的：  
1. 在工作目录中添加、修改文件；
2. 将需要进行版本管理的文件放入暂存区域；
3. 将暂存区域的文件提交到Git仓库。
   
因此，Git管理的文件有三种状态：已修改（Modigied）、已暂存（staged）、已提交（committed）  


# Git项目搭建

# Git文件操作

# 使用码云/GitHub

# IDEA中集成Git

# 说明：Git分支