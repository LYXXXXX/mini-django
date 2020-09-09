import json
from utils.res_code import Code, to_json_data, error_map
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from . import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from utils import CONSTANT
import filetype
import hashlib
import logging
loggers = logging.getLogger('mini')


# 上传文件的视图
class UploadImageView(View):
    def post(self, request):
        #   从请求表单中获取文件对象
        json_data = request.body
        if not json_data:
            return to_json_data(errno=Code.NODATA, errmsg=error_map[Code.NODATA])
        param = json.loads(request.POST.get('Param'))
        is_top = param['top']
        file = request.FILES.get('img', None)
        user_id = param['id']

        if not file:  # 文件对象不存在, 返回400请求错误
            return to_json_data(errno=Code.NODATA, errmsg="no file.")

        # 图片大小限制
        if not pIsAllowedFileSize(file.size):
            return to_json_data(errno=Code.DATAERR, errmsg="文件太大")

        # 计算文件的md5
        md5 = pCalculateMd5(file)
        uploadImg = models.UploadImage.get_image_by_md5(md5)
        if uploadImg:   # 图片文件已存在,直接返回
            return to_json_data(errno=Code.DATAEXIST,
                                errmsg=error_map[Code.DATAEXIST],
                                data={'url': uploadImg.get_image_url()})

        # 获取扩展类型 并判断
        ext = pGetFileExtension(file)
        if not pIsAllowedImageType(ext):
            return to_json_data(errno=Code.DATAERR, errmsg="文件类型错误")

        # 检测通过 创建新的image对象
        uploadImg = models.UploadImage()
        uploadImg.filename = file.name
        uploadImg.file_size = file.size
        uploadImg.file_md5 = md5
        uploadImg.file_type = ext
        uploadImg.is_top = is_top
        uploadImg.user_id = user_id
        uploadImg.save()

        # 保存文件到硬盘
        with open(uploadImg.get_image_path(), 'wb+') as f:
            # 分块写入
            for chunk in file.chunks():
                f.write(chunk)

        # 记录日志
        loggers.info("图片上传成功！[md5:%s  id:%s]" % (md5, uploadImg.id))

        # 返回图片的url
        return to_json_data(errno=Code.OK, errmsg=error_map[Code.OK], data={"url": uploadImg.get_image_url()})


# 获取文件的视图
class GetImage(View):
    def get(self, request):
        try:
            page = int(request.GET.get('page', 1))
        except:
            print('页码错误')
            page = 1

        img_url = models.Image.objects.values('url').order_by('id')

        pagent = Paginator(img_url, 5, orphans=4)

        try:
            info = pagent.page(page)
        except Exception as e:
            print(e)
            info = pagent.page(pagent.num_pages)

        # print(info)

        url_list = list(info)
        print(url_list)
        final_url = []
        for i in url_list:
            final_url.append('http://123.57.242.170:8000/media/image/1/' + i['url'] + '/')

        print(final_url)

        return to_json_data(data=final_url)


# 检测文件类型
# 使用第三方库filetype
def pGetFileExtension(file):
    rawData = bytearray()
    for c in file.chunks():
        rawData += c
    try:
        ext = filetype.guess_extension(rawData)
        return ext
    except Exception as e:
        # todo log
        return None


# 计算文件的md5
def pCalculateMd5(file):
    md5Obj = hashlib.md5()
    for chunk in file.chunks():
        md5Obj.update(chunk)
    return md5Obj.hexdigest()


# 文件类型过滤
def pIsAllowedImageType(ext):
    if ext in ["png", "jpeg", "jpg"]:
        return True
    return False


# 文件大小限制
# settings.IMAGE.SIZE_LIMIT是常量配置，我设置为10M
def pIsAllowedFileSize(size):
    limit = CONSTANT.IMAGE_SIZE_LIMIT
    if size < limit:
        return True
    return False

