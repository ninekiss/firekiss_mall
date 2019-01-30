// index page

// banner
function banner() {
    var $slides = $('.list li');
    var $points = $('.point');
    var nowIndex = 0;
    var prevIndex = 0;
    var timer = null;
    var ismove = false;

    $slides.not(':first').css({"left": 1230});


    $points.delegate('li', 'click', function() {
        nowIndex = $(this).index();
        if (nowIndex == prevIndex) {
            return;
        }
        $(this).addClass('active').siblings().removeClass('active');
        move();
    });

    $('.prev').click(function() {
        if (ismove) {
            return;
        }
        ismove = true;
        nowIndex--;
        move();
        $('.point li').eq(nowIndex).addClass('active').siblings().removeClass('active');

    });

    $('.next').click(function() {
        if (ismove) {
            return;
        }
        ismove = true;
        nowIndex++;
        move();
        $('.point li').eq(nowIndex).addClass('active').siblings().removeClass('active');
    });

    timer = setInterval(function() {
        nowIndex++;
        move();
        $('.point li').eq(nowIndex).addClass('active').siblings().removeClass('active');
    },2000);


    $('.slide').hover(function(){
        clearInterval(timer);
    },function() {
        timer = setInterval(function() {
        nowIndex++;
        move();
        $('.point li').eq(nowIndex).addClass('active').siblings().removeClass('active');
        },3000);
    });


    function move() {
        if (nowIndex<0) {
            nowIndex = $slides.length - 1;
            prevIndex = 0;
            $slides.eq(nowIndex).css({"left": -1230});
            $slides.eq(nowIndex).animate({"left": 0},300);
            $slides.eq(prevIndex).animate({"left": 1230}, 300, function() {
                ismove = false;
            });
            prevIndex = nowIndex;
            return;
        }
        if (nowIndex>($slides.length - 1)) {
            nowIndex = 0;
            prevIndex = $slides.length - 1;
            $slides.eq(nowIndex).css({"left": 1230});
            $slides.eq(nowIndex).animate({"left": 0}, 300);
            $slides.eq(prevIndex).animate({"left": -1230}, 300, function() {
                ismove = false;
            });
            prevIndex = nowIndex;
            return;
        }
        if (nowIndex > prevIndex) {
            $slides.eq(nowIndex).css({"left": 1230});
            $slides.eq(nowIndex).animate({"left": 0}, 300);
            $slides.eq(prevIndex).animate({"left": -1230}, 300, function() {
                ismove = false;
            });
            prevIndex = nowIndex;
        }
        else {
            $slides.eq(nowIndex).css({"left": -1230});
            $slides.eq(nowIndex).animate({"left": 0}, 300);
            $slides.eq(prevIndex).animate({"left": 1230}, 300, function() {
                ismove = false;
            });
            prevIndex = nowIndex;
        }

    }

};

// scroll event
function sear_redisplay(params) {
    var $sear = $('.global');
    var $left_nav = $('.left_nav');
    var $now_top = 0;
    var navNowTop = 0;
    var num = 0;
    var timer = null;
    $(window).scroll(function() {

        var $now_top = $(document).scrollTop();

        // 滚动条距顶部距离大于800时，顶部悬停搜索框出现，小于800时，顶部悬停搜索框消失
        if ($now_top >= 800 ) {
            $sear.fadeIn();
        }
        else {
            $sear.fadeOut();
        }
        // 滚动条据顶部距离大于600时，左侧导航栏出现，小于600时，左侧导航栏消失
        if ($now_top >= 800 ) {
            $left_nav.fadeIn();
        }
        else {
            $left_nav.fadeOut();
        }

        // 左侧导航条距离顶部的距离而改变其相对于父元素的top定位值，来实现左侧导航条滚动
        navNowTop = $now_top - 650;
        if (navNowTop < 200) {
            nowIndex = 200;
        }
        $left_nav.css({'top': navNowTop});

        clearTimeout(timer);
        timer = setTimeout(function () {
            // 左侧导航条距离顶部的距离达到一定值时，也就是到某个大类菜单时，对应的导航块变为hover状态
            num = parseInt(($now_top - 1380)/650);
            if (num > 7) {
                num = 7;
            }
            if (num == 0) {
                if ($now_top < 1380) {
                    $('.l_mart').addClass('base');
                }
                else {
                    $('.l_mart').removeClass('base').addClass('clor-ch0').siblings().addClass('base');
                }
            }
            else if (num == 1) {
                $('.l_star').removeClass('base').addClass('clor-ch1').siblings().addClass('base');
            }
            else if (num == 2) {
                $('.l_outdoor').removeClass('base').addClass('clor-ch2').siblings().addClass('base');
            }
            else if (num == 3) {
                $('.l_cool').removeClass('base').addClass('clor-ch3').siblings().addClass('base');
            }
            else if (num == 4) {
                $('.l_beauty').removeClass('base').addClass('clor-ch4').siblings().addClass('base');
            }
            else if (num == 5) {
                $('.l_life').removeClass('base').addClass('clor-ch5').siblings().addClass('base');
            }
            else if (num == 6) {
                $('.l_home').removeClass('base').addClass('clor-ch6').siblings().addClass('base');
            }
            else if (num == 7) {
                $('.l_ulike').removeClass('base').addClass('clor-ch7').siblings().addClass('base');
            }
        });
    });
};

