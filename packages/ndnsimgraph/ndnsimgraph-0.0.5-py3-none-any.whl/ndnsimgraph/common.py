import os
import random
import matplotlib.pyplot as plt


def getRandomColor():
    """获取一个随机的颜色"""
    colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0, 14)]
    return "#" + color


class GraphBase:
    """
    一个基于 matplotlib 实现的通用绘图接口
    """

    def __init__(self):
        # 记录所有可用的 Marker
        # https://matplotlib.org/stable/api/markers_api.html
        self.markers = ["o", "v", "^", "<", ">", "1", "2", "3", "4", "8", "s", "p", "P", "*", "h", "H", "+",
                        "x", "X", "D", "d", "|", "_", ".", ","]
        # 记录当前图已经使用的Marker
        self.currentUsedMarker = {}
        # 记录常用的 color
        self.colors = [
            "tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple",
            "tab:brown", "tab:pink", "tab:gray", "tab:olive", "tab:cyan", "red", "green", "blue", "c", "m", "y",
        ]
        # 记录当前图已经使用的 color
        self.currentUsedColor = {}

    def autoSelectMarker(self) -> str:
        """
        从所有的marker中自动选择 Marker，保证不和已有的Marker重复
        :return:
        """
        for marker in self.markers:
            if marker not in self.currentUsedMarker:
                return marker
        return ""

    def autoSelectColor(self) -> str:
        for color in self.colors:
            if color not in self.currentUsedColor:
                return color
        while True:
            randomColor = getRandomColor()
            if randomColor not in self.currentUsedColor:
                break
        return randomColor

    def xlim(self, *args, **kwargs):
        plt.xlim(*args, **kwargs)
        return self

    def ylim(self, *args, **kwargs):
        plt.ylim(*args, **kwargs)
        return self

    def xticks(self, ticks=None, labels=None, **kwargs):
        plt.xticks(ticks, labels, **kwargs)
        return self

    def title(self, label, fontdict=None, loc=None, pad=None, **kwargs):
        plt.title(label, fontdict=fontdict, loc=loc, pad=pad, **kwargs)
        return self

    def xlabel(self, xlabel, fontdict=None, labelpad=None, loc=None, **kwargs):
        plt.xlabel(xlabel, fontdict, labelpad, loc=loc, **kwargs)
        return self

    def ylabel(self, ylabel, fontdict=None, labelpad=None, loc=None, **kwargs):
        plt.ylabel(ylabel, fontdict, labelpad, loc=loc, **kwargs)
        return self

    def legend(self, *args, **kwargs):
        plt.legend(*args, **kwargs)
        return self

    def plot(self, x, y, *args,
             color: str = "&&",
             linewidth: float = 2, linestyle: str = "dotted", marker: str = "&&",
             markerfacecolor: str = "none", markersize: float = 6,
             **kwargs):
        if "linewidth" not in kwargs:
            kwargs["linewidth"] = linewidth
        if "linestyle" not in kwargs:
            kwargs["linestyle"] = linestyle
        # 默认自动选择Marker
        if marker == "&&":
            marker = self.autoSelectMarker()
            self.currentUsedMarker[marker] = marker
        if "marker" not in kwargs:
            kwargs["marker"] = marker
        if "markerfacecolor" not in kwargs:
            kwargs["markerfacecolor"] = markerfacecolor
        if "markersize" not in kwargs:
            kwargs["markersize"] = markersize
        # 默认自动选择 color
        if color == "&&":
            color = self.autoSelectColor()
            self.currentUsedColor[color] = color
        if "color" not in kwargs:
            kwargs["color"] = color
        plt.plot(x, y, *args, **kwargs)
        return self

    def show(self):
        """
        绘制吞吐量图，并show
        :return:
        """
        plt.show()
        return self

    def drawAndSave(self, dir: str, name: str):
        """
        绘制吞吐量图，并保存到图片当中
        :return:
        """
        if not os.path.exists(dir):
            os.makedirs(dir)
        plt.savefig(f"{dir}{os.sep}{name}")
        return self

    def close(self):
        plt.close()
