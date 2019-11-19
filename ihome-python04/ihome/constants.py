"""
@Time    : 2019/11/18 下午5:50
@Author  : chenhui
@FileName: constants.py
@Software: PyCharm
"""
# 设置常量

# 七牛云域名
QINIU_URL_DOMAIN = 'XXXX'

# 城区信息的缓存时间，单位: 秒
AREA_INFO_REDIS_CACHE_EXPIRES = 7200

# 首页展示最多的房屋数量
HOME_PAGE_MAX_HOUSES = 5

# 首页房屋数据的redis缓存时间，单位：秒
HOME_PAGE_DATA_REDIS_EXPIRES = 7200

# 房屋详情页展示的评论最大数
HOUSE_DETAIL_COMMENT_DISPLAY_COUNTS = 30

# 房屋详情页面数据redis缓存时间，单位：秒
HOUSE_DETAIL_REDIS_EXPIRE_SECOND = 7200

