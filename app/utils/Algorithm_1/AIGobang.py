'''
Function:
	五子棋小游戏-支持人机和局域网对战
Author:
	Bin

'''
import os
import sys
import json
import pygame
import random
import socket
import threading
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from itertools import product


class cfg:
    ICON_FILEPATH = "D:/Blog/app/utils/Algorithm_1/resources/images/icon/icon.ico"
    # 背景图片路径
    BACKGROUND_IMAGEPATHS = {
        'bg_game': f'D:/Blog/app/utils/Algorithm_1/resources/images/bg/bg_game.png',
        'bg_start': f'D:/Blog/app/utils/resources/images/bg/bg_start.png'
    }
    # 按钮图片路径
    BUTTON_IMAGEPATHS = {
        'online': [f'D:/Blog/app/utils/Algorithm_1/resources/images/buttons/online_0.png',
                   f'D:/Blog/app/utils/Algorithm_1/resources/images/buttons/online_1.png',
                   f'D:/Blog/app/utils/Algorithm_1/resources/images/buttons/online_2.png'],
        'ai': [f'D:/Blog/app/utils/Algorithm_1/resources/images/buttons/ai_0.png',
               f'D:/Blog/app/utils/Algorithm_1/resources/images/buttons/ai_1.png',
               f'D:/Blog/app/utils/Algorithm_1/resources/images/buttons/ai_2.png'],
        'home': [f'D:/Blog/app/utils/Algorithm_1/resources/images/buttons/home_0.png',
                 f'D:/Blog/app/utils/Algorithm_1/resources/images/buttons/home_1.png',
                 f'D:/Blog/app/utils/Algorithm_1/resources/images/buttons/home_2.png'],
        'givein': [f'D:/Blog/app/utils/Algorithm_1/resources/images/buttons/givein_0.png',
                   f'D:/Blog/app/utils/Algorithm_1/resources/images/buttons/givein_1.png',
                   f'D:/Blog/app/utils/Algorithm_1/resources/images/buttons/givein_2.png'],
        'regret': [f'D:/Blog/app/utils/Algorithm_1/resources/images/buttons/regret_0.png',
                   f'D:/Blog/app/utils/Algorithm_1/resources/images/buttons/regret_1.png',
                   f'D:/Blog/app/utils/Algorithm_1/resources/images/buttons/regret_2.png'],
        'startgame': [f'D:/Blog/app/utils/Algorithm_1/resources/images/buttons/startgame_0.png',
                      f'D:/Blog/app/utils/Algorithm_1/resources/images/buttons/startgame_1.png',
                      f'D:/Blog/app/utils/Algorithm_1/resources/images/buttons/startgame_2.png'],
        'urge': [f'D:/Blog/app/utils/Algorithm_1/resources/images/buttons/urge_0.png',
                 f'D:/Blog/app/utils/Algorithm_1/resources/images/buttons/urge_1.png',
                 f'D:/Blog/app/utils/Algorithm_1/resources/images/buttons/urge_2.png']
    }
    # 显示胜利图片路径
    WIN_IMAGEPATHS = {
        'black': f'D:/Blog/app/utils/resources/images/win/black_win.png',
        'white': f'D:/Blog/app/utils/resources/images/win/white_win.png',
        'draw': f'D:/Blog/app/utils/resources/images/win/draw.png'
    }
    # 棋子图片路径
    CHESSMAN_IMAGEPATHS = {
        'black': f'D:/Blog/app/utils/resources/images/chessman/black.png',
        'white': f'D:/Blog/app/utils/resources/images/chessman/white.png',
        'sign': f'D:/Blog/app/utils/resources/images/chessman/sign.png',
    }
    # 音效
    # SOUNDS_PATHS = {
    #     'drop': f'D:/Blog/app/utils/resources/audios/drop.wav',
    #     'urge': f'D:/Blog/app/utils/resources/audios/urge.wav'
    # }
    # 端口号(联机对战时使用)
    PORT = 3333


'''游戏开始界面'''


class gameStartUI(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(gameStartUI, self).__init__(parent)
        self.setFixedSize(760, 650)
        self.setWindowTitle('五子棋')
        self.setWindowIcon(QIcon(cfg.ICON_FILEPATH))
        # 背景图片
        palette = QPalette()
        palette.setBrush(self.backgroundRole(),
                         QBrush(QPixmap(f'D:/Blog/app/utils/Algorithm_1/resources/images/bg/bg_start.png')))
        self.setPalette(palette)
        # 按钮
        # --人机对战
        self.ai_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('ai'), self)
        self.ai_button.move(250, 200)
        self.ai_button.show()
        self.ai_button.click_signal.connect(self.playWithAI)
        # --联机对战
        self.online_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('online'), self)
        self.online_button.move(250, 350)
        self.online_button.show()
        self.online_button.click_signal.connect(self.playOnline)

    '''人机对战'''

    def playWithAI(self):
        self.close()
        self.gaming_ui = playWithAIUI(cfg)
        self.gaming_ui.exit_signal.connect(lambda: sys.exit())
        self.gaming_ui.back_signal.connect(self.show)
        self.gaming_ui.show()

    '''联机对战'''

    def playOnline(self):
        self.close()
        self.gaming_ui = playOnlineUI(cfg, self)
        self.gaming_ui.show()


