# coding: utf-8
from fugle_realtime import intraday
import configparser
import re
from pprint import pprint as pp
import numpy as np
from dateutil import parser
import datetime


class ReplyTool:
    config = configparser.ConfigParser()
    config.read('config.ini')
    TOKEN = config['FUGLE']['API_TOKEN']

    @staticmethod
    def is_valid_cmd(input_text: str) -> bool:
        pattern = r'^\S+\ (l|t|b|a|ts)$'

        if re.match(pattern, input_text):
            return True
        else:
            return False

    @staticmethod
    def get_task_info(input_text: str) -> dict:
        result = dict()
        tokens = input_text.split(' ')
        result['type'] = tokens[1]
        result['target'] = tokens[0]

        return result

    @staticmethod
    def get_stock_name(target: str):
        data = intraday.meta(apiToken=ReplyTool.TOKEN, output='raw', symbolId=target)
        if 'error' not in data.keys():
            return data.get('nameZhTw')
        else:
            return False

    @staticmethod
    def npt_to_datetime(input_time: np.datetime64):
        parse_dt = datetime.datetime.utcfromtimestamp(input_time.astype('O') / 1e9) + \
                   datetime.timedelta(hours=8)

        return parse_dt

    @staticmethod
    def str_to_datetime(input_time: str):
        input_time = (parser.isoparse(input_time) + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
        return input_time

    @staticmethod
    def reply_helper(input_text: str) -> str:
        if ReplyTool.is_valid_cmd(input_text):
            task_info = ReplyTool.get_task_info(input_text)
            task_type = task_info['type']
            target = task_info['target']

            if task_type == 'l':
                return ReplyTool.latest_helper(target)
            elif task_type == 't':
                return ReplyTool.trade_helper(target)
            elif task_type == 'b':
                return ReplyTool.basic_helper(target)

        else:
            msg = '戴夫，你的指令可不可以好好打?'
            return msg

    @staticmethod
    def latest_helper(target: str) -> str:
        name = ReplyTool.get_stock_name(target)
        if name:
            df = intraday.chart(apiToken=ReplyTool.TOKEN, output='dataframe', symbolId=target).tail(1)
            last_time = ReplyTool.npt_to_datetime(df['at'].values[0])

            curr_open = df['open'].values[0]
            curr_close = df['close'].values[0]
            curr_high = df['high'].values[0]
            curr_low = df['low'].values[0]
            curr_count = df['unit'].values[0]
            curr_value = df['volume'].values[0]

            msg = '{} - {}\n' \
                  '最新: {}\n\n' \
                  '當時開盤價: {}\n\n' \
                  '當時收盤價: {}\n\n' \
                  '當時最高價: {}\n\n' \
                  '當時最低價: {}\n\n' \
                  '當時交易張數: {}\n\n' \
                  '當時交易金額: {}'.format(target, name, last_time,
                                      curr_open, curr_close, curr_high,
                                      curr_low, curr_count, curr_value)
            return msg
        else:
            msg = '戴夫，台股根本沒這支股票，可不可以查清楚再來?'
            return msg

    @staticmethod
    def trade_helper(target: str) -> str:
        name = ReplyTool.get_stock_name(target)
        if name:
            df = intraday.quote(apiToken=ReplyTool.TOKEN, output='dataframe', symbolId=target)
            daily_count = df['total.unit'].values[0]
            daily_value = df['total.volume'].values[0]
            daily_high_time = ReplyTool.str_to_datetime(df['priceHigh.at'].values[0])
            daily_high = df['priceHigh.price'].values[0]
            daily_low_time = ReplyTool.str_to_datetime(df['priceLow.at'].values[0])
            daily_low = df['priceLow.price'].values[0]

            msg = '{} - {}\n\n' \
                  '當日總成交張數: {}\n' \
                  '當日總成交價: {}\n\n' \
                  '當日最高價:\n' \
                  '- {}\n' \
                  '- {}\n\n' \
                  '當日最低價:\n' \
                  '- {}\n' \
                  '- {}\n\n'.format(target, name, daily_count, daily_value,
                                    daily_high_time, daily_high, daily_low_time, daily_low
                                    )
            return msg
        else:
            msg = '戴夫，台股根本沒這支股票，可不可以查清楚再來?'
            return msg

    @staticmethod
    def basic_helper(target: str):
        data = intraday.meta(apiToken=ReplyTool.TOKEN, output='raw', symbolId=target)
        if 'error' in data.keys():
            msg = '戴夫，台股根本沒這支股票，可不可以查清楚再來?'
            return msg

        industry = data['industryZhTw']
        category = data['typeZhTw']
        ref_price = data['priceReference']
        high_limit = data['priceHighLimit']
        low_limit = data['priceLowLimit']

        day_buy_sell = ''
        dbs = data['canDayBuySell']
        if dbs:
            day_buy_sell = '可買後即賣當沖'
        else:
            day_buy_sell = '不可買後即賣當沖'

        day_sell_buy = ''
        dsb = data['canDaySellBuy']
        if dsb:
            day_sell_buy = '可賣後現買當沖'
        else:
            day_sell_buy = '不可賣後現買當沖'

        short_margin = ''
        sm = data['canShortMargin']
        if sm:
            short_margin = '可豁免平盤下融券賣出'
        else:
            short_margin = '不可豁免平盤下融券賣出'

        short_lend = ''
        sl = data['canShortLend']
        if sl:
            short_lend = '可豁免平盤下借券賣出'
        else:
            short_lend = '不可豁免平盤下借券賣出'

        is_terminated = ''
        terminated = data['isTerminated']
        if terminated:
            is_terminated = '今日已終止上市'
        else:
            is_terminated = '今日仍上市'

        is_suspended = ''
        suspended = data['isSuspended']
        if suspended:
            is_suspended = '今日暫停買賣'
        else:
            is_suspended = '今日正常買賣'

        if 'error' not in data.keys():
            name = data['nameZhTw']
            msg = '{} - {}\n\n' \
                  '- 產業別: {}\n' \
                  '- 股票別: {}\n\n' \
                  '- 今日參考價: {}\n' \
                  '- 漲停價: {}\n' \
                  '- 跌停價: {}\n\n' \
                  '- {}\n' \
                  '- {}\n' \
                  '- {}\n' \
                  '- {}\n\n' \
                  '- {}\n' \
                  '- {}\n'.format(target, name, industry, category,
                                  ref_price, high_limit, low_limit,
                                  day_buy_sell, day_sell_buy, short_margin, short_lend,
                                  is_terminated, is_suspended)
            return msg
        else:
            msg = '戴夫，台股根本沒這支股票，可不可以查清楚再來?'
            return msg
