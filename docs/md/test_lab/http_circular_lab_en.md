# Setup severvices with circular redirection
## target: A->B->C->A 
Maybe you need it sometime later.
Source script see: https://github.com/baoyingwang/JVM_TroubleShooting/tree/master/docs/md/test_lab/_http_circular_lb
<br>note：I maybe adjust the position of the source code. But it will always as near as possible with this note
## 工具
download moco
https://github.com/dreamhead/moco

Thanks Mr Zheng to write this tool!

## 步骤

Setup first http service
A.json as moco configuration. It will redirect the http://localhost:12311/A to http://localhost:12312/B
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
Start script: A.sh：
```
$JAVA_HOME/bin/java -jar moco-runner-0.12.0-standalone.jar http -p 12311 -c A.json
```

Access： http://localhost:12311/A


Setup B.json/B.sh和 C.json/C.sh, below are difference
```
B: 
    "uri":"/B",  
    "redirectTo":"http://localhost:12313/C"
    port:12312
C: 
    "uri":"/C",  
    "redirectTo":"http://localhost:12311/A"
    port:12312
```