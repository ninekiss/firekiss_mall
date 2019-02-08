from django.contrib import admin
from django.core.cache import cache
from goods.models import GoodsSKU, Goods, GoodsImage, GoodsProperty, GoodsType, GoodsBrand, IndexSaleActive, IndexBrand, \
BlockGoodsType, IndexGoods


class BaseModelAdmin(admin.ModelAdmin):
    """模型管理器基类"""
    def save_model(self, request, obj, form, change):
        """admin后台添加或更新数据时调用"""
        super().save_model(request, obj, form, change)
        # 不知道为何，这里每个方法都得单独导入tasks
        from celery_task.tasks import get_static_index_html
        get_static_index_html.delay()

        # 添加或修改数据时清除缓存
        cache.delete('index_page_data')

    def delete_model(self, request, obj):
        """admin后台删除数据时调用"""
        super().delete_model(request, obj)
        from celery_task.tasks import get_static_index_html
        get_static_index_html.delay()

        # 数据删除时清除缓存
        cache.delete('index_page_data')


class GoodsAdmin(BaseModelAdmin):
    """商品种类模型管理器类"""
    list_display = ('id', 'name')


class GoodsSKUAdmin(BaseModelAdmin):
    """商品种类模型管理器类"""
    list_display = ('id', 'name', 'brand', 'real_price')


class GoodsTypeAdmin(BaseModelAdmin):
    """商品种类模型管理器类"""
    list_display = ('id', 'type', 'icon')


class IndexSaleActiveAdmin(BaseModelAdmin):
    """商品种类模型管理器类"""
    list_display = ('id', 'name', 'image', 'url', 'display', 'index')


class BlockGoodsTypeAdmin(BaseModelAdmin):
    """首页大块商品分类模型管理器类"""
    list_display = ('id', 'name', 'en_name', 'image', 'style', 'url', 'father_type', 'index')


class IndexGoodsAdmin(BaseModelAdmin):
    """首页商品模型类管理器类"""
    list_display = ('id', 'sku', 'block_type', 'index')


class IndexBrandAdmin(BaseModelAdmin):
    """首页商品模型类管理器类"""
    list_display = ('brand', 'url', 'index')


# Register your models here.
admin.site.register(Goods, GoodsAdmin)
admin.site.register(GoodsSKU, GoodsSKUAdmin)
admin.site.register(GoodsType, GoodsTypeAdmin)
admin.site.register(GoodsBrand)
admin.site.register(IndexSaleActive, IndexSaleActiveAdmin)
admin.site.register(IndexBrand, IndexBrandAdmin)
admin.site.register(BlockGoodsType, BlockGoodsTypeAdmin)
admin.site.register(IndexGoods, IndexGoodsAdmin)