// scrollTop
function nav_jump() {
    var now_tag = 0;
    var next_top = 0;
    $('.top').click(function() {
        $('html, body').animate({"scrollTop": 0});
    });

    $('.r_top').click(function() {
        $('html, body').animate({"scrollTop": 0});
    });

    $('.jump_nav').delegate('a', 'click', function () {
        
        // 回到顶部
        // $('html, body').animate({"scrollTop": 0});
        now_tag = $(this).index();
        if (now_tag < 4) {
            next_top = now_tag*650 + 1390;
        }
        else if (now_tag > 6) {
            next_top = now_tag*650 + 1390 + 3*85;
        }
        else {
            next_top = now_tag*650 + 1390 + (now_tag-3)*85;
        }
        // alert(now_tag);
        $('html, body').animate({"scrollTop": next_top});
    });
};


// goods_detail page 

// reading glass
function glass(pself, shadow, follow, multiple) {
    var self = pself;  // 要放大的元素自身
    var shadow = shadow;  // 放大后的元素
    var follow = follow;  // 元素上的可移动块
    var multiple = multiple;  //放大后的图片与元素中的图片的倍数关系
    var seWidth = self.innerWidth();
    var seHeight = self.innerHeight();
    var foWidth = follow.outerWidth();
    var foHeight = follow.outerHeight();
    var outX = seWidth - foWidth;
    var outY = seHeight - foHeight;
    var nowX = 0;
    var nowY = 0;
    // self 相对document的left偏移值加上它的border-width
    var offX = self.offset().left + parseInt(self.css('border-width'));
    // self 相对document的top偏移值加上它的border-width
    var offY = self.offset().top + parseInt(self.css('border-width'));
    
    self.mouseenter(function() {
        follow.show();
        shadow.show();
        $(document).mousemove(function(event){
            nowX = event.pageX - offX - foWidth/2;
            nowY = event.pageY - offY - foHeight/2;
            swithX = offX + foWidth/2;
            swithY = offY + foHeight/2;
            if (nowX < 0) {
                nowX = 0;
            }
            if (nowX > outX) {
                nowX = outX;
            }
            if (nowY < 0) {
                nowY = 0;
            }
            if (nowY > outY) {
                nowY = outY;
            }
            // X;
            if (event.pageX > swithX) {
                follow.css({"left": nowX});
                shadow.css({"background-position-x": -nowX*multiple});
            }
            else if (event.pageX < swithX) {
                follow.css({"left": 0});
            }
            // Y
            if (event.pageY > swithY) {
                follow.css({"top": nowY});
                shadow.css({"background-position-y": -nowY*multiple});
            }
            else if (event.pageY < swithY) {
                follow.css({"top": 0});
            }
                
        });
    });
    self.mouseleave(function () {
        follow.hide();
        shadow.hide();
    });
};

