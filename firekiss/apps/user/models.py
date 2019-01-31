from django.db import models
from db.base_model import BaseModel
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(BaseModel, AbstractUser):
    """用户模型类"""
    user_is_vip = (
        (0, '普通用户'),
        (1, '会员'),
        (2, '超级会员')
    )

    tel = models.CharField(max_length=11, verbose_name='手机')
    avatar = models.ImageField(upload_to='user', null=True, verbose_name='头像')
    is_seller = models.BooleanField(default=False, verbose_name='卖家标识')
    is_vip = models.SmallIntegerField(choices=user_is_vip, default=0, verbose_name='身份标识')

    class Meta:
        db_table = 'fk_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class AddressManager(models.Manager):
    """地址模型管理器类"""

    def get_default_addr(self, user):

        try:
            address = self.get(user_id=user, is_default=True)
        except self.model.DoesNotExist:
            address = None
        return address


class Address(BaseModel):
    """地址模型类"""
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='所属账户')
    receiver = models.CharField(max_length=30, verbose_name='收件人')
    addr = models.CharField(max_length=256, verbose_name='详细地址')
    area = models.CharField(max_length=256, verbose_name='所在地区')
    zip_code = models.CharField(max_length=6, null=True, verbose_name='邮编')
    phone = models.CharField(max_length=11, verbose_name='联系方式')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')

    objects = AddressManager()

    class Meta:
        db_table = 'fk_address'
        verbose_name = '地址'
        verbose_name_plural = verbose_name




