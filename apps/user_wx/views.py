import json
from utils.res_code import Code, to_json_data, error_map
from django.views import View
from . import models
import uuid
import requests
import logging
loggers = logging.getLogger('mini')

wx_appId = 'wx7b217d61ac537dd9'
wx_secret = 'b9c97ec2a9072e35a9a13dbcf204bfa2'


def login(request):
    json_data = request.body
    if not json_data:
        return to_json_data(errno=Code.NODATA, errmsg=error_map[Code.NODATA])
    dict_data = json.loads(json_data)
    print(dict_data)
    code = dict_data['code']
    userInfo = dict_data['userInfo']
    req_result = requests.get('https://api.weixin.qq.com/sns/jscode2session?appid=' + wx_appId +
                              '&secret=' + wx_secret +
                              '&js_code=' + code +
                              '&grant_type=authorization_code')
    userData = req_result.json()
    print(userData)
    user_uuid = str(uuid.uuid4())  # 随机生成字符串user_uuid, 自定义登录态, 暴露给用户的位置标识
    try:
        user = models.UserWX.objects.get(openid=userData['openid'])
        # 如果已经存在的用户 user, 只需要改变他的session_key即可
        user.session_key = userData['session_key']
        # 保存新的用户态
        user.user_uuid = user_uuid
        user.save()
        return to_json_data(errno=Code.OK, errmsg='登录成功', data={'user_uuid': user_uuid})
    # 第一次登录，保存用户的登录信息  openid
    except:
        user = models.UserWX(openid=userData['openid'],
                             session_key=userData['session_key'],
                             user_uuid=user_uuid,
                             nickname=userInfo['nickName'],
                             sex=userInfo['gender'],
                             avatar=userInfo['avatarUrl'],
                             city=userInfo['city'],
                             province=userInfo['province'],
                             country=userInfo['country'])
        user.save()
        res = {
            'user_uuid': user_uuid
        }
        return to_json_data(data=res)
