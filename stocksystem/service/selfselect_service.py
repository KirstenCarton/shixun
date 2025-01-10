from flask import logging
from model.selfselect import SelfSelect,db
from model.stock import  Stock
from datetime import datetime,timedelta
from model.industry import Industry
from model.analysis_result import AnalysisResult
from model.news import News
import tushare as ts
import pandas as pd

ts.set_token('b7378a5c379a258bd7f96c9d3c411d6484b82d0ff3ce312f720abc9c')
pro = ts.pro_api()

class SelfSelectService:

    @staticmethod
    def add_self_select(userid, stockid):
        try:
            # 假设 new_selfselect 是一个自选股模型实例
            new_selfselect = SelfSelect(userid=userid, stockid=stockid)
            db.session.add(new_selfselect)
            db.session.commit()
            return {"success": True, "message": "股票已添加到自选股"}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"自选股添加失败: {str(e)}"}


    def get_user_self_selects(self,userid):
        try:
            # 查询用户自选股
            selfselects = SelfSelect.query.filter_by(userid=userid).limit(5).all()
            stock_list = []
            df = ts.realtime_list(src='dc')
            for select in selfselects:
                stocks_item = {
                    "userid": userid
                }

                if select.stockid:
                    stock = Stock.query.get(select.stockid)
                    stocks_item["stockid"]=stock.stockid if stock else None
                    stocks_item["stockname"] = stock.stockname if stock else None
                    stocks_item["stockcode"] = stock.stockcode if stock else None
                    matching_row = df[df['TS_CODE'] == stock.stockcode]
                    if not matching_row.empty:
                        stocks_item["volume"] = matching_row['VOLUME'].iloc[0]    # 成交量(单位：手)
                        stocks_item["close"] = matching_row['CLOSE'].iloc[0]    #收盘价
                        stocks_item["pct_change"]=matching_row['PCT_CHANGE'].iloc[0]  # 涨跌幅
                        stocks_item['5min']=matching_row['5MIN'].iloc[0]  # 5分钟涨幅
                        stocks_item["totoal_mv"] = matching_row['TOTAL_MV'].iloc[0]/10000  # 总市值(单位：万元)
                        stocks_item["news"]= self.get_selfstock_news(stock.stockid)
                        """
                        df可选参数（按照上面格式添加就行）：'
                        CHANGE              涨跌额
                        AMOUNT              成交金额
                        SWING               振幅
                        LOW                 今日最低价
                        HIGH                今日最高价
                        OPEN                今日开盘价
                        VOL_RATIO           量比
                        TURNOVER_RATE       换手率
                        PE                  市盈率
                        PB                  市净率
                        FLOAT_MV            流通市值
                        RISE                涨速
                        60DAY               60天涨幅
                        1YEAR               1年涨幅
                        """


                stock_list.append(stocks_item)
            return stock_list  # 返回股票id的列表
        except Exception as e:
            # 记录异常信息
            return {"success": False, "message": str(e)}
    def get_user_self_selects_all(self,userid):
        try:
            # 查询用户自选股
            selfselects = SelfSelect.query.filter_by(userid=userid).all()
            stock_list = []
            df = ts.realtime_list(src='dc')
            for select in selfselects:
                stocks_item = {
                    "userid": userid
                }

                if select.stockid:
                    stock = Stock.query.get(select.stockid)
                    stocks_item["stockid"] = stock.stockid if stock else None
                    stocks_item["stockname"] = stock.stockname if stock else None
                    stocks_item["stockcode"] = stock.stockcode if stock else None
                    matching_row = df[df['TS_CODE'] == stock.stockcode]
                    pd.set_option('display.max_columns', 1000)
                    pd.set_option('display.width', 1000)
                    pd.set_option('display.max_colwidth', 1000)
                    print(matching_row)
                    if not matching_row.empty:
                        stocks_item["volume"] = matching_row['VOLUME'].iloc[0]    # 成交量(单位：手)
                        stocks_item["close"] = matching_row['CLOSE'].iloc[0]    #收盘价
                        stocks_item["pct_change"]=matching_row['PCT_CHANGE'].iloc[0]  # 涨跌幅
                        stocks_item['5min']=matching_row['5MIN'].iloc[0]  # 5分钟涨幅
                        stocks_item["totoal_mv"] = matching_row['TOTAL_MV'].iloc[0]/10000  # 总市值(单位：万元)
                        stocks_item["news"]= self.get_selfstock_news(stock.stockid)
                        """
                        df可选参数（按照上面格式添加就行）：'
                        CHANGE              涨跌额
                        AMOUNT              成交金额
                        SWING               振幅
                        LOW                 今日最低价
                        HIGH                今日最高价
                        OPEN                今日开盘价
                        VOL_RATIO           量比
                        TURNOVER_RATE       换手率
                        PE                  市盈率
                        PB                  市净率
                        FLOAT_MV            流通市值
                        RISE                涨速
                        60DAY               60天涨幅
                        1YEAR               1年涨幅
                        """


                stock_list.append(stocks_item)
            return stock_list  # 返回股票id的列表
        except Exception as e:
            # 记录异常信息
            return {"success": False, "message": str(e)}


    @staticmethod
    def remove_self_select(userid, stockid):
        selfselect = SelfSelect.query.filter_by(userid=userid, stockid=stockid).first()
        if not selfselect:
            return {"success": False, "message": "该股票不在您的自选股中"}

        db.session.delete(selfselect)
        db.session.commit()

        return {"success": True, "message": "股票已从自选股中移除"}


    @staticmethod
    def get_selfselect_news(userid):
        try:
            selfselects = SelfSelect.query.filter_by(userid=userid).all()
            news_list = []
            for select in selfselects:
                if select.stockid:
                    news = News.query.filter_by(stockid=select.stockid).all()
                    for news_news in news:
                        news_item = {}
                        stock = Stock.query.get(news_news.stockid)
                        analysis = AnalysisResult.query.filter_by(news_id=news_news.newsid).all()
                        for analysis_analysis in analysis:
                            news_item["stockname"]=stock.stockname if stock else None
                            news_item["stockcode"]=stock.stockcode if stock else None
                            news_item["title"] = news_news.title if news_news.title else None
                            news_item["url"] = news_news.url if news_news.url else None
                            news_item['date'] = news_news.publishdate if news_news.publishdate else None

                            news_item['trend']=analysis_analysis.trend if analysis_analysis.trend else None
                            news_item['reason']=analysis_analysis.reason if analysis_analysis.reason else None
                            news_item['sentiment']=analysis_analysis.sentiment if analysis_analysis.sentiment else None
                            news_item['sector']=analysis_analysis.sector if analysis_analysis.sector else None
                            news_list.append(news_item)
            return news_list  # 返回股票id的列表
        except Exception as e:
            # 记录异常信息
            return {"success": False, "message": str(e)}



    def get_selfstock_news(self,stockid):
        try:
            news_list = []
            news = News.query.filter_by(stockid=stockid).all()
            for news_news in news:
                news_item = {}
                analysis = AnalysisResult.query.filter_by(news_id=news_news.newsid).all()
                for analysis_analysis in analysis:
                    news_item["title"] = news_news.title if news_news.title else None
                    news_item["url"] = news_news.url if news_news.url else None
                    news_item['date'] = news_news.publishdate if news_news.publishdate else None

                    news_item['trend']=analysis_analysis.trend if analysis_analysis.trend else None
                    news_item['reason']=analysis_analysis.reason if analysis_analysis.reason else None
                    news_item['sentiment']=analysis_analysis.sentiment if analysis_analysis.sentiment else None
                    news_item['sector']=analysis_analysis.sector if analysis_analysis.sector else None
                    news_list.append(news_item)
            return news_list  # 返回股票id的列表
        except Exception as e:
            # 记录异常信息
            return {"success": False, "message": str(e)}

