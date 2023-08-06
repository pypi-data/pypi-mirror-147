# Insert your code here. 
import requests
import pandas as pd


class StockSpider:
    """
    爬取股票交易信息。
    """
    def __init__(self):
        """
        对象参数成员：
            url1：接口url
            default_params1：数据属性
        """
        self.encoding = "GBK"
        self.url1 = "http://quotes.money.163.com/service/chddata.html"
        self.default_params1 = ["TCLOSE", "HIGH", "LOW", "TOPEN", "LCLOSE", "CHG", "PCHG", "TURNOVER", "VOTURNOVER", "VATURNOVER", "TCAP", "MCAP"]

    def get(self, exchange, code, start, end, params=None):
        """
        获取历史（按日）交易信息
        :param exchange: 交易所信息  数据类型：int   交易所信息 0：上证交易所；1：深圳交易所
        :param code: 股票代码   数据类型：str
        :param start: 开始日期  数据类型：str    格式：yyyyMMdd
        :param end: 结束日期    数据类型：str    格式：yyyyMMdd
        :param params: 访问数据类型   数据类型：List[str]
            TCLOSE: 收盘价
            HIGH: 当日最高
            LOW: 当日最低
            TOPEN: 开盘价
            LCLOSE: 前收盘
            CHG: 涨跌额
            PCHG: 涨跌幅
            TURNOVER: 换手率
            VATURNOVER: 成交量
            VOTURNOVER: 成交金额
            TCAP: 总市值
            MCAP: 流通市值

        :return: DataFrame对象
        """
        if not params:
            params = self.default_params1
        query = {
            "code": str(exchange) + code,
            "start": start,
            "end": end,
            "fields": ";".join(params)
        }
        response = requests.get(self.url1, params=query)
        response.encoding = self.encoding

        # 处理数据格式
        text_ls = response.text.split(sep='\n')
        new_ls = []
        for i in text_ls:
            new_ls.append(i.split(','))

        columns = new_ls[0]
        columns[-1] = columns[-1][:-1]
        new_ls.pop(-1)
        data = new_ls[:0:-1]
        for i in range(len(data)):
            data[i][-1] = data[i][-1][:-1]
        df = pd.DataFrame(data=data, columns=columns)
        return df

