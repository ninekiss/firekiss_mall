from django.contrib import admin
from goods.models import GoodsSKU, Goods, GoodsImage, GoodsProperty, GoodsType, GoodsBrand, IndexSaleActive, IndexBrand, \
BlockGoodsType, IndexGoods


class GoodsAdmin(admin.ModelAdmin):
    """商品种类模型管理器类"""
    list_display = ('id', 'name')


class GoodsSKUAdmin(admin.ModelAdmin):
    """商品种类模型管理器类"""
    # list_display = ('id', 'type', 'icon')
    pass

class GoodsTypeAdmin(admin.ModelAdmin):
    """商品种类模型管理器类"""
    list_display = ('id', 'type', 'icon')


class IndexSaleActiveAdmin(admin.ModelAdmin):
    """商品种类模型管理器类"""
    list_display = ('id', 'name', 'image', 'url', 'display', 'index')


class BlockGoodsTypeAdmin(admin.ModelAdmin):
    """首页大块商品分类模型管理器类"""
    list_display = ('id', 'name', 'en_name', 'image', 'style', 'url', 'father_type', 'index')


class IndexGoodsAdmin(admin.ModelAdmin):
    """首页商品模型类管理器类"""
    list_display = ('id', 'sku', 'block_type', 'index')


# Register your models here.
admin.site.register(Goods, GoodsAdmin)
admin.site.register(GoodsSKU, GoodsSKUAdmin)
admin.site.register(GoodsType, GoodsTypeAdmin)
admin.site.register(GoodsBrand)
admin.site.register(IndexSaleActive, IndexSaleActiveAdmin)
admin.site.register(IndexBrand)
admin.site.register(BlockGoodsType, BlockGoodsTypeAdmin)
admin.site.register(IndexGoods, IndexGoodsAdmin)


