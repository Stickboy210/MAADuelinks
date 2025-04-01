<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <img alt="LOGO" src="https://cdn.jsdelivr.net/gh/MaaAssistantArknights/design@main/logo/maa-logo_512x512.png" width="256" height="256" />
</p>

<div align="center">

# MaaDuelinks3.6

</div>

本仓库为 [MaaFramework](https://github.com/MaaXYZ/MaaFramework) 所提供的项目模板，基于该模板开发的Yu-Gi-Oh!Duel Links国服的人机脚本。
欢迎支持maa，也欢迎加入MaaDuelinks（笑）
如果你有新的想法想要实现，可以加入我一起完善脚本！

> **MaaFramework** 是基于图像识别技术、运用 [MAA](https://github.com/MaaAssistantArknights/MaaAssistantArknights) 开发经验去芜存菁、完全重写的新一代自动化黑盒测试框架。
> 低代码的同时仍拥有高扩展性，旨在打造一款丰富、领先、且实用的开源库，助力开发者轻松编写出更好的黑盒测试程序，并推广普及。

## 如何使用
首先从最新的视频简介（[最新视频](https://www.bilibili.com/video/BV124QoYGEfr/?vd_source=432e5ae7fe7562f78ce33e44df702b66)）下载MAADuelinks压缩包，解压后会得到MAADuelinks.exe文件和resource文件夹，将这两个文件放在同一文件夹下，然后打开MuMu模拟器中的《游戏王·决斗链接》，运行MAADuelinks.exe，程序会自动寻找模拟器的adb连接，连接成功后会出现UI如下（可能略有不同）：
<div align="center">
  ![image](https://github.com/user-attachments/assets/04268b0d-89a0-4116-9c46-ed108110f391)
</div>
![image](https://github.com/user-attachments/assets/04268b0d-89a0-4116-9c46-ed108110f391)



## FAQ

### 1. 我是第一次使用 Python，在命令行输入 `python ./configure.py` 或 `python -m pip install MaaFW` 之后没有反应？没有报错，也没有提示成功，什么都没有

Win10 或者 Win11 系统自带了一份 "Python"，但它其实只是一个安装器，是没法用的。  
你需要做的是关闭它或者删除它的环境变量，然后自己去 Python 官网下载并安装一份 Python。  
[参考方法](https://www.bilibili.com/read/cv24692025/)

### 2. 我输入 `python ./configure.py` 后报错：`Please clone this repository completely, don’t miss "--recursive", and don’t download the zip package!`

![项目不完整1](https://github.com/user-attachments/assets/e1f697c0-e5b6-4853-8664-a358df7327a8)

**请仔细阅读文档！！！**  
就是你现在正在看的本篇文档，就在上面，“如何开发”里的第一条，都已经用粗体标出来了，再问我要骂人了！

### 3. 使用 MaaDebugger 或 MaaPicli 时弹窗报错，应用程序错误：应用程序无法正常启动

![缺少运行库](https://github.com/user-attachments/assets/942df84b-f47d-4bb5-98b5-ab5d44bc7c2a)

一般是电脑缺少某些运行库，请安装一下 [vc_redist](https://aka.ms/vs/17/release/vc_redist.x64.exe) 。

### 4. 我在这个仓库里提了 Issue 很久没人回复

这里是《项目模板》仓库，它仅仅是一个模板，一般很少会修改，开发者也较少关注。  
在此仓库请仅提问模板相关问题，其他问题最好前往对应的仓库提出，如果有 log，最好也带上它（`debug/maa.log` 文件）

- MaaFW 本身及 MaaPiCli 的问题：[MaaFramework/issues](https://github.com/MaaXYZ/MaaFramework/issues)
- MaaDebugger 的问题：[MaaDebugger/issues](https://github.com/MaaXYZ/MaaDebugger/issues)
- 不知道算是哪里的、其他疑问等：[讨论区](https://github.com/orgs/MaaXYZ/discussions)

### 5. OCR 文字识别一直没有识别结果，报错 "Failed to load det or rec", "ocrer_ is null"

你不但没有仔细阅读文档，还无视了前面步骤的报错。我不想解释了，请再把本文档仔细阅读一遍！

## 鸣谢

本项目由 **[MaaFramework](https://github.com/MaaXYZ/MaaFramework)** 强力驱动！

感谢以下开发者对本项目作出的贡献（下面链接改成你自己的项目地址）:

<a href="https://github.com/MaaXYZ/MaaFramework/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=MaaXYZ/MaaFramework&max=1000" />
</a>
