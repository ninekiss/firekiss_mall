from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.core.cache import cache
from django.core.paginator import Paginator
from goods.models import GoodsSKU, GoodsType, BlockGoodsType, IndexSaleActive, IndexGoods, IndexBrand
from order.models import GoodsAppraisal, OrderGoods
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
                main_goods = IndexGoods.objects.filter(block_type=mb).order_by('-index')[:8]
                mb.m_goods = main_goods

            # 猜你喜欢区域商品(获取100条)
            ulikes = IndexGoods.objects.filter(block_type=13).order_by('-index')[:100]

            # banner区域(获取6条)
            banners = IndexSaleActive.objects.filter(display=4).order_by('-index')[:6]

            # 品牌墙(获取29条)
            brand_wall = IndexBrand.objects.all().order_by('-index')[:29]

            # 三个广告位(获取3条)
            ads = IndexSaleActive.objects.filter(display=1).order_by('-index')[:3]

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


class Detail(View):
    """商品详情"""
    def get(self, request, goods_id):
        """显示详情页"""
        # 查询数据
        try:
            # 商品sku
            goods = GoodsSKU.objects.get(id=goods_id)
        except GoodsSKU.DoesNotExist:
            return redirect(reverse('goods:index'))

        # 宝贝排行榜(每个店铺不同)
        # 根据销量
        goods_ranking_by_sales = GoodsSKU.objects.filter(brand=goods.brand).exclude(id=goods_id).order_by('-sales')[:5]
        # 根据评价
        goods_ranking_by_comments = GoodsSKU.objects.filter(brand=goods.brand).exclude(id=goods_id).order_by('-comments')[:5]

        # 看了又看(最新的商品)
        look = GoodsSKU.objects.filter(brand=goods.brand).exclude(id=goods_id).order_by('-id')[:5]

        # 人气((销量+评价)*500
        popular = (goods.sales+goods.comments+10)*500

        # 所有评价数
        appr_count = GoodsAppraisal.objects.filter(goods__sku=goods).exclude(appr_status__in=(3, 4))

        # 追评数
        appr_add_count = appr_count.filter(appr_status=2).count()

        appr_count = appr_count.count()

        apprs = []

        # 属于同一个订单商品的评论
        # 先把所有订单查出来
        orders = OrderGoods.objects.filter(sku=goods)
        # 查询每个订单对应的评价
        for order in orders:

            appr = GoodsAppraisal.objects.filter(goods=order)

            # 初次评价
            appr.first = appr.filter(appr_status=1)

            # 追评
            appr.add = appr.filter(appr_status=2)
            if appr.add:
                # 有追评
                appr.has_add = True
            else:
                appr.has_add = False

            # 解释(初评解释)
            appr.expo_first = appr.filter(appr_status=3)

            # 解释(追评解释)
            appr.expo_add = appr.filter(appr_status=4)

            # 有图评价
            appr.has_pic = True
            apprs.append(appr)

        # 组织模板上下文
        content = {
            'goods': goods,
            'ranking_by_sales': goods_ranking_by_sales,
            'ranking_by_comments': goods_ranking_by_comments,
            'look': look,
            'popular': popular,
            'appr_count': appr_count,
            'appr_add_count': appr_add_count,
            'apprs': apprs
        }
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

            # 添加用户历史浏览记录
            con = get_redis_connection("default")
            history_key = 'history_%d' % user.id
            # 移除列表中的goods_id
            con.lrem(history_key, 0, goods_id)
            # 把goods_id插入到列表最左侧
            con.lpush(history_key, goods_id)
            # 只保存用户最近5条的历史浏览记录
            con.ltrim(history_key, 0, 4)

            # 获取用户历史浏览记录
            hist_ids = con.lrange(history_key, 0, 4)  # 获取最新的5条
            goods_list = []
            for hist_id in hist_ids:
                goods = GoodsSKU.objects.get(id=hist_id)
                goods_list.append(goods)

        content.update(cart_count=cart_count)
        content.update(goods_list=goods_list)
        # 返回数据
        return render(request, 'goods_detail.html', content)


# list/type_id/page?sort=排序方式
class List(View):
    """列表页"""
    def get(self, request, type_id, page):
        """显示列表页"""
        # 查询数据
        # 获取种类信息
        try:
            type = GoodsType.objects.get(id=type_id)
        except GoodsType.DoesNotExist:
            return redirect(reverse('goods:index'))

        # 获取排序方式
        sort = request.GET.get('sort')

        # 获取种类id对应的商品,并进行排序
        if sort == 'hot':
            # 人气
            skus = GoodsSKU.objects.filter(type=type).order_by('-comments')
        elif sort == 'new':
            # 新品
            skus = GoodsSKU.objects.filter(type=type).order_by('-id')
        elif sort == 'sales':
            # 销量
            skus = GoodsSKU.objects.filter(type=type).order_by('-sales')
        elif sort == 'price':
            # 价格
            skus = GoodsSKU.objects.filter(type=type).order_by('-real_price')
        else:
            # 默认
            sort = 'default'
            skus = GoodsSKU.objects.filter(type=type)

        # 对数据进行分页
        paginator = Paginator(skus, 1)


        # 总页数
        nums_pages = paginator.num_pages



        # 获取第page页的数据
        try:
            page = int(page)
        except Exception as e:
            page = 1

        # 大于总页数
        if page > nums_pages:
            page = 1

        # 获取第page页的实例对象
        skus_page = paginator.page(page)

        # 页码范围自定义
        # 总页数小于8页,显示所有页码
        if nums_pages <= 8:
            if page <= 6:
                # 1.当前页小于等于6，全部显示在省略号左边
                pages_left = range(1, nums_pages+1)
                pages_right = []
            else:
                # 2.当前页大于6, 省略号前面固定显示1，2页,省略号后面固定显示当前页前3页，当前页，当前页后两页
                pages_left = [1, 2]
                pages_right = range(nums_pages-4, nums_pages+1)

        else:
            pages_left = [1, 2]
            pages_right = range(page-2, page+3)

        # 组织模板上下文
        content = {
            'type': type,
            'skus_page': skus_page,
            'sort': sort,
            'pages_left': pages_left,
            'pages_right': pages_right
        }

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

            # 获取用户历史浏览记录
            con = get_redis_connection("default")
            history_key = 'history_%d' % user.id

            hist_ids = con.lrange(history_key, 0, 4)  # 获取最新的5条

            goods_list = []
            for hist_id in hist_ids:
                goods = GoodsSKU.objects.get(id=hist_id)
                goods_list.append(goods)

        content.update(cart_count=cart_count)
        content.update(goods_list=goods_list)

        # 返回数据
        return render(request, 'goods_list.html', content)
