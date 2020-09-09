import json
from . import models
from image_upload.models import UploadImage
from django.views import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from utils.res_code import Code, to_json_data, error_map
from utils import CONSTANT

# Create your views here.
import logging

loggers = logging.getLogger('mini')


# 获取动态内容
class GetNewsView(View):
    def get(self, request):
        try:
            page = int(request.GET.get('page', 1))
        except Exception as e:
            loggers.error('获取参数失败：', e)
            print('页码错误')
            page = 1

        news = models.News.objects.values('id', 'text', 'user_id', 'love_num',
                                          'comment_num', 'create_time', 'user__nickname',
                                          'user__avatar').filter(is_delete=False).all()

        page_info = Paginator(news, 10)

        try:
            info = page_info.page(page)
        except Exception as e:
            loggers.info('给定的页码错误：{}'.format(e))
            info = page_info.page(page_info.num_pages)

        # 添加图片URL
        info = list(info)
        for i in info:
            imgList = []
            img = models.UploadImage.objects.filter(imagefromnews__news_id=i['id'])
            if img:
                for j in img:
                    url = j.get_image_url()
                    imgList.append(url)
            i['imgList'] = imgList

        # 包装data
        data = {
            'news': info
        }
        return to_json_data(errno=Code.OK, errmsg=error_map[Code.OK], data=data)


# 创建动态内容
class CreateNewsView(View):
    pass
