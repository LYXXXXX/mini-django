from django.db import models
from utils.BaseModel import BaseModel
from user_wx.models import UserWX
from image_upload.models import UploadImage
# Create your models here.


# 动态表
class News(BaseModel):
    text = models.CharField(max_length=500, verbose_name='动态内容')
    user = models.ForeignKey(UserWX, on_delete=models.CASCADE, verbose_name='用户ID')
    love_num = models.IntegerField(verbose_name='点赞数量')
    comment_num = models.IntegerField(verbose_name='评论数量')

    class Meta:
        db_table = 'tb_news'
        verbose_name = '动态表'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']

    def __str__(self):
        return self.id


# 点赞关系表
class LovesFromWho(BaseModel):
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='动态ID')
    user = models.ForeignKey(UserWX, on_delete=models.CASCADE, verbose_name='用户ID')

    class Meta:
        db_table = 'tb_loves_from_who'
        verbose_name = '点赞关系表'
        verbose_name_plural = verbose_name


# 评论表
class Comment(BaseModel):
    PRT_CHOICES = [
        (1, 1),
        (2, 2)
    ]

    text = models.CharField(max_length=500, verbose_name='评论内容')
    level = models.IntegerField(choices=PRT_CHOICES, verbose_name='评论级别')
    user = models.ForeignKey(UserWX, on_delete=models.CASCADE, verbose_name='评论者ID')
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='评论所属动态ID')
    reply_user_id = models.IntegerField(null=True, verbose_name='回复对象ID')

    class Meta:
        db_table = 'tb_comment'
        verbose_name = '评论表'
        verbose_name_plural = verbose_name


# 图片表
class ImageFromNews(BaseModel):
    image = models.ForeignKey(UploadImage, null=True, on_delete=models.SET_NULL, verbose_name='图片ID')
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='动态ID')

    class Meta:
        db_table = 'tb_image_from_news'
        verbose_name = '图片与动态关系表'
        verbose_name_plural = verbose_name