// other
function detail_con () {
    // 更多优惠
    var $active_sale = $('.active_sale');
    var $active_more = $('.active_more');
    var $more_btn = $active_sale.find('#sale_down_btn');
    var $less_btn = $active_more.find('#sale_up_btn');

    // 数量
    var $count_change = $('.count_change');
    var $count = $count_change.prev();
    var now_count = 0;
    var $count_add = $count_change.find('.count_add');
    var $count_less = $count_change.find('.count_less');
    var re_count = /^\d+$/;

    // 看了又看
    var $look_list = $('.look ul');
    var look_num = $look_list.children().length-3;
    var $l_prev_btn =$('#l_prev_btn');
    var $l_next_btn =$('#l_next_btn');
    var freq = 0;

    // 宝贝排行榜
    var $rank_filter = $('.g_ranking h4 a');
    var $rank_list1 = $('#filter1');
    var $rank_list2 = $('#filter2');
    
    // 商品详情，累计评价
    var $main_header = $('.m_header');
    var $info = $('.m_body');
    var $discuss_header = $('.m_discuss');

    // 评价
    var $discuss_op_con = $('.d_op_con');
    var $op_right = $('.op_right');
    var $default_no = $op_right.find('.default_no');
    var $d_desc = $('.df_des');
    var $d_main = $('.df_main input');
    var $discuss = $('.d_body tr');
    var $have_add = $('.d_body').find('.have_add');
    var $have_pic = $('.d_body').find('.have_pic');


    // 更多优惠
    $more_btn.click(function () {
        $active_more.show();
    });
    $less_btn.click(function () {
        $active_more.hide();
    });


    // 数量
    $count.keyup(function() {
        now_count = parseInt($count.val());
        if(now_count == 0 | !(re_count.test(now_count))) {
            now_count = 1;
        }
        $(this).val(now_count);
    });

    $count_add.click(function() {
        now_count = parseInt($count.val());
        now_count++;
        $count.val(now_count);
    });
    $count_less.click(function() {
        now_count = parseInt($count.val());
        now_count--;
        if(now_count<1){
            now_count = 1;
        }
        $count.val(now_count);
    });


    // 看了又看
    $l_next_btn.click(function() {
        freq++;
        if (freq>look_num) {
            freq = look_num;
            return;
        }
        now_top = -190*freq;
        $look_list.animate({"top": now_top});
    });
    $l_prev_btn.click(function() {
        freq--;
        if (freq<0) {
            freq = 0;
            return;
        }
        now_top = -190*freq;
        $look_list.animate({"top": now_top});
    });


    // 宝贝排行榜
    $rank_filter.mouseenter(function() {
       $(this).addClass('r_active').siblings().removeClass('r_active');
       if($(this).index() == 0) {
            $rank_list1.addClass('default_filter').siblings().removeClass('default_filter');
       }
       else {
            $rank_list2.addClass('default_filter').siblings().removeClass('default_filter');
       }
    });


    // 商品详情，累计评价
    $main_header.delegate('li', 'click', function() {
        $(this).addClass('m_active').siblings().removeClass('m_active');
        if($(this).index() != 0) {
            $info.hide();
            $discuss_header.find('h5').hide();
        }
        else {
            $info.show();
            $discuss_header.find('h5').show();
        }
    });


    // 评价
    $op_right.find('i').click(function() {
        $discuss_op_con.toggleClass('default_hidden');
        $default_no.toggleClass('change_show');
    });

    $d_desc.find('i').click(function() {
       $(this).parent().next().toggle(); 
    });
    
    $d_main.click(function() {
        if($(this).prop('cheaked', true)) {
            if($(this).prop('id') == 'd_have_add_btn') {
                $have_add.show();
                $discuss.not('.have_add').hide();
            }
            else if ($(this).prop('id') == 'd_have_pic_btn') {
                $have_pic.show();
                $discuss.not('.have_pic').hide();
            }
            else {
                $discuss.show();
            }
        }
    });
    
};