class aiGobang():
    def __init__(self, ai_color, player_color, search_depth=1, **kwargs):
        assert search_depth % 2, 'search_depth must be odd number'
        self.ai_color = ai_color
        self.player_color = player_color
        self.search_depth = search_depth
        self.score_model = [(50, (0, 1, 1, 0, 0)),
                            (50, (0, 0, 1, 1, 0)),
                            (200, (1, 1, 0, 1, 0)),
                            (500, (0, 0, 1, 1, 1)),
                            (500, (1, 1, 1, 0, 0)),
                            (5000, (0, 1, 1, 1, 0)),
                            (5000, (0, 1, 0, 1, 1, 0)),
                            (5000, (0, 1, 1, 0, 1, 0)),
                            (5000, (1, 1, 1, 0, 1)),
                            (5000, (1, 1, 0, 1, 1)),
                            (5000, (1, 0, 1, 1, 1)),
                            (5000, (1, 1, 1, 1, 0)),
                            (5000, (0, 1, 1, 1, 1)),
                            (50000, (0, 1, 1, 1, 1, 0)),
                            (99999999, (1, 1, 1, 1, 1))]
        self.alpha = -99999999
        self.beta = 99999999
        self.all_list = [(i, j) for i, j in product(range(19), range(19))]

    '''外部调用'''

    def act(self, history_record):
        self.ai_list = []
        self.player_list = []
        self.aiplayer_list = []
        for item in history_record:
            self.aiplayer_list.append((item[0], item[1]))
            if item[-1] == self.ai_color:
                self.ai_list.append((item[0], item[1]))
            elif item[-1] == self.player_color:
                self.player_list.append((item[0], item[1]))
        while True:
            self.next_point = random.choice(range(19)), random.choice(range(19))
            if self.next_point not in self.aiplayer_list:
                break
        self.__doSearch(True, self.search_depth, self.alpha, self.beta)
        return self.next_point

    '''负极大值搜索, alpha+beta剪枝'''

    def __doSearch(self, is_ai_round, depth, alpha, beta):
        if self.__isgameover(self.ai_list) or self.__isgameover(self.player_list) or depth == 0:
            return self.__evaluation(is_ai_round)
        blank_list = list(set(self.all_list).difference(set(self.aiplayer_list)))
        blank_list = self.__rearrange(blank_list)
        for next_step in blank_list:
            if not self.__hasNeighbor(next_step):
                continue
            if is_ai_round:
                self.ai_list.append(next_step)
            else:
                self.player_list.append(next_step)
            self.aiplayer_list.append(next_step)
            value = -self.__doSearch(not is_ai_round, depth - 1, -beta, -alpha)
            if is_ai_round:
                self.ai_list.remove(next_step)
            else:
                self.player_list.remove(next_step)
            self.aiplayer_list.remove(next_step)
            if value > alpha:
                if depth == self.search_depth:
                    self.next_point = next_step
                if value >= beta:
                    return beta
                alpha = value
        return alpha

    '''游戏是否结束了'''

    def __isgameover(self, oneslist):
        for i, j in product(range(19), range(19)):
            if i < 15 and (i, j) in oneslist and (i + 1, j) in oneslist and (i + 2, j) in oneslist and (
                    i + 3, j) in oneslist and (i + 4, j) in oneslist:
                return True
            elif j < 15 and (i, j) in oneslist and (i, j + 1) in oneslist and (i, j + 2) in oneslist and (
                    i, j + 3) in oneslist and (i, j + 4) in oneslist:
                return True
            elif i < 15 and j < 15 and (i, j) in oneslist and (i + 1, j + 1) in oneslist and (
                    i + 2, j + 2) in oneslist and (i + 3, j + 3) in oneslist and (i + 4, j + 4) in oneslist:
                return True
            elif i > 3 and j < 15 and (i, j) in oneslist and (i - 1, j + 1) in oneslist and (
                    i - 2, j + 2) in oneslist and (i - 3, j + 3) in oneslist and (i - 4, j + 4) in oneslist:
                return True
        return False

    '''重新排列未落子位置'''

    def __rearrange(self, blank_list):
        last_step = self.aiplayer_list[-1]
        for item in blank_list:
            for i, j in product(range(-1, 2), range(-1, 2)):
                if i == 0 and j == 0:
                    continue
                next_step = (last_step[0] + i, last_step[1] + j)
                if next_step in blank_list:
                    blank_list.remove(next_step)
                    blank_list.insert(0, next_step)
        return blank_list

    '''是否存在近邻'''

    def __hasNeighbor(self, next_step):
        for i, j in product(range(-1, 2), range(-1, 2)):
            if i == 0 and j == 0:
                continue
            if (next_step[0] + i, next_step[1] + j) in self.aiplayer_list:
                return True
        return False

    '''计算得分'''

    def __calcScore(self, i, j, x_direction, y_direction, list1, list2, all_scores):
        add_score = 0
        max_score = (0, None)
        for each in all_scores:
            for item in each[1]:
                if i == item[0] and j == item[1] and x_direction == each[2][0] and y_direction == each[2][1]:
                    return 0, all_scores
        for noffset in range(-5, 1):
            position = []
            for poffset in range(6):
                x, y = i + (poffset + noffset) * x_direction, j + (poffset + noffset) * y_direction
                if (x, y) in list2:
                    position.append(2)
                elif (x, y) in list1:
                    position.append(1)
                else:
                    position.append(0)
            shape_len5 = tuple(position[0: -1])
            shape_len6 = tuple(position)
            for score, shape in self.score_model:
                if shape_len5 == shape or shape_len6 == shape:
                    if score > max_score[0]:
                        max_score = (score, ((i + (0 + noffset) * x_direction, j + (0 + noffset) * y_direction),
                                             (i + (1 + noffset) * x_direction, j + (1 + noffset) * y_direction),
                                             (i + (2 + noffset) * x_direction, j + (2 + noffset) * y_direction),
                                             (i + (3 + noffset) * x_direction, j + (3 + noffset) * y_direction),
                                             (i + (4 + noffset) * x_direction, j + (4 + noffset) * y_direction)),
                                     (x_direction, y_direction))
        if max_score[1] is not None:
            for each in all_scores:
                for p1 in each[1]:
                    for p2 in max_score[1]:
                        if p1 == p2 and max_score[0] > 10 and each[0] > 10:
                            add_score += max_score[0] + each[0]
            all_scores.append(max_score)
        return add_score + max_score[0], all_scores

    '''评估函数'''

    def __evaluation(self, is_ai_round):
        if is_ai_round:
            list1 = self.ai_list
            list2 = self.player_list
        else:
            list2 = self.ai_list
            list1 = self.player_list
        active_all_scores = []
        active_score = 0
        for item in list1:
            score, active_all_scores = self.__calcScore(item[0], item[1], 0, 1, list1, list2, active_all_scores)
            active_score += score
            score, active_all_scores = self.__calcScore(item[0], item[1], 1, 0, list1, list2, active_all_scores)
            active_score += score
            score, active_all_scores = self.__calcScore(item[0], item[1], 1, 1, list1, list2, active_all_scores)
            active_score += score
            score, active_all_scores = self.__calcScore(item[0], item[1], -1, 1, list1, list2, active_all_scores)
            active_score += score
        passive_all_scores = []
        passive_score = 0
        for item in list2:
            score, passive_all_scores = self.__calcScore(item[0], item[1], 0, 1, list2, list1, passive_all_scores)
            passive_score += score
            score, passive_all_scores = self.__calcScore(item[0], item[1], 1, 0, list2, list1, passive_all_scores)
            passive_score += score
            score, passive_all_scores = self.__calcScore(item[0], item[1], 1, 1, list2, list1, passive_all_scores)
            passive_score += score
            score, passive_all_scores = self.__calcScore(item[0], item[1], -1, 1, list2, list1, passive_all_scores)
            passive_score += score
        total_score = active_score - passive_score * 0.1
        return total_score


