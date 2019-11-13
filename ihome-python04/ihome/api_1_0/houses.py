"""
@Time    : 2019/11/13 上午10:09
@Author  : chenhui
@FileName: houses.py
@Software: PyCharm
"""

from ..models import House, Facility
from flask import jsonify, session, request


@api.route('/house/info', methods=['POST'])
@login_required
def save_house_info():
    """保存房屋的基本信息"""
    # 获取数据
    house_data = request.get_json()

    title = house_data.get('title')
    price = house_data.get('price')
    area_id = house_data.get('area_id')
    address = house_data.get('address')
    room_count = house_data.get('room_count')
    acreage = house_data.get('acreage')
    unit = house_data.get('unit')
    capacity = house_data.get('capacity')
    beds = house_data.get('beds')
    deposit = house_data.get('deposit')
    min_das = house_data.get('min_das')
    max_days = house_data.get('max_days')

    # 校验参数
    if not all([title, price, area_id, address, room_count, acreage, unit, capacity, beds, deposit, min_das, max_days]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')  # jsonify: 字典转换成json字符串

    # 判断金额是否正确
    try:
        price = int(float(price) * 100)
        deposit = int(float(deposit) * 100)
    except Exception as e:
        current_app.logger.error(e)  # 保存错误信息日志
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 判断城区id是否存在
    try:
        area = Area.query.get(area_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='参数异常')
    if area is None:
        return jsonify(errno=RET.NODATA, errmsg='城区信息有误')

    # 保存房屋信息
    house = House(
        user_id=user_id,
        area_id=area_id,
        title=title,
        price=price,
        address=address,
        room_count=room_count,
        acreage=acreage,
        unit=unit,
        capacity=capacity,
        beds=beds,
        deposit=deposit,
        min_das=min_das,
        max_days=max_days
    )

    # 处理房屋的设施信息
    facility_ids = house_data.get('facility')

    # 如果用户勾选了设施信息，进行保存
    if facility_ids:
        try:
            facilities = Facility.query.filter(Facility.id.in_(facility_ids)).all()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='数据库异常')

        if facilities:
            # 表示有合法的设施数据
            # 保存设施数据
            house.facilities = facilities
    try:
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()  # 回滚
        return jsonify(errno=RET.DBERR, errmsg='保存数据失败')

    # 保存数据成功
    return jsonify(errno=RET.OK, errmsg='OK', data={'house_id': house.id})

def save_house_image():
    """保存房屋的图片
    参数 图片 房屋的id
    """
    image_file = request.files.get('house_image')
    house_id = request.form.get('house_id')

    if not all([image_file,house_id]):
        return jsonify(errno=RET,PARAMERR,errmsg='参数错误')

    # 判断house_id正确性
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='数据库异常')
    if house is None:
        return jsonify(errno=RET.NODATA,errmsg='房屋不存在')
    image_data = image_file.read()
    # 保存图片到七牛云中
    try:
        file_name = storage(image_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR,errmsg='保存图片失败')

    # 保存图片信息到数据库中
    house_image = Houseimage(house_id=house_id,url=file_name)
    db.session.add(house_image)

    # 处理房屋的主图片
    if not house.index_image_url:
        house.index_image_url = file_name
        db.session.add(house)

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR,errmsg='保存图片数据异常')

    image_url = constants.QINIU_URL_DOMAIN + file_name

    return jsonify(errno=RET.OK,errmsg='OK',data={'image_url':image_url})