{% include toc.html html=content %}

# Java Trouble Shooting 实用介绍

开始之前，检查一下JVM参数，其将极大有利于问题调查与恢复
* 总是设置OOM时候进行heapdump (https://github.com/baoyingwang/JVM_TroubleShooting/wiki/JVM-Options-Suggestions)
* 总是打印GC activity(https://github.com/baoyingwang/JVM_TroubleShooting/wiki/JVM-Options-Suggestions)

熟练掌握visualvm + MAT + jstack，其他的碰到具体问题再具体的研究，可以解决大部分问题。

TODO 1
* 下面的各个方法使用起来不那么方便，重新整编本文，时期更加易读/易于定位
* 提供一个方便的脚本，把下面功能罗列进去，方便实际使用
* 增加TOC/Table Of Content

# 获取一个Java进程的内部信息

## 获取线程信息（thread dump - 每个线程当时的运行状态）
- 推荐：kill -3 <pid> 不依赖于任何工具，直接打印到console；限制，only for linux/unix 
- 推荐：jstack <pid> 简单直接。但是依赖于jdk。
  - refer： https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/tooldescr016.html
  - 参考：[CPU 01_Java进程高CPU使用调查方法简介](https://github.com/baoyingwang/JVM_TroubleShooting/wiki/CPU---01_Java%E8%BF%9B%E7%A8%8B%E9%AB%98CPU%E4%BD%BF%E7%94%A8%E8%B0%83%E6%9F%A5%E6%96%B9%E6%B3%95%E7%AE%80%E4%BB%8B)
- 生成core dump文件，然后jstack $JAVA_HOME/bin/java core。
- 开发时还可以使用jvisualvm，顺便就看了，也比较简单。
- 还有其他方式，如jmc, control+break on Windows, ThreadMXBean, APMTool - App Dynamics。本文 [7 个抓取 Java Thread Dumps 的方式](https://my.oschina.net/dabird/blog/691692) 介绍了7中方式（jstack, kill -3, jvisualvm, jmc, control+break on Windows, ThreadMXBean, APMTool - App Dynamics)

- note: 3 - SIGQUIT, jvm不会退出。参见https://hllvm-group.iteye.com/group/topic/39570介绍的jvm内部如何实现（在dk7u/jdk7u/hotspot/file/tip/src/share/vm/runtime/os.cpp中定义了对这个信号的处理）

## 查看GC和内存
- jmap -heap pid 查看overview 
- jstat -gc pid 查看gc
  - 一般不需要，因为我们一般都打开了打印GC的jvm option 

## 获取heap dump
- 使用jmap -dump:format=b,file=YOUR_EXPECTED_HEAP_DUMP_FILE_NAME pid  直接dump出来。限制：依赖于jdk 工具 jmap。
  - 注意：如果机器没有安装jdk(也就没有jmap工具），则可以使用gcore把整个进程dump出来（gcore是通用工具，不是jvm工具; gcore -o filename <pid>），然后可以通过jmap工具读取gcore的输出文件.
- 使用jvisualvm界面直接dump。限制：一般无法直接访问生产环境
- 使用gcore生成一个进程完整的coredump文件，使用jmap命令从这个文件（和相应的java binary）形成heap dump (jmap -dump:format=b,file=YOUR_EXPECTED_HEAP_DUMP_FILE_NAME JAVA_BINARY CORE_DUMP_FILE ).  限制：这个文件比较大（可能几个G甚至几十个G，不过可以压缩一些）。（好像）jvisualvm可以直接load这个core dump文件。jstack可以直接直接引用于这个core dump文件。参考：https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/bugreports004.html 关于如何生成core dump。

## 生成进程core dump
直接使用gcore [-o filename] pid  获取该coredump之后，可以线下使用jmap，jstack工具获取线程信息/heap信息等，继续分析。

## 通过visualvm检测java进程
该工具visualvm + MAT + jstack是我最常用三个之一。 它的功能及其强大。我一般用visualvm
* 查看内存使用情况（开发测试环境）。安装了vsiual gc插件，各内存区域情况一目了然。
* 查看cpu使用情况。通过Sampler-CPU, 实时查看各个线程，各个方法在sampling期间都是用了多少cpu。简直是performance调优的利器。
* 查看memory使用情况。通过Sampler-Memory, 实时查看各个线程，各个方法在sampling期间都是分配了多少内存。


JVM启动时，如果加了这样的参数，就可以不停机使用visualvm直接连接查看内存，cpu，线程等
-Dcom.sun.management.jmxremote.port=3333  -Dcom.sun.management.jmxremote.ssl=false  -Dcom.sun.management.jmxremote.authenticate=false

如果你有多个网卡，还需要指定监听的IP -Djava.rmi.server.hostname=YOUR_IP YOUR_APP

## 通过jdb直接对java进程进行debug
做这件事情有几个条件
1. 该进程打开了debug， e.g.-Xdebug -Xrunjdwp:transport=dt_socket,address=8998,server=y 
2. 安装了jdk，jdb是jdk内置binary
3. 你了解源代码（精确到代码方法，甚至代码行）以及当前问题可能处在哪里


## 一个进程的各种信息
- 某进程所有相关描述符(fd) lsof -a -p pid 或者直接进入 /proc/<pid>/fd 查看（每个fd以一个文件的方式体现）.note: 从lsof的结果中grep LISTEN可以知道这个进程在哪些端口监听。BTW：lsof -i :port 可以知道这个port被哪个进程监听（或者使用netstat -ltnp | grep -w ':80' )
- 获取进程启动目录： pwdx pid , lsof -p pid | grep cwd, readlink -e /proc/<PID>/cwd refer: https://unix.stackexchange.com/questions/94357/find-out-current-working-directory-of-a-running-process
- 获取进程的父（直至1）和子进程 pstree -s -p pid
- 获取进程使用的cpu/memo使用情况 ps -eo pid,lwp,user,comm,pcpu,rss,size,%mem | grep "^[[:space:]]\+${process_id}[[:space:]]\+" ， 或者 ps -mfL pid 支持简单列出线程列表
- 获取进程的各个轻进程/线程的cpu/memory等使用情况 ps -Leo pid,lwp,user,comm,pcpu --no-headers| grep "^[[:space:]]\+${process_id}[[:space:]]\+" 这个可以用来找到最繁忙的线程（根绝lwp id与jstack输出中的thread id做比较 - refer： KB [Lib - script - identify the busy thread of a java process] )
- 进程的io usage ， 工具 iotop - 需要单独安装and need kernel >2.6.20 and Python 2.5 see https://www.cyberciti.biz/hardware/linux-iotop-simple-top-like-io-monitor/； 或者atop（也需要单独安装）
- pmap 这个命令可以查看进程(任何linux进程，不只jvm）的内存地址分配。有一些深入的内存问题，可能需要查看这个。
  - 参考： [Java内存之本地内存分析神器： NMT 和 pmap](http://blog.csdn.net/jicahoo/article/details/50933469) 
  - 我在调查XXX GW的最大容量的时候，是用了pmap来定位各个线程使用native memory的情况，是很有帮助的。进而了解到，线程数量与heap大小之间的反向关系(TODO 一篇文档待整理). 



# 获取操作系统自身的各种信息
- 运行状态， 直接使用top或者htop，查看load， 进程的cpu排名/memory排名等
- io情况，使用iostat（refer： http://www.cnblogs.com/peida/archive/2012/12/28/2837345.html ） 或者vmstat 


# 工具一览 - 线下排查

## MAT - 强大的heap解析工具，直接给出线程溢出报告。而且可以方便的查看heap中各个变量的值！同时支持查看线程信息。绝对是居家必备。
TODO 这个是一个单独的页面，挪走，这里只保留一个简单的介绍

掌握以下知识，对于日常问题调查很有帮助
1. 通过查看leak report, 定位可能的问题点。这个比较直接，因其自动生成report。
2. 对于怀疑的内存部分，通过incoming/outgoing reference, 来查看具体的内存对象的值，以及数量。理解
3. 其支持查看java list(包括map）的所有元素的值(java collections -> extract list values). 因为很多内存问题都与list/map中元素过多有关。
4. 掌握简单的OQL语言, 例如
```
e.g.
SELECT toString(s.ab.value) 
FROM com.xyz.DealRecord s 
WHERE (toString(s.ab.value).length() >= 1000)  
note: ab is a String field of DealRecord
note: it will query all ab fields whose length > 1000
```
5. 知道如何查看线程列表。一般很少注意到这个地方，因为我们一般直接通过leak report往下看内存情况。但是有些复杂问题，需要结合线程信息才行。通过table of contents -> system overview -> thread overview可以看到线程列表，每个线程retain的内存大小等。

## Java 8 NMT 查看jvm native memory的利器。不过，我暂时还没有在实际问题中使用过NTM这个工具。只是作为学习使用。
参考：[Java内存之本地内存分析神器： NMT 和 pmap](http://blog.csdn.net/jicahoo/article/details/50933469) 

