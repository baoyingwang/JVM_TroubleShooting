[TOC]
{:toc}

# Overview
jqTree非常简单方便。
看一看其tutorial（https://mbraak.github.io/jqTree/），略微懂一些js和html，就可以快速的搭建一个环境出来。

# 搭建quick start的几个要点
- 把相关的文件(jquery.min.js, tree.jquery.js, jqtree.css)copy到你的子目录下面，方便从html中定位
- 先直接copy下面简单例子，不要改别的东西

# 第一个页面

```

<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>https://baoyingwang.github.io/JVM_TroubleShooting/</title>
    <script src="./scripts/mbraak-jqTree-1.4.12-0-f2091a1/jquery.min.js"></script>
    <script src="./scripts/mbraak-jqTree-1.4.12-0-f2091a1/tree.jquery.js"></script>
    <link rel="stylesheet" href="./scripts/mbraak-jqTree-1.4.12-0-f2091a1/jqtree.css">
    <script>

    var data = [
{"name": "md", "id": 0, "url": "www.google.com", "children": [{"name": "md_1.md", "id": 1, "is_dir": false, "url": "md/md_1.html"}, {"name": "f2", "id": 2, "is_dir": true, "url": "md/f2", "children": [{"name": "index.md", "id": 3, "is_dir": false, "url": "md/f2/index.html"}]}, {"name": "f1", "id": 4, "is_dir": true, "url": "md/f1", "children": [{"name": "index.md", "id": 5, "is_dir": false, "url": "md/f1/index.html"}]}]}



    ];

    $(function() {
        $('#tree1').tree({
            data: data,
            autoOpen: true,
            dragAndDrop: false,
            autoEscape: false
        });

        //https://stackoverflow.com/questions/20714589/jqtree-associating-a-url-with-a-node
        $('#tree1').bind(
            'tree.click',
            function(event) {
                // The clicked node is 'event.node'
                var node = event.node;
                var theURL = node.url;
                if (theURL) {
                    location.href = theURL;
                }
            }
        );
    });

    </script>

    <div id="tree1"></div>


</html>
```
