from django.contrib import admin
from celery_task.tasks import get_static_index_html


class BaseAdmin(admin.ModelAdmin):
    """模型管理器基类"""
    def save_model(self, request, obj, form, change):
        """admin后台修改或更新数据时调用"""
        super().save_model(request, obj, form, change)
        get_static_index_html.delay()

    def delete_model(self, request, obj):
        """admin后台删除数据时调用"""
        super().delete_model(request, obj)
        get_static_index_html.delay()
