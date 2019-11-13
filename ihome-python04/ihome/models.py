"""
@Time    : 2019/11/8 下午7:44
@Author  : chenhui
@FileName: models.py
@Software: PyCharm
"""
from ihome import db


class House():
    """房屋信息"""

    __tablename__ = 'ih_house_info'
    id = db.Column(db.Integer, primary_key=True)  #房屋编号
    user_id = db.Column(db.Integer, db.ForeignKey('ih_user_profile.id'), nullable=False) # 房屋主人，一对一
    area_id = db.Column(db.Integer, db.ForeignKey('ih_area_info.id'), nullable=False) # 归属地的区域
    title = db.Column(db.String(64), nullable=False)  #标题
    price = db.Column(db.Integer, default=0) # 单价，单位：分
    address = db.Column(db.String(512), default='') # 地址
    room_count = db.Column(db.Integer, default=1) #房间数量
    acreage = db.Column(db.Integer, default=0) # 房间面积
    unit = db.Column(db.String(32), default='') # 房间单元，如几室几厅
    capacity = db.Column(db.Integer, default=1) # 房屋容纳人数
    beds = db.Column(db.String(64), default='') # 房屋床铺的配置
    deposit = db.Column(db.Integer, default=0) # 房屋押金
    min_days = db.Column(db.Integer, default=1) #最小入住天数
    max_days = db.Column(db.Integer, default=0) # 最多入住天数，0表示不限制
    order_count = db.Column(db.Integer, default=0) # 预定完成的该房屋的订单数
    index_image_url = db.Column(db.String(256), default='') # 房屋主图片的路劲
    facilities = db.relationship("Facility", secondary=house_facility) # 房屋设施
    images = db.relationship('HouseImage') # 房屋图片
    orders = db.relationship('Order', backref='house') # 房屋订单


class Facility(db.Model):
    """设施信息"""
    __tablename__ = 'ih_facility_info'
    id = db.Column(db.Integer,primary_key=True) # 设施编号
    name = db.Column(db.String(32),nullable=False) #设施名字