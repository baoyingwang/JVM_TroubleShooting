# 如何搭建一个http circular
## 目标，搭建一个A->B->C->A 循环http re-direction的web访问
别问我为什么需要这个，碰到你就需要了
## 工具
下载moco
https://github.com/dreamhead/moco
## 步骤

准备web节点A的配置文件A.json。其将redirect访问到http://localhost:12312/B
```
[
        {
                "description":"redirect example",
                "request":{
                        "uri":"/A"
                },
                "response":{
                        "json":{
                                "note":"this will be redirected"
                        }
                },
                "redirectTo":"http://localhost:12312/B"
        }
]
```
启动A.sh：
```
$JAVA_HOME/bin/java -jar moco-runner-0.12.0-standalone.jar http -p 12311 -c A.json
```
访问方式： http://localhost:12311/A


通过类似方式准备节点B.json/B.sh和节点C.json/C.sh, 不同点在于
```
B: 
    "uri":"/B",  
    "redirectTo":"http://localhost:12313/C"
    启动端口改为12312
C: 
    "uri":"/C",  
    "redirectTo":"http://localhost:12311/A"
    启动端口改为12312
```