<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <img alt="LOGO" src="./assets/伽拉忒亚.jpg" width="256" height="256" />
</p>

<div align="center">

# MaaDuelinks3.6

</div>

本仓库为基于 [MaaFramework](https://github.com/MaaXYZ/MaaFramework)模板开发的Yu-Gi-Oh!Duel Links国服的人机脚本。
欢迎支持maa，也欢迎加入MaaDuelinks（笑）
如果你有新的想法想要实现，可以加入我一起完善脚本！

> **MaaFramework** 是基于图像识别技术、运用 [MAA](https://github.com/MaaAssistantArknights/MaaAssistantArknights) 开发经验去芜存菁、完全重写的新一代自动化黑盒测试框架。
> 低代码的同时仍拥有高扩展性，旨在打造一款丰富、领先、且实用的开源库，助力开发者轻松编写出更好的黑盒测试程序，并推广普及。

## 如何使用
首先从最新的视频简介（[最新视频](https://www.bilibili.com/video/BV124QoYGEfr/?vd_source=432e5ae7fe7562f78ce33e44df702b66)）下载MAADuelinks压缩包，解压后会得到MAADuelinks.exe文件和resource文件夹，将这两个文件放在同一文件夹下，然后打开MuMu模拟器中的《游戏王·决斗链接》，运行MAADuelinks.exe，程序会自动寻找模拟器的adb连接，连接成功后会出现UI如下（可能略有不同）：

![image](https://github.com/user-attachments/assets/04268b0d-89a0-4116-9c46-ed108110f391)



## FAQ

## 一、手动传送门为什么不攻击？
手动传送门需要设置卡组全都是攻击力1800以上的能够通常召唤的，没有效果的怪兽，不要使用卡图较绿的怪，比如双子妖精、小仙人掌等，并且需要设置卡组卡垫为空，否则可能影响攻击识别现在不需要考虑卡垫什么的了！还可以携带装备卡以加快速度PS：现在新版本可以携带一些可以直接发动的魔法卡，比如地碎、地裂等卡片，用来加速手动传送门的速度，
## 二、可以在什么设备上面运行？
可以在windows系统上运行，目前只能在电脑的MuMu模拟器上下载决斗链接运行，暂不支持其他设备请谅解；
## 三、模拟器如何设置？
模拟器设置分辨率如下：

![image](https://github.com/user-attachments/assets/d7facb7c-572e-487f-b34f-1ff003c99e9f)

尽量采用和上述分辨率相同的设置，否则一些图标位置变化可能导致识别出错。
## 四、有类似下面的报错：

![image](https://github.com/user-attachments/assets/756c0a12-00c2-416c-9ada-892e203c85bc)

解决方法：1. 直接重启电脑；2. 在任务管理器里结束abd进程
## 五、自动刷迷宫如何使用？
先在迷宫中设定好自动卡组（如真红眼，恐龙等）为默认卡组，然后返回主页运行自动迷宫选项，便会自动开刷。
要注意：刷迷宫的过程中不能点击屏幕，如果中途停止需要将棋子点回起点处，并且保证棋子在屏幕中央。

## 鸣谢

本项目由 **[MaaFramework](https://github.com/MaaXYZ/MaaFramework)** 强力驱动！

欢迎各位提出宝贵建议！
