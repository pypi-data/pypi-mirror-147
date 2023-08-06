# print_wcolor
使用print_wcolor可以打印出彩色字体和彩色背景

Use Print WColor to print out colored fonts and colored backgrounds
使用示例

for example

```
from print_wcolor import print_wcolor

a=[1,2,3,4]
c={}
c["r"]=255
c["g"]=255
print("*"*20)
print_wcolor("i think","therefor i am",a,c,fg="red",bg="green")
print("*"*20)
print_wcolor("i think","therefor i am",a,c,fg="red")
print("*"*20)
print_wcolor("i think","therefor i am",a,c,bg="green")
print("*"*20)
print_wcolor("i think","therefor i am",a,c)
```


其中"i think,therefor i am"是要打印的信息，fg是字体颜色，bg是背景颜色。

Where "I think,therefor I am" is the information to be printed, fg is the font color, bg is the background color.

关键词fg选项如下

Keyword FG options are as follows

```
{"black","red","green","yellow","blue","purple","cyan","white"}
```


关键词bg选项如下

Keyword BG options are as follows

```
{"black","red","green","yellow","blue","purple","cyan","white"}
```

