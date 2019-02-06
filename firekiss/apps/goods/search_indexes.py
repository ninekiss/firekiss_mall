# 创建全文检索类
from haystack import indexes
from goods.models import GoodsSKU


class GoodsSKUIndex(indexes.SearchIndex, indexes.Indexable):
    """sku全文检索类"""

    # use_template=True使用数据模板来构建搜索引擎将索引的文档
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        """返回模型类类名"""
        return GoodsSKU

    def index_queryset(self, using=None):
        """在模型更新时为索引使用"""
        return self.get_model().objects.all()