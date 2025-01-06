from model.__init__ import db

class News(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'news'

    # 数据库字段定义
    newsid = db.Column(db.Integer, primary_key=True, autoincrement=True)    # 新闻唯一标识
    title = db.Column(db.String(200), nullable=False)                        # 新闻标题
    url = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)  # 新闻内容
    publishdate = db.Column(db.Date)                         # 新闻发布时间
    sourceid = db.Column(db.Integer)  # 外键，关联数据来源
    industryid = db.Column(db.Integer)  # 外键，关联行业
    sentimentid = db.Column(db.Integer)  # 外键，关联情感
    stockid = db.Column(db.String(20))  # 外键，关联股票表

    def __repr__(self, title, url, content=None):
        self.title = title
        self.url = url
        self.content = content
        # self.stockid = stockid
        # self.publishdate = publishdate
        # self.sourceid = sourceid
        # self.sentimentid = sentimentid
        # self.industryid = industryid

