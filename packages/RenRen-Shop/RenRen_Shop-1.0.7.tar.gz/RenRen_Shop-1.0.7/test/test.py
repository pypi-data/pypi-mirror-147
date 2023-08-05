# -*- coding: utf-8 -*-
"""
@Time : 2022/4/6 15:07 
@Author : YarnBlue 
@description : 
@File : test.py 
"""
import datetime
import json
import random
import time

from RenRen_Shop.configs.configs import DELAY
from RenRen_Shop.factory import Factory
from RenRen_Shop.common.price_interface import PriceInterface
from RenRen_Shop.common.conDB import connection_db


class option_price(PriceInterface):
    def call(self, **kwargs):
        db = connection_db('127.0.0.1', 'renrenmall', 'root', 'root').db()
        cursor = db.cursor()
        if 'sku_id' in kwargs.keys():
            sku_id = kwargs['sku_id']
            sql = f'select seckill_price from goods_price where sku_id="{sku_id}"'
        elif 'goods_id' in kwargs.keys():
            goods_id = kwargs['goods_id']
            sql = f'select seckill_price from goods_price where id="{goods_id}"'
        else:
            raise Exception('IdError')
        try:
            cursor.execute(sql)
            price = cursor.fetchone()[0]
        except Exception as e:
            raise Exception(e)
        finally:
            db.close()
        return float(price)


def main(client: Factory):
    Fetcher = client.seckill.FetchSecKillList
    Fetcher.next(keyword='整点秒杀')
    seckill_list = Fetcher.result()
    seckill_ids = list()
    for each in seckill_list:
        seckill_ids.append(int(each['id']))
    diypage_info = client.diypage.page_info(1603, 10)
    diypage_content = json.loads(diypage_info['content'])
    seckill_contents = client.diypage.PageContent.fetch_content(diypage_content, 'seckill')
    for index, each in enumerate(seckill_contents):
        diypage_content[each[0]] = client.diypage.PageContent.secKill_edit(each[1],
                                                                           params__activityData__id=
                                                                           seckill_ids[-1 - index])
    diypage_info['content'] = diypage_content
    if client.diypage.page_eidt(**diypage_info):
        client.logger.info('Done!')


def seckill(client):
    start_dt = '2022-04-14 14:00:00'
    data = {
        'create_time[]': ['2022-03-13 00:00', '2022-04-11 00:00'],
        'category_id': 3396
    }
    client.app.MySecKill.add_mySecKill_with_filter_and_time(start_dt, **data)


def daily_seckill(client: Factory):
    """
    随机获取1/7的商品，加入每日特价组，按大促的价格，并编辑主页内容，实现每日特价功能
    :param client:
    :return:
    """
    goods_ids = client.goods.filter_goods(key='category__0__category_id', value=3858, judge='=')
    for goods_id in goods_ids:
        client.goods.EditGoods.goods_del_category(goods_id, 3858)
        time.sleep(client.DELAY)
    client.logger.info('去除昨日特价')
    fetcher = client.seckill.FetchSecKillList
    fetcher.next(keyword='每日特价')
    for result in fetcher.result():
        seckill_id = result['id']
        if client.seckill.seckill_delete(seckill_id):
            client.logger.info(f'删除秒杀活动：{result["title"]}')
        time.sleep(DELAY)
    goods_ids = client.goods.filter_goods(key='category__0__category_id', value=3396, judge='!=')
    goods_count = len(goods_ids)
    goods_ids = random.sample(goods_ids, int(round(goods_count / 7)))
    if client.group.update_groups('每日特价', *goods_ids):
        client.logger.info(f'{len(goods_ids)}个商品成功加入每日特价')
    client.category.set_category(0, [3858], *goods_ids)
    start_time = f'{datetime.date.today()} 00:00:00'
    duration = 24 * 3600
    iterface = option_price()
    if client.seckill.seckill_add_quick(iterface,
                                        *goods_ids,
                                        start_time=start_time,
                                        duration=duration,
                                        title='每日特价'):
        client.logger.info('每日特价秒杀活动新建成功')


if __name__ == '__main__':
    with Factory() as client:
        daily_seckill(client)
