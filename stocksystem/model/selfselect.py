from model.__init__ import db

class SelfSelect(db.Model):
    __tablename__ = 'selfselect'
    __table_args__ = {'extend_existing': True}
    # 组合主键，确保每个用户只能选择每只股票一次
    stockid = db.Column(db.Integer, primary_key=True)  # 外键，关联股票表
    userid = db.Column(db.Integer, primary_key=True)    # 外键，关联用户表


    def __repr__(self,userid, stockid):
        self.userid = userid
        self.stockid = stockid
