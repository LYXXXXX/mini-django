from django.db import models
from utils.BaseModel import BaseModel
# Create your models here.


# 用户表
class UserWX(BaseModel):
    name = models.CharField(max_length=30, null=True, verbose_name='姓名')
    nickname = models.CharField(max_length=30, null=True, verbose_name='昵称')
    avatar = models.URLField(max_length=100, verbose_name='头像')
    wx_account = models.CharField(max_length=60, null=True, unique=True, verbose_name='微信号')
    openid = models.CharField(max_length=60, null=False, unique=True, verbose_name='微信唯一标志')
    age = models.IntegerField(default='18', verbose_name='年龄')
    sex = models.BooleanField(default=True, verbose_name='性别')
    country = models.CharField(max_length=30, default='中国', verbose_name='国家')
    province = models.CharField(max_length=30, default='北京', verbose_name='省份/直辖市')
    city = models.CharField(max_length=30, default='北京', verbose_name='城市')
    county = models.CharField(max_length=30, default='东城区', verbose_name='区/县')

    class Meta:
        db_table = 'tb_user_wx'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


# 兴趣爱好表
class Hobby(BaseModel):
    hobby = models.CharField(max_length=30, verbose_name='兴趣爱好')

    class Meta:
        db_table = 'tb_hobby'
        verbose_name = '兴趣爱好表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.hobby


# 用户和兴趣爱好的中间表
class User2Hobby(BaseModel):
    user = models.ForeignKey(UserWX, on_delete=models.CASCADE, verbose_name='用户ID')
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE, verbose_name='爱好ID')

    class Meta:
        db_table = 'tb_user2hobby'
        verbose_name = '用户兴趣中间表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.hobby_id


class Word(BaseModel):
    content = models.CharField(max_length=360, default='这个人很懒，什么也没写', null=True, blank=True, verbose_name='个性签名')
    user = models.OneToOneField(UserWX, on_delete=models.CASCADE, unique=True, verbose_name='用户id')

    class Meta:
        db_table = 'tb_word'
        verbose_name = '个性签名表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


class Match(BaseModel):
    user = models.ForeignKey(UserWX, on_delete=models.CASCADE, verbose_name='用户ID')
    target_id = models.IntegerField(verbose_name='目标ID')
    relationship = models.BooleanField(null=True, default="", verbose_name='匹配关系')
    attention = models.BooleanField(default=False, verbose_name='关注')

    class Meta:
        db_table = 'tb_match'
        unique_together = ('user', 'target_id')
        verbose_name = '用户关系表'
        verbose_name_plural = verbose_name

    def __str__(self):
        s = '目标id:' + str(self.target_id) + '匹配结果:' + str(self.relationship) + '关注：' + str(self.attention)
        print(s)
        return str(self.target_id)