// register page
function register() {
                
    // 初始化

    // 协议部分
    var $pact = $('.pact');
    var pact_agree = $('#agree');
    var pact_close = $('#close');

    // 步骤头部分
    var $step_head = $('.step_title div');

    // 步骤部分
    var $step1 = $('.step1');
    var $step2 = $('.step2');
    var $step3 = $('.step3');
    var $step4 = $('.step4');

    // 每个步骤需要的组件
    var $user_name = $step1.find('#user');
    var step1_msg = $step1.find('.msg');
    var $form = $step2.find('form');
    var $user_mail = $step4.find('#user_mail');
   

    // 每个步骤的提交按钮
    var step1_btn = $('#step1_btn');
    var afteradd_btn = $step3.find('#afteradd');
    var resend_link = $step4.find('#resend_link');
    var success_btn = $step4.find('#success_btn');
    // 验证码刷新
    var refersh_proc = false;
    var timer2 = null;
    var ver_re_btn = $step2.find('.vercode_pic');
    var ver_resh = ver_re_btn.find('i');
    
    // 表单组件
    var d_name = $form.find('#username');
    var d_pwd = $form.find('#pwd');
    var d_apwd = $form.find('#apwd');
    var d_tel = $form.find('#tel');
    var d_mail = $form.find('#mail');
    var d_code = $form.find('#code');
    
    // 表单数据
    var usr_name = '';
    var usr_pwd = '';
    var usr_apwd = '';
    var usr_tel = '';
    var usr_mail = '';
    var usr_code = '';
    var csrftoken = $.cookie('csrftoken');
    // 正则
    var re_name = /^[\u4e00-\u9fa5A-Za-z_][\u4e00-\u9fa5A-Za-z\d_]{3,15}$/
    var re_pwd = /^.*(?=.{6,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[[!@#$%^&*?\.,]).*$/;
    var re_mail = /^[\-_]?[A-Za-z\d\.]+[\-_]?[A-Za-z\d\.]+[\-_]?@[\-_]?[A-Za-z\d]+[\-_]?[A-Za-z\d]+[\-_]?\.[A-Za-z]{2,6}(\.[A-Za-z]{2,6})*$/;
    var re_tel = /^(\+?0?86\-?)?1[345789]\d{9}$/;
    var re_code = /^[A-Za-z0-9]{4}$/;

    // 校验过程
    var pass_name = false;
    var pass_pwd = false;
    var pass_apwd = false;
    var pass_tel = false;
    var pass_mail = false;
    var pass_code = false;

    // 重新发送邮件
    var $resend_email = $('#resend_email');
    var $resend_btn = $('#resend_btn');
    var recv_mail = '';
    var timer1 = null;
    var leftNum = 60;
    var c_switch = false;

    // 返回数据
    var msg = '';

    
    pact();

    // 步骤一 校验用户名
    step1_btn.click(function() {
        d_name.focus(function() {
            step1_msg.hide();
        });
        usr_name = $user_name.val();
        // 判断用户名是否为空
        if (usr_name == "") {
            step1_msg.html('请输入用户名!')
            step1_msg.show();
            
        }
        // 判断用户名是否合法
        else if (!(re_name.test(usr_name))) {
            step1_msg.html("用户名为4-16位字母、数字、中文或'_'的组合,不能以数字开头")
            step1_msg.show();
        }
        else {
            // 发送ajax请求
            $.ajax({
                url: '/user/register_handle', 
                type: 'get',
                datatype: 'json',
                data: {"name": usr_name}
            })
            .done(function(data) {
                msg = data.msg;
                 // 判断用户名是否已存在
                if (msg == 'existed'){
                    step1_msg.html('用户名已存在!')
                    step1_msg.show();
                }
                else {
                    pass_name = true;
                    $step1.hide();
                    // 步骤二头部激活效果
                    $step_head.eq(1).addClass('active').siblings().removeClass('active');
                    $step2.show();
                    // 把步骤一输入验证后的用户名传给步骤二的表单隐藏域
                    d_name.val(usr_name);
                }
            })
            .fail(function() {
                alert('网络繁忙，请稍后重试！');
            });
        }
    });


    $form.delegate('input', 'focus', function() {
        $(this).next().html('').hide();
    });

    
    // 密码
    d_pwd.blur(function() {
        usr_pwd = d_pwd.val();
        if (usr_pwd == '') {
            $(this).next().html('请输入密码!').show();
        }
        else if (re_pwd.test(usr_pwd)) {
            pass_pwd = true;
        }
        else {
            $(this).next().html('最少6位,至少包含一位大写字母、小写字母、数字和特殊符号!').show();
        }
    });
    
    // 重复输入密码
    d_apwd.blur(function() {
        usr_apwd = d_apwd.val();
        if(usr_apwd == '') {
            $(this).next().html('请重复输入密码!').show();
        }
        else if (usr_apwd !== usr_pwd) {
            $(this).next().html('密码错误,请重新输入!').show();
        }
        else {
            pass_apwd = true;
        }
    });

    // 邮箱
    d_mail.blur(function() {
        usr_mail = d_mail.val();

        if(usr_mail == '') {
            $(this).next().html('请输入邮箱地址!').show();
        }
        else if (re_mail.test(usr_mail)) {
            pass_mail = true;
        }
        else {
            $(this).next().html('邮箱格式不正确,请重新输入!').show();
        }
    });

    // 手机号
    d_tel.blur(function() {
        usr_tel = d_tel.val();

        if(usr_tel == '') {
            $(this).next().html('请输入手机号码!').show();
        }
        else if (re_tel.test(usr_tel)) {
            pass_tel = true;
        }
        else {
            $(this).next().html('请输入中国大陆手机号码!').show();
        }
    });

    // 验证码
    d_code.blur(function() {
        usr_code = d_code.val();

        if(usr_code == '') {
            $(this).next().html('请输入验证码!').show();
        }
        else if (re_code.test(usr_code)) {
            pass_code = true;
        }
        else {
            $(this).next().html('验证码错误!').show();
        }
    });

    // vercode_refresh 验证码刷新
    ver_re_btn.click(function() {
        if (refersh_proc) {
            return;
        }
        refersh_proc = true;

        ver_resh.addClass('i_ro');
        $(this).find('img').prop('src','../images/vercode2.png');

        clearTimeout(timer2);
        timer2 = setTimeout(function() {
            ver_resh.removeClass('i_ro');
            refersh_proc = false;
        },500);
    });
    

    // 步骤二 校验表单数据
    $form.submit(function(e) {
        e.preventDefault();
        // 判断表单选项是否漏输
        if (pass_name & pass_pwd & pass_apwd & pass_mail & pass_tel & pass_code) {
            // 发送ajax请求
            $.ajax({
                url: '/user/register_handle', 
                type: 'post',
                datatype: 'json',
                headers: {"X-CSRFToken": csrftoken},
                data: {
                    "name": usr_name,
                    "pwd": usr_pwd,
                    "apwd": usr_apwd,
                    "tel": usr_tel,
                    "mail": usr_mail,
                    "code": usr_code
                }
            })
            .done(function(data) {
                msg = data.msg;
                if (msg == 'success') {
                    $step2.hide();
                    // 步骤三头部激活效果
                    $step_head.eq(2).addClass('active').siblings().removeClass('active');
                    $step3.show();
                    $user_mail.html(usr_mail);
                }
                else if (msg == 'incomplete') {
                    alert('IncomplateError:数据不完整，请重试!');
                }
                else if (msg == 'email_illegal'){
                    alert('EmailIllegal:邮箱不支持，请重试!');
                }
            })
            .fail(function() {
                alert('网络繁忙，请稍后重试!');
            });
        }
        else {
            alert('所有项均不能为空!');
        }
    });
    // 步骤三，暂时跳过按钮
    afteradd_btn.click(function() {
        $step3.hide();
        // 步骤四头部激活效果
        $step_head.eq(3).addClass('active').siblings().removeClass('active');
        $step4.show();
    });

    // 步骤四
    success_btn.click(function() {
        window.location.href = "/";
    });
    resend_link.click(function() {
        $step4.find('.r_input_con').hide().next().show();
        $resend_email.val(usr_mail);
    });
    // 重新发送邮件
    $resend_email.focus(function() {
        $(this).next().html('').hide();
    });
    $resend_btn.click(function() {
        recv_mail = $resend_email.val();

        
        if(recv_mail == '') {
            $resend_email.next().html('请输入邮箱地址!').show();
        }
        else if (re_mail.test(recv_mail)) {
            if (c_switch) {
                return;
            };
            // 发送ajax请求
            // $.ajax({
            //     url: 'https://api.apiopen.top/searchAuthors?', 
            //     type: 'get',
            //     datatype: 'jsonp',
            //     data: {"name": "李白"}
            // })
            // .done(function(data) {
            //     console.log(data);
            //     // $('.p1').html(data.result[0].desc);
            // })
            // .fail(function() {
            //     alert('服务器超时，请重试！');
            // });
            c_switch = true;
            $(this).parent().parent().hide().prev().show();
            $user_mail.html(recv_mail);
            timer1 = setInterval(function() {
                leftNum--;
                $resend_btn.addClass('disabled');
                $resend_btn.val("" + leftNum +"秒后可重新发送");

                if (leftNum<0) {
                    $resend_btn.removeClass('disabled');
                    leftNum = 60;
                    clearInterval(timer1);
                    $resend_btn.val("重新发送");
                    c_switch = false;
                }
            },1000);
        }
        else {
            $resend_email.next().html('邮箱格式不正确,请重新输入!').show();
        }
    });
   
    // 协议
    function pact() {
        pact_agree.click(function() {
            $pact.hide();
            $step1.show();
        });
        pact_close.click(function() {
            window.location.href = "index.html";
        })
    };
};


// goods_list page goods_detail page

// 底部分页
function pagenater() {
				
    var $result_pagena = $('.result_pagena');
    var $page_con = $result_pagena.find('.page_con');
    var $all_pages = $('.all_pages');
    var pages = parseInt($all_pages.html());
    var p = 1;
    var $r_prev_page = $('#r_prev_page');
    var $r_next_page = $('#r_next_page');
    var $page_to = $('#page_to');
    var $page_to_btn = $('#page_to_btn');
    var re_to = /^\d+$/

    $page_to_btn.click(function() {
        topage = parseInt($page_to.val());
        if(topage == 0 | !(re_to.test(topage))) {
            console.log(topage);
            console.log('exit');
            return;
        }
        else{
            p = topage;
            console.log(topage);
            console.log('success');
        }
    });

    $r_next_page.click(function() {
        p++;
        if (p>pages) {
            $r_next_page.addClass('now_page');
            p = pages;
            return;
        }
        if(p>1) {
            $r_prev_page.removeClass('now_page');
        }
        console.log(p);

    });
    $r_prev_page.click(function() {
        p--;
        if (p<1) {
            $r_prev_page.addClass('now_page');
            p = 1;
            return;
        }
        if(p<pages) {
            $r_next_page.removeClass('now_page');
        }
        console.log(p);
    })
    $page_con.delegate('a', 'click', function () {
        $(this).addClass('now_page').parent().siblings().children().removeClass('now_page');
    })
};

// 过滤条件区
function filter_con(params) {
				
    var $filter_con = $('.f_many');
    var $filter_more = $('.more');
    var $check_con = $('.check_con');
    // 过滤区分页器
    var $page_prev = $('#f_prev_page');
    var $page_next = $('#f_next_page');
    var i = 1;
    var all_page_num = 0;

    f_prev_page

    $filter_con.delegate('a', 'click', function() {
        $(this).addClass('f_active').siblings().removeClass('f_active');
    });

    
    $filter_more.click(function() {
        $check_con.toggleClass('show_all');
    });

    // 分页器
    
    $page_next.click(function() {
        i++;
        all_page_num = parseInt($(this).prev().prev().children().eq(1).html());

        if (i>all_page_num) {
            $page_next.addClass('active_btn').prev().removeClass('active_btn');
            i = all_page_num;
            return;
        }
        if (i>1) {
            $page_prev.removeClass('active_btn').next().removeClass('active_btn');
        }
        $(this).prev().prev().children().eq(0).html(i);
    });

    $page_prev.click(function() {
        i--;
        if (i<1) {
            $page_prev.addClass('active_btn').next().removeClass('active_btn');
            i = 1;
            return;
        }
        if (i<all_page_num) {
            $page_next.removeClass('active_btn').prev().removeClass('active_btn');
        }
        $(this).prev().children().eq(0).html(i);
    });
};


// goods_cart page
// 目前较多bug未解决
// function shop_cart() {
//     // 结算头 
//     var $cart_con = $('.cart_con');
//     var $se_header = $('.se_header');
//     var $settle_right = $('.settle_right');
//     var $all_chex = $('.chex');
//     var $check_all = $('#check_all_goods');
//     var $check_store = $('.check_now_store');
//     var $check_one = $('.check_one_goods');
//     var $s_group = $('.s_group');
//     var $s_goods = $('.s_goods');
//     var $remove_goods = $s_goods.find('.s_op p ').eq(1).find('a');
//     var all_checked = false;
//     var store_checked = false;
//     var one_checked = false;

//     $cart_con.delegate('.chex', 'click', function() {
//         if($(this).prop('checked')) {
//             $settle_right.find('input').addClass('se_enabled');
//         }
//         else {
//             $settle_right.find('input').removeClass('se_enabled');
//         }
        
//     });
//     $remove_goods.each(function() {
//         $(this).click(function() {
//             if($(this).parent().parent().parent().parent().siblings().length < 2) {
//                 $(this).parent().parent().parent().parent().parent().remove();
//             }
//             $(this).parent().parent().parent().parent().remove();
//         });
//     });

//     // 商品
//     var $goods_count = $s_goods.find('.s_count input').eq(1);
//     var $count_add = $goods_count.next();
//     var $count_less = $goods_count.prev();
//     var $one_price = $s_goods.find('.s_oneprice em');
//     var $many_price = $s_goods.find('.s_manyprice em');
//     var $all_price = $settle_right.find('em');
//     var now_count = 0;
//     var c_one_price = parseInt(parseFloat($one_price.html())*100);
//     var c_many_price = 0;
//     var c_all_price = 0;
//     var re_count = /^\d+$/;
    

//     // 单个商品价格数量区域
//     $goods_count.keyup(function() {
//         now_count = parseInt($goods_count.val());
//         if(now_count == 0 | !(re_count.test(now_count))) {
//             now_count = 1;
//         }
//         $(this).val(now_count);
//         c_many_price = now_count*c_one_price/100;

//         $many_price.html(c_many_price);
//         c_all_price = c_many_price;
//         console.log(c_all_price);

//     });
//     $count_add.click(function() {
//         now_count = parseInt($goods_count.val());
//         now_count++;
//         $goods_count.val(now_count);
//         c_many_price = now_count*c_one_price/100;
//         $many_price.html(c_many_price);
//         c_all_price = c_many_price;
//         console.log(c_all_price);
//     });
//     $count_less.click(function() {
//         now_count = parseInt($goods_count.val());
//         now_count--;
//         if(now_count<1){
//             now_count = 1;
//         }
//         $goods_count.val(now_count);
//         c_many_price = now_count*c_one_price/100;
//         $many_price.html(c_many_price);
//         c_all_price = c_many_price;
//         console.log(c_all_price);
//     });

//     $se_header.delegate('a', 'click', function() {
//         $(this).addClass('se_op').siblings().removeClass('se_op');
//     })

//     // 全选整个购物车的所有商品
//     $check_all.click(function () {
//         if($(this).prop('checked')) {
//             $check_store.prop('checked', true);
//             $check_one.prop('checked', true);
//         }
//         else {
//             $check_store.prop('checked', false);
//             $check_one.prop('checked', false);
//         }
//     });
    
//     // 选中购物车中某个商品
//     $s_group.delegate('.check_now_store', 'click', function() {
//         if($(this).prop('checked')) {
//             $(this).parent().parent().find('.check_one_goods').prop('checked', true);
//         }
//         else {
//             $(this).parent().parent().find('.check_one_goods').prop('checked', false);
//         }
//     });

    // $s_goods.delegate('.check_one_goods', 'click', function() {
    //     if($(this).prop('checked')) {
    //         now_count = parseInt($goods_count.val());
    //         c_many_price = now_count*c_one_price/100;
    //         c_all_price += c_many_price;
    //         one_checked = true;
    //     }
    //     else {
    //         c_all_price = 0.00;
    //         one_checked = false;
    //     }
    //     isCheck();
    // });
    
    // $settle_right.find('input').click(function() {
    //     // console.log(all_checked);
    //     // console.log(store_checked);
    //     // console.log(one_checked);
    // });

    // function isCheck () {
    //     if (one_checked | all_checked | store_checked) {
    //         $settle_right.find('input').addClass('se_enabled');
    //         $all_price.html(c_all_price);
    //     }
    //     else {
    //         $settle_right.find('input').removeClass('se_enabled');
    //         $all_price.html('0.00');
    //     }
    // };
    
// };