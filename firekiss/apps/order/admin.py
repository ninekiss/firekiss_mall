from django.contrib import admin
from order.models import OrderInfo, OrderGoods, GoodsAppraisal

# Register your models here.


class GoodsAppraisalAdmin(admin.ModelAdmin):
    """商品种类模型管理器类"""
    list_display = ('id', 'goods')


admin.site.register(OrderInfo)
admin.site.register(OrderGoods)
admin.site.register(GoodsAppraisal, GoodsAppraisalAdmin)
