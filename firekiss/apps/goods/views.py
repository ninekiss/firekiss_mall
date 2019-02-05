from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.core.cache import cache
from goods.models import GoodsSKU, GoodsType, BlockGoodsType, IndexSaleActive, IndexGoods, IndexBrand
from django_redis import get_redis_connection


# Create your views here.


class Index(View):
    def get(self, request):
        # 试着从缓存中获取数据
        content = cache.get('index_page_data')

        if content is None:
            # 缓存中没有数据

            # 查询数据
            qs = BlockGoodsType.objects.all()

            # 品牌推广区块
            brand_popularize = qs.filter(id=1)
            bps = qs.filter(father_type=brand_popularize)

            # 商品主块
            main_block = qs.filter(id=5)
            mbs = qs.filter(father_type=main_block)

            for mb in mbs:
                # 商品主块文字链接
                main_link = qs.filter(father_type=mb).order_by('-index')
                mb.m_links = main_link
                # 商品主块商品(获取8条)
                main_goods = IndexGoods.objects.filter(block_type=mb).order_by('-index')[0:8]
                mb.m_goods = main_goods

            # 猜你喜欢区域商品(获取100条)
            ulikes = IndexGoods.objects.filter(block_type=13).order_by('-index')[0:100]

            # banner区域(获取6条)
            banners = IndexSaleActive.objects.filter(display=4).order_by('-index')[0:6]

            # 品牌墙(获取29条)
            brand_wall = IndexBrand.objects.all().order_by('-index')[0:29]

            # 三个广告位(获取3条)
            ads = IndexSaleActive.objects.filter(display=1).order_by('-index')[0:3]

            # 组织模板上下文
            content = {
                'bps': bps,
                'mbs': mbs,
                'banners': banners,
                'brand_wall': brand_wall,
                'ads': ads,
                'ulikes': ulikes
            }

            # 设置缓存
            cache.set('index_page_data', content, 3600)

        # 购物车商品数量
        cart_count = 0
        user = request.user
        if user.is_authenticated():
            # 如果用户已登录,获取用户购物车商品数量(使用redis)
            # key: cart_用户id
            # field: 商品id
            # value: 某个商品的数量

            con = get_redis_connection("default")
            cart_key = 'cart_user%d' % user.id
            cart_count = con.hlen(cart_key)

        content.update(cart_count=cart_count)
        # 返回数据
        return render(request, 'index.html', content)


