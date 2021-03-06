# -*- coding:utf-8 -*-
"""
2019新春五福活动
"""
from utils.mysql_util import mysql_util
import logging
from utils import util

try:
    from log.my_logger import modian_logger as my_logger
except:
    my_logger = logging.getLogger(__name__)
import time

FU_POOL = ['健康福', '好运福', '巨款福', '事业福', '和平福', '解锁一条新年祝福:鼠年吉祥，祝你2020新年快乐呀']
FU_CHANCE = [1, 4, 10, 10, 25, 50]


def compute_draw_nums(backer_money):
    """
    计算抽福张数
    每集资10.17抽一张
    集资达到101.7抽11张
    :param backer_money:
    :return:
    """
    if backer_money < 10.17:
        return 0
    elif backer_money < 101.7:
        return int(backer_money // 10.17)
    else:
        tmp1 = int(backer_money // 101.7) * 11
        tmp2 = int((backer_money % 101.7) // 10.17)
        return tmp1 + tmp2


def can_draw():
    """
    是否可以抽中福, 概率1/2
    :return:
    """
    candidates = [i for i in range(2)]
    rst = util.choice(candidates)
    my_logger.debug('是否抽中福: %s' % (rst[0] < 1))
    return rst[0] < 1


def draw(user_id, nickname, backer_money, pay_time):
    my_logger.info('抽卡: user_id: %s, nickname: %s, backer_money: %s, pay_time: %s',
                   user_id, nickname, backer_money, pay_time)
    # 计算抽卡张数
    card_num = compute_draw_nums(backer_money)

    if card_num == 0:
        my_logger.info('集资未达到标准，无法抽卡')
        return ''

    my_logger.info('共抽卡%d张', card_num)
    fu_dict = {}

    flag = False  # 是否执行数据库插入语句
    insert_sql = 'insert into t_draw_fu_record (`modian_id`, `fu_idx`, `fu_name`, `update_time`) VALUES '
    for no in range(card_num):
        # draw_rst = can_draw()
        # if not draw_rst:
        #     continue
        flag = True
        idx = util.weight_choice(FU_POOL, FU_CHANCE)

        insert_sql += '(\'{}\', {}, \'{}\', \'{}\'), '.format(user_id, idx, FU_POOL[idx],
                                                          util.convert_timestamp_to_timestr(int(time.time() * 1000)))
        if idx not in fu_dict:
            fu_dict[idx] = 1
        else:
            fu_dict[idx] += 1

    if len(fu_dict) <= 0:
        return ''
    report = '恭喜抽中: '
    for key, value in fu_dict.items():
        report += '{}*{}, '.format(FU_POOL[key], value)
    if flag:
        print(insert_sql.strip()[:-1])
        mysql_util.query(insert_sql.strip()[:-1])
    print(report)
    return report + '\n'


if __name__ == "__main__":
    # draw('987758', 'Nanjo恩恩', 10.17, '2019-02-08 12:00:41')
    # print(draw('阿钰', '阿钰', 52, '2020-01-24 20:56:57'))
    # print(draw('阿钰', '阿钰', 10.17, '2020-01-24 22:44:50'))
    print(draw("Umi'Mimori", "Umi'Mimori", 10.17, '2020-01-25 03:27:22'))
    # print(draw("Dack", "Dack", 10.17, '2020-01-24 21:29:07'))
    # print(draw("Dack", "Dack", 10.17, '2020-01-24 20:52:51'))
    # print(draw("kakaxi", "kakaxi", 10.17, '2020-01-24 20:56:50'))
    pass