class playWithAIUI(QWidget):
    back_signal = pyqtSignal()
    exit_signal = pyqtSignal()
    send_back_signal = False

    def __init__(self, cfg, parent=None, **kwargs):
        super(playWithAIUI, self).__init__(parent)
        self.cfg = cfg
        self.setFixedSize(760, 650)
        self.setWindowTitle('五子棋')
        self.setWindowIcon(QIcon(cfg.ICON_FILEPATH))
        # 背景图片
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap(cfg.BACKGROUND_IMAGEPATHS.get('bg_game'))))
        self.setPalette(palette)
        # 按钮
        self.home_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('home'), self)
        self.home_button.click_signal.connect(self.goHome)
        self.home_button.move(680, 10)
        self.startgame_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('startgame'), self)
        self.startgame_button.click_signal.connect(self.startgame)
        self.startgame_button.move(640, 240)
        self.regret_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('regret'), self)
        self.regret_button.click_signal.connect(self.regret)
        self.regret_button.move(640, 310)
        self.givein_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('givein'), self)
        self.givein_button.click_signal.connect(self.givein)
        self.givein_button.move(640, 380)
        # 落子标志
        self.chessman_sign = QLabel(self)
        sign = QPixmap(cfg.CHESSMAN_IMAGEPATHS.get('sign'))
        self.chessman_sign.setPixmap(sign)
        self.chessman_sign.setFixedSize(sign.size())
        self.chessman_sign.show()
        self.chessman_sign.hide()
        # 棋盘(19*19矩阵)
        self.chessboard = [[None for i in range(19)] for _ in range(19)]
        # 历史记录(悔棋用)
        self.history_record = []
        # 是否在游戏中
        self.is_gaming = True
        # 胜利方
        self.winner = None
        self.winner_info_label = None
        # 颜色分配and目前轮到谁落子
        self.player_color = 'white'
        self.ai_color = 'black'
        self.whoseround = self.player_color
        # 实例化ai
        self.ai_player = aiGobang(self.ai_color, self.player_color)
        # 落子声音加载
        pygame.mixer.init()
        # self.drop_sound = pygame.mixer.Sound(cfg.SOUNDS_PATHS.get('drop'))

    '''鼠标左键点击事件-玩家回合'''

    def mousePressEvent(self, event):
        if (event.buttons() != QtCore.Qt.LeftButton) or (self.winner is not None) or (
                self.whoseround != self.player_color) or (not self.is_gaming):
            return
        # 保证只在棋盘范围内响应
        if event.x() >= 50 and event.x() <= 50 + 30 * 18 + 14 and event.y() >= 50 and event.y() <= 50 + 30 * 18 + 14:
            pos = Pixel2Chesspos(event)
            # 保证落子的地方本来没有人落子
            if self.chessboard[pos[0]][pos[1]]:
                return
            # 实例化一个棋子并显示
            c = Chessman(self.cfg.CHESSMAN_IMAGEPATHS.get(self.whoseround), self)
            c.move(event.pos())
            c.show()
            self.chessboard[pos[0]][pos[1]] = c
            # 落子声音响起
            self.drop_sound.play()
            # 最后落子位置标志对落子位置进行跟随
            self.chessman_sign.show()
            self.chessman_sign.move(c.pos())
            self.chessman_sign.raise_()
            # 记录这次落子
            self.history_record.append([*pos, self.whoseround])
            # 是否胜利了
            self.winner = checkWin(self.chessboard)
            if self.winner:
                self.showGameEndInfo()
                return
            # 切换回合方(其实就是改颜色)
            self.nextRound()

    '''鼠标左键释放操作-调用电脑回合'''

    def mouseReleaseEvent(self, event):
        if (self.winner is not None) or (self.whoseround != self.ai_color) or (not self.is_gaming):
            return
        self.aiAct()

    '''电脑自动下-AI回合'''

    def aiAct(self):
        if (self.winner is not None) or (self.whoseround == self.player_color) or (not self.is_gaming):
            return
        next_pos = self.ai_player.act(self.history_record)
        # 实例化一个棋子并显示
        c = Chessman(self.cfg.CHESSMAN_IMAGEPATHS.get(self.whoseround), self)
        c.move(QPoint(*Chesspos2Pixel(next_pos)))
        c.show()
        self.chessboard[next_pos[0]][next_pos[1]] = c
        # 落子声音响起
        self.drop_sound.play()
        # 最后落子位置标志对落子位置进行跟随
        self.chessman_sign.show()
        self.chessman_sign.move(c.pos())
        self.chessman_sign.raise_()
        # 记录这次落子
        self.history_record.append([*next_pos, self.whoseround])
        # 是否胜利了
        self.winner = checkWin(self.chessboard)
        if self.winner:
            self.showGameEndInfo()
            return
        # 切换回合方(其实就是改颜色)
        self.nextRound()

    '''改变落子方'''

    def nextRound(self):
        self.whoseround = self.player_color if self.whoseround == self.ai_color else self.ai_color

    '''显示游戏结束结果'''

    def showGameEndInfo(self):
        self.is_gaming = False
        info_img = QPixmap(self.cfg.WIN_IMAGEPATHS.get(self.winner))
        self.winner_info_label = QLabel(self)
        self.winner_info_label.setPixmap(info_img)
        self.winner_info_label.resize(info_img.size())
        self.winner_info_label.move(50, 50)
        self.winner_info_label.show()

    '''认输'''

    def givein(self):
        if self.is_gaming and (self.winner is None) and (self.whoseround == self.player_color):
            self.winner = self.ai_color
            self.showGameEndInfo()

    '''悔棋-只有我方回合的时候可以悔棋'''

    def regret(self):
        if (self.winner is not None) or (len(self.history_record) == 0) or (not self.is_gaming) and (
                self.whoseround != self.player_color):
            return
        for _ in range(2):
            pre_round = self.history_record.pop(-1)
            self.chessboard[pre_round[0]][pre_round[1]].close()
            self.chessboard[pre_round[0]][pre_round[1]] = None
        self.chessman_sign.hide()

    '''开始游戏-之前的对弈必须已经结束才行'''

    def startgame(self):
        if self.is_gaming:
            return
        self.is_gaming = True
        self.whoseround = self.player_color
        for i, j in product(range(19), range(19)):
            if self.chessboard[i][j]:
                self.chessboard[i][j].close()
                self.chessboard[i][j] = None
        self.winner = None
        self.winner_info_label.close()
        self.winner_info_label = None
        self.history_record.clear()
        self.chessman_sign.hide()

    '''关闭窗口事件'''

    def closeEvent(self, event):
        if not self.send_back_signal:
            self.exit_signal.emit()

    '''返回游戏主页面'''

    def goHome(self):
        self.send_back_signal = True
        self.close()
        self.back_signal.emit()


