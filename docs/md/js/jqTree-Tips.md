[TOC]
{:toc}
# Overview
这里列出我在使用中的一些小技巧，共初学者参考

## 如何给节点添加url
https://stackoverflow.com/questions/20714589/jqtree-associating-a-url-with-a-node
同时参考我的jqTree-QuickStart.md

## 有人说加link需要设置autoEscape：false
https://github.com/mbraak/jqTree/issues/69
TODO：抽空看一下不设置是不是有问题，反正我设置了

## 增加过滤框
这个需要懂一些js和html知识（不需要太多），知道你想什么时候去触发搜索，以及如何获取搜索的值，等。

这个事情在这里有讨论
https://github.com/mbraak/jqTree/issues/211
https://github.com/mbraak/jqTree/issues/230

基本上就是
1. 增加一个搜索框
2. 增加一个js，注册带捕捉事件，然后搜索整个tree

下面搜索框例子
```
    <div id="search">
        <input type="text" id="searchName" name="searchName" required minlength="4" maxlength="8" size="10">
    </div>
```

- 下面是js注册事件和搜索tree例子。主题思想来源于https://github.com/mbraak/jqTree/issues/211
  - 这里要知道，每次键盘时间（抬起按键）都会触发keyup，然后里面判断是不是enter。因为我想enter之后再开始搜索
    - TODO 以后要做成那种google输入那种，随着输入动态搜索
  - 下面的tree.iterate比较好理解，子要indexOf能找到，就算找到了
    - TODO 以后做成可以搜索到多个结果的
  - TODO 目前只搜索tree标题，以后还要集成搜索内容（可能永远不会，除非github能够内置集成这个功能）
```
        //https://github.com/mbraak/jqTree/issues/211
        //https://stackoverflow.com/questions/14411235/while-typing-in-a-text-input-field-printing-the-content-typed-in-a-div
        //https://api.jquery.com/keyup/
        //https://stackoverflow.com/questions/8795283/jquery-get-input-value-after-keypress
        $('#searchName').keyup(
            function(e) {

                //https://stackoverflow.com/questions/11365632/how-to-detect-when-the-user-presses-enter-in-an-input-field
                if (!e) e = window.event;
                var keyCode = e.keyCode || e.which;
                if (keyCode != '13'){
                  return false;
                }

                var $tree = $('#tree1');
                var search_term = this.value;

                var tree = $tree.tree('getTree');

                tree.iterate(
                    function(node) {
                        if (node.name.indexOf(search_term) == -1) {
                            // Not found, continue searching
                            return true;
                        }
                        else {
                            // Found. Select node. Stop searching.
                            $tree.tree('selectNode', node, true);
                            return false
                        }
                    }
                );
            }
        );
```