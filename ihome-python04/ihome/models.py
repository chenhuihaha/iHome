"""
@Time    : 2019/11/8 下午7:44
@Author  : chenhui
@FileName: models.py
@Software: PyCharm
"""
from ihome import constants
from datetime import datetime
import time
#    flask的密码加密模块              密码生成函数           密码验证函数
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""

    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录更新时间


class User(BaseModel, db.Model):
    """用户"""

    __tablename__ = 'ih_user_profile'

    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    name = db.Column(db.String(32), unique=True, nullable=False)  # 用户昵称
    password_hash = db.Column(db.String(128), nullable=False)  # 加密的密码
    mobile = db.Column(db.String(11), unique=True, nullable=False)  # 手机号
    real_name = db.Column(db.String(32))  # 真是姓名
    id_card = db.Column(db.String(20))  # 身份证号
    avatar_url = db.Column(db.String(128))  # 用户头像路径
    houses = db.relationship('House', backref='user')  # 用户发布的房量
    orders = db.relationship('Order', backref='user')  # 用户下的订单

    @property
    def password(self):
        """获取password属性时被调用"""
        # 报错
        raise AttributeError('不可读')

    @password.setter
    def password(self, passwd):
        """设置password属性时被调用,设置密码加密"""
        self.password_hash = generate_password_hash(passwd)

    def check_password(self, passwod):
        """检验密码的正确性"""
        return check_password_hash(self.password_hash, passwod)

    def to_dict(self):
        """将对象转换为字典数据"""
        auth_dict = {
            'user_id': self.id,
            'real_name': self.real_name,
            'id_card': self.id_card
        }
        return auth_dict


class Area(BaseModel, db.Model):
    """城区信息"""

    __tablename__ = 'ih_area_info'
    id = db.Column(db.Integer, primary_key=True)  # 城区编号
    name = db.Column(db.String(32), nullable=False)  # 区域名字
    houses = db.relationship('House', backref='area')  # 区域的房屋

    def to_dict(self):
        """将对象转换为字典数据"""
        area_dict = {
            'aid': self.id,
            'aname': self.name
        }
        return area_dict


# 房屋设施表，建立房屋与设施的多对多关系
house_facility = db.Table(
    'ih_house_facility',
    db.Column('house_id', db.Integer, db.ForeignKey('ih_house_info.id'), primary_key=True),
    db.Column('facility_id', db.Integer, db.ForeignKey('ih_facility_info.id'), primary_key=True)
)


class Houses(BaseModel, db.Model):
    """房屋信息"""

    __tablename__ = 'ih_house_info'
    id = db.Column(db.Integer, primary_key=True)  # 房屋编号
    user_id = db.Column(db.Integer, db.ForeignKey('ih_user_profile.id'), nullable=False)  # 房屋主人，一对一
    area_id = db.Column(db.Integer, db.ForeignKey('ih_area_info.id'), nullable=False)  # 归属地的区域
    title = db.Column(db.String(64), nullable=False)  # 标题
    price = db.Column(db.Integer, default=0)  # 单价，单位：分
    address = db.Column(db.String(512), default='')  # 地址
    room_count = db.Column(db.Integer, default=1)  # 房间数量
    acreage = db.Column(db.Integer, default=0)  # 房间面积
    unit = db.Column(db.String(32), default='')  # 房间单元，如几室几厅
    capacity = db.Column(db.Integer, default=1)  # 房屋容纳人数
    beds = db.Column(db.String(64), default='')  # 房屋床铺的配置
    deposit = db.Column(db.Integer, default=0)  # 房屋押金
    min_days = db.Column(db.Integer, default=1)  # 最小入住天数
    max_days = db.Column(db.Integer, default=0)  # 最多入住天数，0表示不限制
    order_count = db.Column(db.Integer, default=0)  # 预定完成的该房屋的订单数
    index_image_url = db.Column(db.String(256), default='')  # 房屋主图片的路劲
    facilities = db.relationship("Facility", secondary=house_facility)  # 房屋设施
    images = db.relationship('HouseImage')  # 房屋图片
    orders = db.relationship('Order', backref='house')  # 房屋订单

    def to_basic_dict(self):
        """将基本信息转换为字典数据"""
        house_dict = {
            'house_id': self.id,
            'title': self.title,
            'price': self.price,
            'area_name': self.area.name,
            'img_url': constants.QINIU_DOMIN_PREFIX + self.index_image_url if self.index_image_url else None,
            'room_count': self.room_count,
            'order_count': self.order_count,
            'addres': self.address,
            'user_avatar': constants.QINIU_DOMIN_PREFIX + self.user.avatar_url if self.user.avatar_url else None,
            'ctime': self.create_time.strftime('%Y-%m-%d')
        }

        return house_dict


class Facility(db.Model):
    """设施信息"""
    __tablename__ = 'ih_facility_info'
    id = db.Column(db.Integer, primary_key=True)  # 设施编号
    name = db.Column(db.String(32), nullable=False)  # 设施名字


class HouseImage(BaseModel, db.Model):
    """房屋图片"""

    __tablename__ = 'ih_house_image'

    id = db.Column(db.Integer, primary_key=True)  # 订单编号
    house_id = db.Column(db.Integer, db.ForeignKey('ih_user_profile.id'), nullable=False)  # 房屋编号
    url = db.Column(db.String(256), nullable=False)  # 图片路径


class Order(BaseModel, db.Model):
    """订单"""

    __tablename__ = 'ih_order_info'

    id = db.Column(db.Integer, primary_key=True)  # 订单编号
    user_id = db.Column(db.Integer, db.ForeignKey('ih_user_profile.id'), nullable=False)  # 下订单的用户id
    house_id = db.Column(db.Integer, db.ForeignKey('ih_house_info.id'))  # 预定的房间id
    begin_date = db.Column(db.DateTime, nullable=False)  # 预定的起始时间
    end_date = db.Column(db.DateTime, nullable=False)  # 预定的结束时间
    days = db.Column(db.Integer, nullable=False)  # 预定的总天数
    house_price = db.Column(db.Integer, nullable=False)  # 房屋的单价
    amount = db.Column(db.Integer, nullable=False)  # 订单的总金额
    status = db.Column(  # 订单的状态
        db.Enum(
            'WAIT_ACCEPT',  # 待接单
            'WAIT_PAYMENT',  # 待支付
            'PAID',  # 已支付
            'WAIT_COMMENT',  # 待评价
            'COMPLETE',  # 已完成
            'CANCELED',  # 已取消
            'REJECTED'  # 已拒单
        ),
        default='WAIT_ACCEPT', index=True)
    comment = db.Column(db.Text)  # 订单的评论消息或者拒单的原因
    trade_no = db.Column(db.String(128))  # 支付交易编号

    def to_dict(self):
        """将订单信息转换为字典数据"""
        order_dict = {
            'order_id':self.id,
            'title': self.house.title
            'img_url': constants.QINIU_DOMIN_PREFIX + self.index_image_url if self.index_image_url else None,
            'start_date':self.begin_date.strftime('%Y-%m-%d'),
            'end_date':self.end_date.strftime('%Y-%m-%d'),
            'ctime':self.create_time.trftime('%Y-%m-%d'),
            'days':self.days,
            'amount':self.amount,
            'status':self.status,
            'comment':self.comment if self.comment else ''
        }
        return order_dict