'''定义按钮类'''


class PushButton(QLabel):
    click_signal = pyqtSignal()
    need_emit = False

    def __init__(self, imagepaths, parent=None, **kwargs):
        super(PushButton, self).__init__(parent)
        self.image_0 = QPixmap(imagepaths[0])
        self.image_1 = QPixmap(imagepaths[1])
        self.image_2 = QPixmap(imagepaths[2])
        self.resize(self.image_0.size())
        self.setPixmap(self.image_0)
        self.setMask(self.image_1.mask())

    '''鼠标进入按钮范围内'''

    def enterEvent(self, event):
        self.setPixmap(self.image_1)

    '''鼠标离开按钮范围内'''

    def leaveEvent(self, event):
        self.setPixmap(self.image_0)

    '''鼠标左键点击操作'''

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.need_emit = True
            self.setPixmap(self.image_2)

    '''鼠标左键释放操作'''

    def mouseReleaseEvent(self, event):
        if self.need_emit:
            self.need_emit = False
            self.setPixmap(self.image_1)
            self.click_signal.emit()


'''棋子类'''


class Chessman(QLabel):
    def __init__(self, imagepath, parent=None, **kwargs):
        super(Chessman, self).__init__(parent)
        self.color = imagepath.split('.')[-2][-5:]
        self.image = QPixmap(imagepath)
        self.setFixedSize(self.image.size())
        self.setPixmap(self.image)

    def move(self, point):
        x, y = Pixel2Chesspos(point)
        x = 30 * x + 50 - self.image.width() / 2
        y = 30 * y + 50 - self.image.height() / 2
        super().move(x, y)


'''check dir'''


