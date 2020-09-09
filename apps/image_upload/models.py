from django.db import models
from utils.BaseModel import BaseModel
from user_wx.models import UserWX
from utils import CONSTANT


# Create your models here.


class UploadImage(BaseModel):
    filename = models.CharField(max_length=252, default="", verbose_name='图片文件名')
    file_md5 = models.CharField(max_length=128, verbose_name='图片MD5')
    file_type = models.CharField(max_length=32, verbose_name='图片类型')
    file_size = models.IntegerField(verbose_name='图片大小')
    # 置顶为True 表示匹配页面用的展示图片
    is_top = models.BooleanField(default=False, verbose_name='置顶')
    user = models.ForeignKey(UserWX, on_delete=models.CASCADE, verbose_name='用户ID')

    @classmethod
    def get_image_by_md5(cls, md5):
        # 根据md5值获取图片的模型对象   这是一个类方法
        try:
            return UploadImage.objects.filter(file_md5=md5, is_delete=False).first()
        except Exception as e:
            return None

    # 获取本图片的url,我们可以通过这个url在浏览器访问到这个图片
    # 其中WEB_HOST_NAME 是常量配置，指服务器的域名
    # WEB_IMAGE_SERVER_PATH 是常量配置，指静态图片资源访问路径
    # 这些配置在 常量配置文件 utils/CONSTANT.py 中设置

    def get_image_url(self):
        filename = self.file_md5 + '.' + self.file_type
        url = CONSTANT.WEB_HOST_NAME + CONSTANT.WEB_IMAGE_SERVER_PATH + str(self.user_id) + '/' + filename
        return url

    # 获取本图片在本地的位置，即你的文件系统的路径，图片会保存在这个路径下
    def get_image_path(self):
        filename = self.file_md5 + '.' + self.file_type
        path = CONSTANT.WEB_IMAGE_SERVER_PATH + str(self.user_id) + '/' + filename
        return path

    class Meta:
        db_table = 'tb_image'
        ordering = ['id']
        verbose_name = '用户图片表'
        verbose_name_plural = verbose_name

    def __str__(self):
        s = 'filename:' + str(self.filename) + '-' + 'filetype:' + str(self.file_type) + '-' + 'filesize:' + str(
            self.file_size) + '-' + 'filemd5:' + str(self.file_md5)
        return s


class Image(models.Model):
    url = models.URLField(max_length=60)

    class Meta:
        db_table = 'image_test'
        ordering = ['id']

    def __str__(self):
        return self.url
