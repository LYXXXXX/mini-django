from django.db import models

class BaseModel(models.Model):
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    # 逻辑删除
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        # 指明为抽象类，迁移时不会创建表
        abstract = True