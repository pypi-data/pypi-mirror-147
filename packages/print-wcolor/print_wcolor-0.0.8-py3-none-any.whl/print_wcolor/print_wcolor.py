# print("\033[1;41m 字体颜色：浅灰色\033[0m")
# print("\033[1;30m 字体颜色：白色\033[0m")
# print("\033[1;31m 字体颜色：红色\033[0m")
# print("\033[1;32m 字体颜色：绿色\033[0m")
# print("\033[1;33m 字体颜色：黄色\033[0m")
# print("\033[1;34m 字体颜色：蓝色\033[0m")
# print("\033[1;35m 字体颜色：淡紫色\033[0m")
# print("\033[1;36m 字体颜色：青色\033[0m")
# print("\033[1;37m 字体颜色：灰色\033[0m")
# print("\033[1;38m 字体颜色：浅灰色\033[0m")
# print("背景颜色：白色   \033[1;40m    \033[0m")
# print("背景颜色：红色   \033[1;41m    \033[0m")
# print("背景颜色：深黄色 \033[1;42m    \033[0m")
# print("背景颜色：浅黄色 \033[1;43m    \033[0m")
# print("背景颜色：蓝色   \033[1;44m    \033[0m")
# print("背景颜色：淡紫色 \033[1;45m    \033[0m")
# print("背景颜色：青色   \033[1;46m    \033[0m")
# print("背景颜色：灰色   \033[1;47m    \033[0m")

#print_with color
def print_wcolor(*args,fg=None,bg=None):
    fg_dict={"black":30,"red":31,"green":32,"yellow":33,"blue":34,"purple":35,"cyan":36,"white":37}
    bg_dict = {"black": 40, "red": 41, "green": 42, "yellow": 43, "blue": 44, "purple": 45, "cyan": 46, "white": 47}
    if fg is not None and bg is not None:
        assert fg in fg_dict.keys(), "the foreground color error in the function of print_color"
        assert bg in bg_dict.keys(), "the background color error in the function of print_color"
        for i in args:
            print("\033[0;{};{}m {} \033[0m".format(fg_dict[fg], bg_dict[bg], i))
    elif fg is not None:
        assert fg in fg_dict.keys(), "the foreground color error in the function of print_color"
        for i in args:
            print("\033[0;{}m {} \033[0m".format(fg_dict[fg], i))
    elif bg is not None:
        assert bg in bg_dict.keys(), "the background color error in the function of print_color"
        for i in args:
            print("\033[0;{};{}m {} \033[0m".format(fg_dict["white"],bg_dict[bg], i))
    else:
        for i in args:
            print(i)
if __name__=="__main__":
    print_wcolor("it is all good","i think,therefore i am",fg="green",bg="red")
