#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   wuziqi.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/3/28 15:09   gxrao      1.0         None
'''

# import lib
# 玩家用-1 表示，AI用1 表示 空白地区用0表示
import itertools
import sys
import time
import traceback
from ai import AI1Step
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QWidget


def run_with_exc(f):
    def call(window, *args, **kwargs):
        try:
            return f(window, *args, **kwargs)
        except Exception:
            exc_info = traceback.format_exc()
            QMessageBox.about(window, "信息错误", exc_info)

    return call


class Game_1:
    # 初始化 生成一个地图
    def __init__(self):
        # 15 *15 的二维数组
        self.cur_step = 0
        self.max_search_steps = 2  # 最远搜索
        self.g_map = [[0 for col in range(15)] for row in range(15)]

    @staticmethod
    def Check_5(check_list):
        # 检查是否存在连续５个值
        for k, v in itertools.groupby(check_list):
            if k != 0 and len(list(v)) >= 5:
                return True
        return False

    # 玩家行动
    def player_run(self, input_by_windows=True, pos_x=None, pos_y=None):
        while True:
            try:
                if not input_by_windows:
                    pos_x = int(input("x:"))
                    pos_y = int(input("y:"))
                # 判断是否存在值
                if 0 <= pos_x <= 14 and 0 <= pos_y <= 14:
                    check_ = self.g_map[pos_x][pos_y]
                    if check_ != 0:
                        return
                    self.g_map[pos_x][pos_y] = 1
                    return
            except:
                print("我报错了")

    # AI行动
    def ai_play_1step_py_python(self):
        ai = AI1Step(self, self.cur_step, True)  # AI判断下一步执行什么操作
        st = time.time()
        ai.search(0, [set(), set()], self.max_search_steps)  # 最远看2回合之后
        ed = time.time()
        print('生成了%d个节点，用时%.4f，评价用时%.4f' % (len(ai.method_tree), ed - st, ai.t))
        ai.next_node_dx_list.sort(reverse=True)
        if ai.next_node_dx_list[0] == -1:
            raise ValueError('ai.next_node_dx_list[0] == -1')
        ai_ope = ai.method_tree[ai.next_node_dx_list[0]].ope
        if self.g_map[ai_ope[0]][ai_ope[1]] != 0:
            raise ValueError('self.game_map[ai_ope[0]][ai_ope[1]] = %d' % self.g_map[ai_ope[0]][ai_ope[1]])
        self.g_map[ai_ope[0]][ai_ope[1]] = 2
        self.cur_step += 1

        # 判断胜利条件

    def game_result(self, show=False):
        """判断游戏的结局。0为游戏进行中，1为玩家获胜，2为电脑获胜，3为平局"""
        # 1. 判断是否横向连续五子
        for x in range(11):
            for y in range(15):
                if self.g_map[x][y] == 1 and self.g_map[x + 1][y] == 1 and self.g_map[x + 2][y] == 1 and \
                        self.g_map[x + 3][y] == 1 and self.g_map[x + 4][y] == 1:
                    if show:
                        return 1, [(x0, y) for x0 in range(x, x + 5)]
                    else:
                        return 1
                if self.g_map[x][y] == 2 and self.g_map[x + 1][y] == 2 and self.g_map[x + 2][y] == 2 and \
                        self.g_map[x + 3][y] == 2 and self.g_map[x + 4][y] == 2:
                    if show:
                        return 2, [(x0, y) for x0 in range(x, x + 5)]
                    else:
                        return 2

            # 2. 判断是否纵向连续五子
        for x in range(15):
            for y in range(11):
                if self.g_map[x][y] == 1 and self.g_map[x][y + 1] == 1 and self.g_map[x][y + 2] == 1 and self.g_map[x][
                    y + 3] == 1 and self.g_map[x][y + 4] == 1:
                    if show:
                        return 1, [(x, y0) for y0 in range(y, y + 5)]
                    else:
                        return 1
                if self.g_map[x][y] == 2 and self.g_map[x][y + 1] == 2 and self.g_map[x][y + 2] == 2 and self.g_map[x][
                    y + 3] == 2 and self.g_map[x][y + 4] == 2:
                    if show:
                        return 2, [(x, y0) for y0 in range(y, y + 5)]
                    else:
                        return 2

            # 3. 判断是否有左上-右下的连续五子
        for x in range(11):
            for y in range(11):
                if self.g_map[x][y] == 1 and self.g_map[x + 1][y + 1] == 1 and self.g_map[x + 2][y + 2] == 1 and \
                        self.g_map[x + 3][y + 3] == 1 and self.g_map[x + 4][y + 4] == 1:
                    if show:
                        return 1, [(x + t, y + t) for t in range(5)]
                    else:
                        return 1
                if self.g_map[x][y] == 2 and self.g_map[x + 1][y + 1] == 2 and self.g_map[x + 2][y + 2] == 2 and \
                        self.g_map[x + 3][y + 3] == 2 and self.g_map[x + 4][y + 4] == 2:
                    if show:
                        return 2, [(x + t, y + t) for t in range(5)]
                    else:
                        return 2

            # 4. 判断是否有右上-左下的连续五子
        for x in range(11):
            for y in range(11):
                if self.g_map[x + 4][y] == 1 and self.g_map[x + 3][y + 1] == 1 and self.g_map[x + 2][y + 2] == 1 and \
                        self.g_map[x + 1][y + 3] == 1 and self.g_map[x][y + 4] == 1:
                    if show:
                        return 1, [(x + t, y + 4 - t) for t in range(5)]
                    else:
                        return 1
                if self.g_map[x + 4][y] == 2 and self.g_map[x + 3][y + 1] == 2 and self.g_map[x + 2][y + 2] == 2 and \
                        self.g_map[x + 1][y + 3] == 2 and self.g_map[x][y + 4] == 2:
                    if show:
                        return 2, [(x + t, y + 4 - t) for t in range(5)]
                    else:
                        return 2

            # 5. 判断是否为平局
        for x in range(15):
            for y in range(15):
                if self.g_map[x][y] == 0:  # 棋盘中还有剩余的格子，不能判断为平局
                    if show:
                        return 0, [(-1, -1)]
                    else:
                        return 0

        if show:
            return 3, [(-1, -1)]
        else:
            return 3

    def main(self):
        # while True:
        # # 玩家先走
        # print("玩家走:")
        # prow_x = int(input("x:"))
        # prow_y = int(input("y:"))
        # self.player_run(prow_x, prow_y)
        # check_flg = self.check_win(prow_x, prow_y)
        # if check_flg:
        #     print("player win")
        #     break
        # x, y = self.computer_run()
        # check_flg = self.check_win(x, y)
        # if check_flg:
        #     print("computer win")
        #     break
        # for i in self.checker_board:
        #     print(i, "\n")
        pass


class GameWindows(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()  # 初始化页面
        self.g = Game_1()
        self.last_pos = (-1, -1)

    def init_ui(self):
        """ 初始化界面"""
        # 1. 确定title大小背景页
        self.setObjectName("MiniWindows")
        self.setWindowTitle("Go-bang")
        self.setFixedSize(650, 650)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap(r"C:\Users\86137\Desktop\muz.jpg")))
        self.setPalette(palette)
        # self.setStyleSheet("#MiniWindows{background-color}:red")
        self.setMouseTracking(True)
        # 鼠标移动显示
        self.corner_widget = CornerWidget(self)
        self.corner_widget.repaint()
        self.corner_widget.hide()
        # 显示页面
        self.show()

    @run_with_exc
    def paintEvent(self, e):
        """
        绘制内容
        """

        def draw_map():
            # 绘制棋盘
            qp.setPen(QPen(QColor(0, 0, 0), 2, Qt.SolidLine))

            # 绘制横线
            for x in range(15):
                qp.drawLine(40 * (x + 1), 40, 40 * (x + 1), 600)
            # 绘制竖线
            for y in range(15):
                qp.drawLine(40, 40 * (y + 1), 600, 40 * (y + 1))
            # 绘制
            qp.setBrush(QColor(0, 0, 0))
            key_point = [(4, 4), (12, 4), (4, 12), (12, 12), (8, 8)]
            for t in key_point:
                qp.drawEllipse(QPoint(40 * t[0], 40 * t[1]), 5, 5)

        def draw_pieces():
            # 绘制棋子
            # 黑棋
            qp.setPen(QPen(QColor(0, 0, 0), 1, Qt.SolidLine))
            # qp.setBrush(QColor(0, 0, 0))
            for x in range(15):
                for y in range(15):
                    if self.g.g_map[x][y] == 1:
                        radial = QRadialGradient(40 * (x + 1), 15, 40 * (y + 1), 40 * x + 35, 40 * y + 35)
                        radial.setColorAt(0, QColor(96, 96, 96))
                        radial.setColorAt(1, QColor(0, 0, 0))
                        qp.drawEllipse(40 * (x + 1) - 10, 40 * (y + 1) - 10, 20, 20)

            qp.setPen(QPen(QColor(255, 255, 255), 1, Qt.SolidLine))
            qp.setBrush(QColor(255, 255, 255))
            for x in range(15):
                for y in range(15):
                    if self.g.g_map[x][y] == 2:
                        qp.drawEllipse(40 * (x + 1) - 10, 40 * (y + 1) - 10, 20, 20)

        qp = QPainter()
        qp.begin(self)
        draw_map()
        draw_pieces()
        qp.end()

    @run_with_exc
    def mousePressEvent(self, e):
        """
        鼠标事件
        """
        if e.button() == Qt.LeftButton:
            mouse_x = e.x()
            mouse_y = e.y()
            if (mouse_x % 40 <= 15 or mouse_x % 40 >= 25) and (mouse_y % 40 <= 15 or mouse_y % 40 >= 25):
                game_x = int((mouse_x + 15) // 40) - 1
                game_y = int((mouse_y + 15) // 40) - 1
            else:  # 鼠标点击的位置不正确
                return
            self.g.player_run(True, game_x, game_y)

            check_flag = self.g.game_result()
            if check_flag:
                self.repaint(0, 0, 650, 650)
                self.game_restart(1)
                return
                # 电脑下棋
            self.g.ai_play_1step_py_python()
            check_flg = self.g.game_result()
            if check_flg:
                self.game_restart(2)
                self.repaint(0, 0, 650, 650)
                return
            self.repaint(0, 0, 650, 650)
        for i in self.g.g_map:
            print(i,"\n")

    def mouseMoveEvent(self, e):
        mouse_x = e.x()
        mouse_y = e.y()
        if 25 <= mouse_x <= 615 and 25 <= mouse_y <= 615 and (mouse_x % 40 <= 15 or mouse_x % 40 >= 25) and (
                mouse_y % 40 <= 15 or mouse_y % 40 >= 25):
            game_x = int((mouse_x + 15) // 40) - 1
            game_y = int((mouse_y + 15) // 40) - 1
        else:  # 鼠标当前的位置不对应任何一个游戏格子，将其标记为(01, 01
            game_x = -1
            game_y = -1

        pos_change = False
        if game_x != self.last_pos[0] or game_y != self.last_pos[1]:
            pos_change = True
        self.last_pos = (game_x, game_y)

        if pos_change and game_x != -1:
            self.setCursor(Qt.ArrowCursor)
        if pos_change and game_x != -1:
            self.corner_widget.move(25 + game_x * 40, 25 + game_y * 40)
            self.corner_widget.show()
        if pos_change and game_x == -1:
            self.corner_widget.hide()

    def game_restart(self, res):
        """ 游戏出现"""
        if res == 1:
            QMessageBox.about(self, "游戏结束", "玩家胜利！")
        elif res == 2:
            QMessageBox.about(self, "游戏结束", "电脑胜利！")
        elif res == 3:
            QMessageBox.about(self, "游戏结束", "平局")
        else:
            raise ValueError("游戏非正常结束")
        self.g = Game_1()
        self.repaint(0, 0, 650, 650)


class CornerWidget(QWidget):
    """"""

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setFixedSize(30, 30)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        pen = QPen(Qt.red, 3, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(0, 8, 0, 0)
        qp.drawLine(0, 0, 8, 0)
        qp.drawLine(22, 0, 28, 0)
        qp.drawLine(28, 0, 28, 8)
        qp.drawLine(28, 22, 28, 28)
        qp.drawLine(28, 28, 20, 28)
        qp.drawLine(8, 28, 0, 28)
        qp.drawLine(0, 28, 0, 22)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ex = GameWindows()
    sys.exit(app.exec_())
