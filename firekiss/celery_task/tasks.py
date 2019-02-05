from celery import Celery
from django.core.mail import send_mail
from django.conf import settings
from django.template import loader



# 使用celery

# 在工作者一端，由于未启动django项目，因此需要进行django初始化
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "firekiss.settings")
django.setup()

from goods.models import BlockGoodsType, IndexGoods, IndexSaleActive, IndexBrand

# 启用工作者worker
# 需要拷贝一份项目代码到worker所在的机器上
# 启动指令(所在文件，信息等级)
# celery -A celery_task.tasks worker -l info


# 创建一个Celery对象,并指明中间人(broker)
app = Celery('celery_task.tasks', broker='redis://192.168.0.100:6379/0')


# 定义任务函数，并用celery对象的task方法进行装饰
@app.task
def send_confirm_mail(to_mail, username, token):
    """发送注册激活邮件"""

    subject = '欢迎来到FIREKISS 火吻'  # 主题
    message = ''  # 正文
    sender = settings.EMAIL_FROM  # 发件人
    recceiver = [to_mail]  # 收件人
    # 正文包含html内容
    html_message = '<h1>%s,欢迎来到火吻商城</h1><p>请点击下面的链接完成账户激活,链接在24小时候后失效</p><p><a href="http://192.168.0.100:8000/user/active/%s">http://192.168.0.100:8000/user/active/%s</a></p>' % (
    username, token, token)

    send_mail(subject, message, sender, recceiver, html_message=html_message)


@app.task
def get_static_index_html():
    """生成首页静态页面"""
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

    # 使用模板
    # 1.获取模板对象
    temp = loader.get_template('static_index.html')
    # 2.渲染模板
    static_index_html = temp.render(content)

    # 生成静态首页html文件
    # 1.保存路径
    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')
    # 2.保存文件
    with open(save_path, 'w') as f:
        f.write(static_index_html)