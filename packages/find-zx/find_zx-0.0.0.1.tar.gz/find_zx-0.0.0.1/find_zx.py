import cv2
import mss
import numpy as np


# 默认匹配程度为0.6
def identify_gap(bg, tp):
    '''
    bg: 背景图片
    tp: 缺口图片
    out:输出图片
    '''
    # 读取背景图片和缺口图片
    # bg_img = cv2.imread(bg)  # 背景图片
    tp_img = cv2.imread(tp)  # 缺口图片

    # 识别图片边缘
    bg_edge = cv2.Canny(bg, 100, 200)
    tp_edge = cv2.Canny(tp_img, 100, 200)

    # 转换图片格式
    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)

    # 缺口匹配
    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配
    if max_val < 0.6:
        return -114514
    # 绘制方框
    th, tw = tp_pic.shape[:2]
    tl = max_loc  # 左上角点的坐标
    br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
    cv2.rectangle(bg, tl, br, (0, 0, 255), 2)  # 绘制矩形

    # cv2.imwrite(out, bg_img)  # 保存在本地
    # 返回缺口的X坐标
    return tl, br


# 自定义匹配程度m
def matching(bg, tp, m):
    '''
    bg: 背景图片
    tp: 缺口图片
    out:输出图片
    '''
    # 读取背景图片和缺口图片
    # bg_img = cv2.imread(bg)  # 背景图片
    tp_img = cv2.imread(tp)  # 缺口图片

    # 识别图片边缘
    bg_edge = cv2.Canny(bg, 100, 200)
    tp_edge = cv2.Canny(tp_img, 100, 200)

    # 转换图片格式
    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)

    # 缺口匹配
    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配
    if max_val < m:
        return -114514
    # 绘制方框
    th, tw = tp_pic.shape[:2]
    tl = max_loc  # 左上角点的坐标
    br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
    cv2.rectangle(bg, tl, br, (0, 0, 255), 2)  # 绘制矩形

    # cv2.imwrite(out, bg_img)  # 保存在本地
    # 返回缺口的X坐标
    return tl, br


# 定位搜寻图片位置的中心点
def find(p):
    sec = mss.mss()
    screen = {
        'left': 0,
        'top': 0,
        'width': 1027,
        'height': 794
    }
    img = sec.grab(screen)
    img = np.array(img)
    a = identify_gap(img, p)
    if a == -114514:
        findx = False
    else:
        x = a[0][0] + ((a[1][0] - a[0][0]) / 2)
        y = a[0][1] + ((a[1][1] - a[0][1]) / 2)
        pos = ((int(x), int(y)))
        return pos


# 在限定区域内寻找对应图片
def find_limit(p, l, t, w, h):
    sec = mss.mss()
    screen = {
        'left': l,
        'top': t,
        'width': w,
        'height': h
    }
    img = sec.grab(screen)
    img = np.array(img)
    a = identify_gap(img, p)
    if a == -114514:
        # print('未找到位置')
        return None
    else:
        # hwnd = win32gui.FindWindow("DagorWClass", None)
        x = a[0][0] + ((a[1][0] - a[0][0]) / 2)
        y = a[0][1] + ((a[1][1] - a[0][1]) / 2)
        pos = ((int(x), int(y)))
        return pos


# 全屏范围寻找，自定义匹配程度
def find_match(p, m):
    sec = mss.mss()
    screen = {
        'left': 0,
        'top': 0,
        'width': 1027,
        'height': 794
    }
    img = sec.grab(screen)
    img = np.array(img)
    # cv2.imshow('111',img)
    # cv2.waitKey(3000)
    a = matching(img, p, m)
    if a == -114514:
        findx = False
    else:
        # hwnd = win32gui.FindWindow("DagorWClass", None)
        x = a[0][0] + ((a[1][0] - a[0][0]) / 2)
        y = a[0][1] + ((a[1][1] - a[0][1]) / 2)
        pos = ((int(x), int(y)))
        return pos


# 限定范围寻找，自定义匹配程度
def find_lit_mat(p, m, l, t, w, h):
    sec = mss.mss()
    screen = {
        'left': l,
        'top': t,
        'width': w,
        'height': h
    }
    img = sec.grab(screen)
    img = np.array(img)
    # cv2.imshow('111',img)
    # cv2.waitKey(3000)
    a = matching(img, p, m)
    if a == -114514:
        findx = False
    else:
        # hwnd = win32gui.FindWindow("DagorWClass", None)
        x = a[0][0] + ((a[1][0] - a[0][0]) / 2)
        y = a[0][1] + ((a[1][1] - a[0][1]) / 2)
        pos = ((int(x), int(y)))
        return pos