def checkDir(dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
        return False
    return True


'''检查是否有人胜利'''


def checkWin(chessboard):
    # 是否是平局
    is_full = True
    for i, j in product(range(19), range(19)):
        if chessboard[i][j] is None:
            is_full = False
    if is_full:
        return 'draw'
    # 是否有人赢了
    for i, j in product(range(19), range(19)):
        # --和右边4个子连成5个
        if i < 15:
            chessmans = [chessboard[i][j], chessboard[i + 1][j], chessboard[i + 2][j], chessboard[i + 3][j],
                         chessboard[i + 4][j]]
            if None not in chessmans:
                colors = [c.color for c in chessmans]
                if len(list(set(colors))) == 1:
                    return colors[0]
        # --和下边4个子连成5个
        if j < 15:
            chessmans = [chessboard[i][j], chessboard[i][j + 1], chessboard[i][j + 2], chessboard[i][j + 3],
                         chessboard[i][j + 4]]
            if None not in chessmans:
                colors = [c.color for c in chessmans]
                if len(list(set(colors))) == 1:
                    return colors[0]
        # --和右下角4个子连成5个
        if i < 15 and j < 15:
            chessmans = [chessboard[i][j], chessboard[i + 1][j + 1], chessboard[i + 2][j + 2], chessboard[i + 3][j + 3],
                         chessboard[i + 4][j + 4]]
            if None not in chessmans:
                colors = [c.color for c in chessmans]
                if len(list(set(colors))) == 1:
                    return colors[0]
        # --和左下角4个子连成5个
        if i > 3 and j < 15:
            chessmans = [chessboard[i][j], chessboard[i - 1][j + 1], chessboard[i - 2][j + 2], chessboard[i - 3][j + 3],
                         chessboard[i - 4][j + 4]]
            if None not in chessmans:
                colors = [c.color for c in chessmans]
                if len(list(set(colors))) == 1:
                    return colors[0]
    return None


'''将像素坐标转为棋盘坐标'''


def Pixel2Chesspos(point):
    x, y = point.x(), point.y()
    x = round((x - 50.) / 30.)
    y = round((y - 50.) / 30.)
    return (x, y)


'''棋盘坐标转像素坐标'''


def Chesspos2Pixel(position):
    x = position[0] * 30 + 50
    y = position[1] * 30 + 50
    return (x, y)


'''接收并读取网络数据'''


def receiveAndReadSocketData(socket):
    data = ''
    while True:
        data_part = socket.recv(1024).decode()
        if 'END' in data_part:
            data += data_part[:data_part.index('END')]
            break
        data += data_part
    return json.loads(data, encoding='utf-8')


'''包装待发送数据'''


def packSocketData(data):
    return (json.dumps(data) + ' END').encode()


'''客户端'''


class gobangClient(QWidget):
    back_signal = pyqtSignal()
    exit_signal = pyqtSignal()
    receive_signal = pyqtSignal(dict, name='data')
    send_back_signal = False

    def __init__(self, cfg, nickname, server_ip, parent=None, **kwargs):
        super(gobangClient, self).__init__(parent)
        # 预定义一些必要的变量
        self.cfg = cfg
        self.nickname = nickname
        self.opponent_nickname = None
        self.server_ipport = (server_ip, cfg.PORT)
        self.is_gaming = False
        self.chessboard = [[None for i in range(19)] for _ in range(19)]
        self.history_record = []
        self.winner = None
        self.winner_info_label = None
        self.player_color = 'black'
        self.opponent_player_color = 'white'
        self.whoseround = None
        # 当前窗口的基本设置
        self.setFixedSize(760, 650)
        self.setWindowTitle('五子棋')
        self.setWindowIcon(QIcon(cfg.ICON_FILEPATH))
        # 背景图片
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap(cfg.BACKGROUND_IMAGEPATHS.get('bg_game'))))
        self.setPalette(palette)
        # 显示你的昵称
        self.nickname_label = QLabel('您是%s' % self.nickname, self)
        self.nickname_label.resize(200, 40)
        self.nickname_label.move(640, 180)
        # 落子标志
        self.chessman_sign = QLabel(self)
        sign = QPixmap(cfg.CHESSMAN_IMAGEPATHS.get('sign'))
        self.chessman_sign.setPixmap(sign)
        self.chessman_sign.setFixedSize(sign.size())
        self.chessman_sign.show()
        self.chessman_sign.hide()
        # 按钮
        self.home_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('home'), self)
        self.home_button.click_signal.connect(self.goHome)
        self.home_button.move(680, 10)
        self.startgame_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('startgame'), self)
        self.startgame_button.click_signal.connect(self.startgame)
        self.startgame_button.move(640, 240)
        self.regret_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('regret'), self)
        self.regret_button.click_signal.connect(self.regret)
        self.regret_button.move(640, 310)
        self.givein_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('givein'), self)
        self.givein_button.click_signal.connect(self.givein)
        self.givein_button.move(640, 380)
        self.urge_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('urge'), self)
        self.urge_button.click_signal.connect(self.urge)
        self.urge_button.move(640, 450)
        # 落子和催促声音加载
        pygame.mixer.init()
        # self.drop_sound = pygame.mixer.Sound(cfg.SOUNDS_PATHS.get('drop'))
        # self.urge_sound = pygame.mixer.Sound(cfg.SOUNDS_PATHS.get('urge'))
        # 接收数据信号绑定到responseForReceiveData函数
        self.receive_signal.connect(self.responseForReceiveData)
        # TCP/IP客户端
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.connect(self.server_ipport)
        data = {'type': 'nickname', 'data': self.nickname}
        self.tcp_socket.sendall(packSocketData(data))
        self.setWindowTitle('五子棋 ——> 已经成功连接服务器, 点击开始按钮进行游戏')
        # 开一个线程进行监听
        threading.Thread(target=self.receiveServerData).start()

    '''返回游戏主界面'''

    def goHome(self):
        self.send_back_signal = True
        self.close()
        self.back_signal.emit()

    '''开始游戏'''

    def startgame(self):
        self.randomAssignColor()
        data = {'type': 'action', 'detail': 'startgame', 'data': [self.player_color, self.opponent_player_color]}
        self.tcp_socket.sendall(packSocketData(data))
        QMessageBox.information(self, '提示', '游戏开始请求已发送, 等待对方确定中')

    '''认输'''

    def givein(self):
        if self.is_gaming and (self.winner is None) and (self.whoseround == self.player_color):
            self.winner = self.opponent_player_color
            self.showGameEndInfo()
            data = {'type': 'action', 'detail': 'givein'}
            self.tcp_socket.sendall(packSocketData(data))

    '''悔棋-只有在对方回合才能悔棋'''

    def regret(self):
        if self.is_gaming and (self.winner is None) and (self.whoseround == self.opponent_player_color):
            data = {'type': 'action', 'detail': 'regret'}
            self.tcp_socket.sendall(packSocketData(data))

    '''催促'''

    def urge(self):
        if self.is_gaming and (self.winner is None) and (self.whoseround == self.opponent_player_color):
            data = {'type': 'action', 'detail': 'urge'}
            self.tcp_socket.sendall(packSocketData(data))
            self.urge_sound.play()

    '''鼠标左键点击事件-玩家回合'''

    def mousePressEvent(self, event):
        if (event.buttons() != QtCore.Qt.LeftButton) or (self.winner is not None) or (
                self.whoseround != self.player_color) or (not self.is_gaming):
            return
        # 保证只在棋盘范围内响应
        if event.x() >= 50 and event.x() <= 50 + 30 * 18 + 14 and event.y() >= 50 and event.y() <= 50 + 30 * 18 + 14:
            pos = Pixel2Chesspos(event)
            # 保证落子的地方本来没有人落子
            if self.chessboard[pos[0]][pos[1]]:
                return
            # 实例化一个棋子并显示
            c = Chessman(self.cfg.CHESSMAN_IMAGEPATHS.get(self.whoseround), self)
            c.move(event.pos())
            c.show()
            self.chessboard[pos[0]][pos[1]] = c
            # 落子声音响起
            self.drop_sound.play()
            # 最后落子位置标志对落子位置进行跟随
            self.chessman_sign.show()
            self.chessman_sign.move(c.pos())
            self.chessman_sign.raise_()
            # 记录这次落子
            self.history_record.append([*pos, self.whoseround])
            # 发送给对方自己的落子位置
            data = {'type': 'action', 'detail': 'drop', 'data': pos}
            self.tcp_socket.sendall(packSocketData(data))
            # 是否胜利了
            self.winner = checkWin(self.chessboard)
            if self.winner:
                self.showGameEndInfo()
                return
            # 切换回合方(其实就是改颜色)
            self.nextRound()

    '''显示游戏结束结果'''

    def showGameEndInfo(self):
        self.is_gaming = False
        info_img = QPixmap(self.cfg.WIN_IMAGEPATHS.get(self.winner))
        self.winner_info_label = QLabel(self)
        self.winner_info_label.setPixmap(info_img)
        self.winner_info_label.resize(info_img.size())
        self.winner_info_label.move(50, 50)
        self.winner_info_label.show()

    '''响应接收到的数据'''

    def responseForReceiveData(self, data):
        if data['type'] == 'action' and data['detail'] == 'exit':
            QMessageBox.information(self, '提示', '您的对手已退出游戏, 游戏将自动返回主界面')
            self.goHome()
        elif data['type'] == 'action' and data['detail'] == 'startgame':
            self.opponent_player_color, self.player_color = data['data']
            self.whoseround = 'white'
            self.whoseround2nickname_dict = {self.player_color: self.nickname,
                                             self.opponent_player_color: self.opponent_nickname}
            res = QMessageBox.information(self, '提示', '对方请求(重新)开始游戏, 您为%s, 您是否同意?' % {'white': '白子', 'black': '黑子'}.get(
                self.player_color), QMessageBox.Yes | QMessageBox.No)
            if res == QMessageBox.Yes:
                data = {'type': 'reply', 'detail': 'startgame', 'data': True}
                self.tcp_socket.sendall(packSocketData(data))
                self.is_gaming = True
                self.setWindowTitle('五子棋 ——> %s走棋' % self.whoseround2nickname_dict.get(self.whoseround))
                for i, j in product(range(19), range(19)):
                    if self.chessboard[i][j]:
                        self.chessboard[i][j].close()
                        self.chessboard[i][j] = None
                self.history_record.clear()
                self.winner = None
                if self.winner_info_label:
                    self.winner_info_label.close()
                self.winner_info_label = None
                self.chessman_sign.hide()
            else:
                data = {'type': 'reply', 'detail': 'startgame', 'data': False}
                self.tcp_socket.sendall(packSocketData(data))
        elif data['type'] == 'action' and data['detail'] == 'drop':
            pos = data['data']
            # 实例化一个棋子并显示
            c = Chessman(self.cfg.CHESSMAN_IMAGEPATHS.get(self.whoseround), self)
            c.move(QPoint(*Chesspos2Pixel(pos)))
            c.show()
            self.chessboard[pos[0]][pos[1]] = c
            # 落子声音响起
            self.drop_sound.play()
            # 最后落子位置标志对落子位置进行跟随
            self.chessman_sign.show()
            self.chessman_sign.move(c.pos())
            self.chessman_sign.raise_()
            # 记录这次落子
            self.history_record.append([*pos, self.whoseround])
            # 是否胜利了
            self.winner = checkWin(self.chessboard)
            if self.winner:
                self.showGameEndInfo()
                return
            # 切换回合方(其实就是改颜色)
            self.nextRound()
        elif data['type'] == 'action' and data['detail'] == 'givein':
            self.winner = self.player_color
            self.showGameEndInfo()
        elif data['type'] == 'action' and data['detail'] == 'urge':
            self.urge_sound.play()
        elif data['type'] == 'action' and data['detail'] == 'regret':
            res = QMessageBox.information(self, '提示', '对方请求悔棋, 您是否同意?', QMessageBox.Yes | QMessageBox.No)
            if res == QMessageBox.Yes:
                pre_round = self.history_record.pop(-1)
                self.chessboard[pre_round[0]][pre_round[1]].close()
                self.chessboard[pre_round[0]][pre_round[1]] = None
                self.chessman_sign.hide()
                self.nextRound()
                data = {'type': 'reply', 'detail': 'regret', 'data': True}
                self.tcp_socket.sendall(packSocketData(data))
            else:
                data = {'type': 'reply', 'detail': 'regret', 'data': False}
                self.tcp_socket.sendall(packSocketData(data))
        elif data['type'] == 'reply' and data['detail'] == 'startgame':
            if data['data']:
                self.is_gaming = True
                self.setWindowTitle('五子棋 ——> %s走棋' % self.whoseround2nickname_dict.get(self.whoseround))
                for i, j in product(range(19), range(19)):
                    if self.chessboard[i][j]:
                        self.chessboard[i][j].close()
                        self.chessboard[i][j] = None
                self.history_record.clear()
                self.winner = None
                if self.winner_info_label:
                    self.winner_info_label.close()
                self.winner_info_label = None
                self.chessman_sign.hide()
                QMessageBox.information(self, '提示', '对方同意开始游戏请求, 您为%s, 执白者先行.' % {'white': '白子', 'black': '黑子'}.get(
                    self.player_color))
            else:
                QMessageBox.information(self, '提示', '对方拒绝了您开始游戏的请求.')
        elif data['type'] == 'reply' and data['detail'] == 'regret':
            if data['data']:
                pre_round = self.history_record.pop(-1)
                self.chessboard[pre_round[0]][pre_round[1]].close()
                self.chessboard[pre_round[0]][pre_round[1]] = None
                self.nextRound()
                QMessageBox.information(self, '提示', '对方同意了您的悔棋请求.')
            else:
                QMessageBox.information(self, '提示', '对方拒绝了您的悔棋请求.')
        elif data['type'] == 'nickname':
            self.opponent_nickname = data['data']

    '''随机生成双方颜色-白子先走'''

    def randomAssignColor(self):
        self.player_color = random.choice(['white', 'black'])
        self.opponent_player_color = 'white' if self.player_color == 'black' else 'black'
        self.whoseround = 'white'
        self.whoseround2nickname_dict = {self.player_color: self.nickname,
                                         self.opponent_player_color: self.opponent_nickname}

    '''改变落子方'''

    def nextRound(self):
        self.whoseround = self.player_color if self.whoseround == self.opponent_player_color else self.opponent_player_color
        self.setWindowTitle('五子棋 ——> %s走棋' % self.whoseround2nickname_dict.get(self.whoseround))

    '''接收服务器端数据'''

    def receiveServerData(self):
        while True:
            data = receiveAndReadSocketData(self.tcp_socket)
            self.receive_signal.emit(data)

    '''关闭窗口事件'''

    def closeEvent(self, event):
        self.tcp_socket.sendall(packSocketData({'type': 'action', 'detail': 'exit'}))
        self.tcp_socket.shutdown(socket.SHUT_RDWR)
        self.tcp_socket.close()
        return super().closeEvent(event)


'''联机对战'''


class playOnlineUI(QWidget):
    def __init__(self, cfg, home_ui, parent=None, **kwargs):
        super(playOnlineUI, self).__init__(parent)
        self.cfg = cfg
        self.home_ui = home_ui
        self.setWindowTitle('联机对战')
        self.setWindowIcon(QIcon(cfg.ICON_FILEPATH))
        self.setFixedSize(300, 200)
        # 昵称
        self.nickname = random.choice(['杰尼龟', '皮卡丘', '小火龙', '小锯鳄', '妙蛙种子', '菊草叶'])
        self.layout0 = QHBoxLayout()
        self.nickname_label = QLabel('游戏昵称:', self)
        self.nickname_edit = QLineEdit(self)
        self.nickname_edit.setText(self.nickname)
        self.layout0.addWidget(self.nickname_label, 1)
        self.layout0.addWidget(self.nickname_edit, 3)
        # IP
        self.target_ip = '127.0.0.1'
        self.layout1 = QHBoxLayout()
        self.ip_label = QLabel('对方IP:', self)
        self.ip_edit = QLineEdit(self)
        self.ip_edit.setText(self.target_ip)
        self.layout1.addWidget(self.ip_label, 1)
        self.layout1.addWidget(self.ip_edit, 3)
        # 按钮
        self.layout2 = QHBoxLayout()
        self.connect_button = QPushButton('作为客户端', self)
        self.connect_button.clicked.connect(self.becomeClient)
        self.ashost_button = QPushButton('作为服务器', self)
        self.ashost_button.clicked.connect(self.becomeHost)
        self.layout2.addWidget(self.connect_button)
        self.layout2.addWidget(self.ashost_button)
        # 布局
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.layout0)
        self.layout.addLayout(self.layout1)
        self.layout.addLayout(self.layout2)
        self.setLayout(self.layout)

    '''作为客户端'''

    def becomeClient(self):
        self.close()
        self.nickname = self.nickname_edit.text()
        self.target_ip = self.ip_edit.text()
        self.client_ui = gobangClient(cfg=self.cfg, nickname=self.nickname, server_ip=self.target_ip)
        self.client_ui.exit_signal.connect(lambda: sys.exit())
        self.client_ui.back_signal.connect(self.home_ui.show)
        self.client_ui.show()

    '''作为服务器'''

    def becomeHost(self):
        self.close()
        self.nickname = self.nickname_edit.text()
        self.server_ui = gobangSever(cfg=self.cfg, nickname=self.nickname)
        self.server_ui.exit_signal.connect(lambda: sys.exit())
        self.server_ui.back_signal.connect(self.home_ui.show)
        self.server_ui.show()


'''服务器端'''


class gobangSever(QWidget):
    back_signal = pyqtSignal()
    exit_signal = pyqtSignal()
    receive_signal = pyqtSignal(dict, name='data')
    send_back_signal = False

    def __init__(self, cfg, nickname, parent=None, **kwargs):
        super(gobangSever, self).__init__(parent)
        # 预定义一些必要的变量
        self.cfg = cfg
        self.nickname = nickname
        self.opponent_nickname = None
        self.client_ipport = None
        self.is_gaming = False
        self.chessboard = [[None for i in range(19)] for _ in range(19)]
        self.history_record = []
        self.winner = None
        self.winner_info_label = None
        self.player_color = 'white'
        self.opponent_player_color = 'black'
        self.whoseround = None
        # 当前窗口的基本设置
        self.setFixedSize(760, 650)
        self.setWindowTitle('五子棋')
        self.setWindowIcon(QIcon(cfg.ICON_FILEPATH))
        # 背景图片
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap(cfg.BACKGROUND_IMAGEPATHS.get('bg_game'))))
        self.setPalette(palette)
        # 显示你的昵称
        self.nickname_label = QLabel('您是%s' % self.nickname, self)
        self.nickname_label.resize(200, 40)
        self.nickname_label.move(640, 180)
        # 落子标志
        self.chessman_sign = QLabel(self)
        sign = QPixmap(cfg.CHESSMAN_IMAGEPATHS.get('sign'))
        self.chessman_sign.setPixmap(sign)
        self.chessman_sign.setFixedSize(sign.size())
        self.chessman_sign.show()
        self.chessman_sign.hide()
        # 按钮
        self.home_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('home'), self)
        self.home_button.click_signal.connect(self.goHome)
        self.home_button.move(680, 10)
        self.startgame_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('startgame'), self)
        self.startgame_button.click_signal.connect(self.startgame)
        self.startgame_button.move(640, 240)
        self.regret_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('regret'), self)
        self.regret_button.click_signal.connect(self.regret)
        self.regret_button.move(640, 310)
        self.givein_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('givein'), self)
        self.givein_button.click_signal.connect(self.givein)
        self.givein_button.move(640, 380)
        self.urge_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('urge'), self)
        self.urge_button.click_signal.connect(self.urge)
        self.urge_button.move(640, 450)
        # 落子和催促声音加载
        pygame.mixer.init()
        # self.drop_sound = pygame.mixer.Sound(cfg.SOUNDS_PATHS.get('drop'))
        # self.urge_sound = pygame.mixer.Sound(cfg.SOUNDS_PATHS.get('urge'))
        # 接收数据信号绑定到responseForReceiveData函数
        self.receive_signal.connect(self.responseForReceiveData)
        # TCP/IP服务器
        self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server.bind(('0.0.0.0', cfg.PORT))
        self.tcp_server.listen(1)
        # TCP/IP的socket
        self.tcp_socket = None
        # 开一个线程进行监听
        threading.Thread(target=self.startListen).start()

    '''返回游戏主界面'''

    def goHome(self):
        self.send_back_signal = True
        self.close()
        self.back_signal.emit()

    '''开始游戏'''

    def startgame(self):
        if self.tcp_socket is None:
            QMessageBox.information(self, '提示', '对方未连接, 请耐心等待')
        else:
            self.randomAssignColor()
            data = {'type': 'action', 'detail': 'startgame', 'data': [self.player_color, self.opponent_player_color]}
            self.tcp_socket.sendall(packSocketData(data))
            QMessageBox.information(self, '提示', '游戏开始请求已发送, 等待对方确定中')

    '''认输'''

    def givein(self):
        if self.tcp_socket and self.is_gaming and (self.winner is None) and (self.whoseround == self.player_color):
            self.winner = self.opponent_player_color
            self.showGameEndInfo()
            data = {'type': 'action', 'detail': 'givein'}
            self.tcp_socket.sendall(packSocketData(data))

    '''悔棋-只有在对方回合才能悔棋'''

    def regret(self):
        if self.tcp_socket and self.is_gaming and (self.winner is None) and (
                self.whoseround == self.opponent_player_color):
            data = {'type': 'action', 'detail': 'regret'}
            self.tcp_socket.sendall(packSocketData(data))

    '''催促'''

    def urge(self):
        if self.tcp_socket and self.is_gaming and (self.winner is None) and (
                self.whoseround == self.opponent_player_color):
            data = {'type': 'action', 'detail': 'urge'}
            self.tcp_socket.sendall(packSocketData(data))
            self.urge_sound.play()

    '''鼠标左键点击事件-玩家回合'''

    def mousePressEvent(self, event):
        if (self.tcp_socket is None) or (event.buttons() != QtCore.Qt.LeftButton) or (self.winner is not None) or (
                self.whoseround != self.player_color) or (not self.is_gaming):
            return
        # 保证只在棋盘范围内响应
        if event.x() >= 50 and event.x() <= 50 + 30 * 18 + 14 and event.y() >= 50 and event.y() <= 50 + 30 * 18 + 14:
            pos = Pixel2Chesspos(event)
            # 保证落子的地方本来没有人落子
            if self.chessboard[pos[0]][pos[1]]:
                return
            # 实例化一个棋子并显示
            c = Chessman(self.cfg.CHESSMAN_IMAGEPATHS.get(self.whoseround), self)
            c.move(event.pos())
            c.show()
            self.chessboard[pos[0]][pos[1]] = c
            # 落子声音响起
            self.drop_sound.play()
            # 最后落子位置标志对落子位置进行跟随
            self.chessman_sign.show()
            self.chessman_sign.move(c.pos())
            self.chessman_sign.raise_()
            # 记录这次落子
            self.history_record.append([*pos, self.whoseround])
            # 发送给对方自己的落子位置
            data = {'type': 'action', 'detail': 'drop', 'data': pos}
            self.tcp_socket.sendall(packSocketData(data))
            # 是否胜利了
            self.winner = checkWin(self.chessboard)
            if self.winner:
                self.showGameEndInfo()
                return
            # 切换回合方(其实就是改颜色)
            self.nextRound()

    '''显示游戏结束结果'''

    def showGameEndInfo(self):
        self.is_gaming = False
        info_img = QPixmap(self.cfg.WIN_IMAGEPATHS.get(self.winner))
        self.winner_info_label = QLabel(self)
        self.winner_info_label.setPixmap(info_img)
        self.winner_info_label.resize(info_img.size())
        self.winner_info_label.move(50, 50)
        self.winner_info_label.show()

    '''响应接收到的数据'''

    def responseForReceiveData(self, data):
        if data['type'] == 'action' and data['detail'] == 'exit':
            QMessageBox.information(self, '提示', '您的对手已退出游戏, 游戏将自动返回主界面')
            self.goHome()
        elif data['type'] == 'action' and data['detail'] == 'startgame':
            self.opponent_player_color, self.player_color = data['data']
            self.whoseround = 'white'
            self.whoseround2nickname_dict = {self.player_color: self.nickname,
                                             self.opponent_player_color: self.opponent_nickname}
            res = QMessageBox.information(self, '提示', '对方请求(重新)开始游戏, 您为%s, 您是否同意?' % {'white': '白子', 'black': '黑子'}.get(
                self.player_color), QMessageBox.Yes | QMessageBox.No)
            if res == QMessageBox.Yes:
                data = {'type': 'reply', 'detail': 'startgame', 'data': True}
                self.tcp_socket.sendall(packSocketData(data))
                self.is_gaming = True
                self.setWindowTitle('五子棋 ——> %s走棋' % self.whoseround2nickname_dict.get(self.whoseround))
                for i, j in product(range(19), range(19)):
                    if self.chessboard[i][j]:
                        self.chessboard[i][j].close()
                        self.chessboard[i][j] = None
                self.history_record.clear()
                self.winner = None
                if self.winner_info_label:
                    self.winner_info_label.close()
                self.winner_info_label = None
                self.chessman_sign.hide()
            else:
                data = {'type': 'reply', 'detail': 'startgame', 'data': False}
                self.tcp_socket.sendall(packSocketData(data))
        elif data['type'] == 'action' and data['detail'] == 'drop':
            pos = data['data']
            # 实例化一个棋子并显示
            c = Chessman(self.cfg.CHESSMAN_IMAGEPATHS.get(self.whoseround), self)
            c.move(QPoint(*Chesspos2Pixel(pos)))
            c.show()
            self.chessboard[pos[0]][pos[1]] = c
            # 落子声音响起
            self.drop_sound.play()
            # 最后落子位置标志对落子位置进行跟随
            self.chessman_sign.show()
            self.chessman_sign.move(c.pos())
            self.chessman_sign.raise_()
            # 记录这次落子
            self.history_record.append([*pos, self.whoseround])
            # 是否胜利了
            self.winner = checkWin(self.chessboard)
            if self.winner:
                self.showGameEndInfo()
                return
            # 切换回合方(其实就是改颜色)
            self.nextRound()
        elif data['type'] == 'action' and data['detail'] == 'givein':
            self.winner = self.player_color
            self.showGameEndInfo()
        elif data['type'] == 'action' and data['detail'] == 'urge':
            self.urge_sound.play()
        elif data['type'] == 'action' and data['detail'] == 'regret':
            res = QMessageBox.information(self, '提示', '对方请求悔棋, 您是否同意?', QMessageBox.Yes | QMessageBox.No)
            if res == QMessageBox.Yes:
                pre_round = self.history_record.pop(-1)
                self.chessboard[pre_round[0]][pre_round[1]].close()
                self.chessboard[pre_round[0]][pre_round[1]] = None
                self.chessman_sign.hide()
                self.nextRound()
                data = {'type': 'reply', 'detail': 'regret', 'data': True}
                self.tcp_socket.sendall(packSocketData(data))
            else:
                data = {'type': 'reply', 'detail': 'regret', 'data': False}
                self.tcp_socket.sendall(packSocketData(data))
        elif data['type'] == 'reply' and data['detail'] == 'startgame':
            if data['data']:
                self.is_gaming = True
                self.setWindowTitle('五子棋 ——> %s走棋' % self.whoseround2nickname_dict.get(self.whoseround))
                for i, j in product(range(19), range(19)):
                    if self.chessboard[i][j]:
                        self.chessboard[i][j].close()
                        self.chessboard[i][j] = None
                self.history_record.clear()
                self.winner = None
                if self.winner_info_label:
                    self.winner_info_label.close()
                self.winner_info_label = None
                self.chessman_sign.hide()
                QMessageBox.information(self, '提示', '对方同意开始游戏请求, 您为%s, 执白者先行.' % {'white': '白子', 'black': '黑子'}.get(
                    self.player_color))
            else:
                QMessageBox.information(self, '提示', '对方拒绝了您开始游戏的请求.')
        elif data['type'] == 'reply' and data['detail'] == 'regret':
            if data['data']:
                pre_round = self.history_record.pop(-1)
                self.chessboard[pre_round[0]][pre_round[1]].close()
                self.chessboard[pre_round[0]][pre_round[1]] = None
                self.nextRound()
                QMessageBox.information(self, '提示', '对方同意了您的悔棋请求.')
            else:
                QMessageBox.information(self, '提示', '对方拒绝了您的悔棋请求.')
        elif data['type'] == 'nickname':
            self.opponent_nickname = data['data']

    '''随机生成双方颜色-白子先走'''

    def randomAssignColor(self):
        self.player_color = random.choice(['white', 'black'])
        self.opponent_player_color = 'white' if self.player_color == 'black' else 'black'
        self.whoseround = 'white'
        self.whoseround2nickname_dict = {self.player_color: self.nickname,
                                         self.opponent_player_color: self.opponent_nickname}

    '''改变落子方'''

    def nextRound(self):
        self.whoseround = self.player_color if self.whoseround == self.opponent_player_color else self.opponent_player_color
        self.setWindowTitle('五子棋 ——> %s走棋' % self.whoseround2nickname_dict.get(self.whoseround))

    '''开始监听客户端的连接'''

    def startListen(self):
        while True:
            try:
                self.setWindowTitle('五子棋 ——> 服务器端启动成功, 等待客户端连接中')
                self.tcp_socket, self.client_ipport = self.tcp_server.accept()
                self.setWindowTitle('五子棋 ——> 客户端已连接, 点击开始按钮进行游戏')
                data = {'type': 'nickname', 'data': self.nickname}
                self.tcp_socket.sendall(packSocketData(data))
                self.receiveClientData()
            except:
                break

    '''接收客户端数据'''

    def receiveClientData(self):
        while True:
            data = receiveAndReadSocketData(self.tcp_socket)
            self.receive_signal.emit(data)

    '''关闭窗口事件'''

    def closeEvent(self, event):
        if self.tcp_socket:
            self.tcp_socket.sendall(packSocketData({'type': 'action', 'detail': 'exit'}))
            self.tcp_socket.shutdown(socket.SHUT_RDWR)
            self.tcp_socket.close()
        self.tcp_server.close()
        return super().closeEvent(event)


'''run'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    handle = gameStartUI()
    font = QFont()
    font.setPointSize(12)
    handle.setFont(font)
    handle.show()
    sys.exit(app.exec_())
