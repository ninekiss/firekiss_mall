$(function () {
    var $global_chexbox = $('input[type="checkbox"]'),
        $all_chexbox = $('.all_chex'),
        $group_chexbox = $('.group_chex'),
        $goods_chexbox = $('.goods_chex');

    var $goods_group = $('.s_group'),
        $every_goods = $('.s_goods');

    // 全局全选与取消全选
    $all_chexbox.click(function() {
        var $chexs = $goods_group.find('input[type="checkbox"]');
        if($(this).is(':checked')) {
            $chexs.prop("checked", true);
        }
        else {
            $chexs.prop("checked", false);
        }
        totalMoney();
    });

    // 单个商品与全选
    $goods_chexbox.each(function() {
        $(this).click(function () {
            if($(this).is(':checked')) {
                //判断：所有单个商品是否勾选
                var goods_len = $goods_chexbox.length;
                var num = 0;
                $goods_chexbox.each(function () {
                    if ($(this).is(':checked')) {
                        num++;
                    }
                });
                if (num == goods_len) {
                    $all_chexbox.prop("checked", true);
                }
            }
            else {
                //单个商品取消勾选，全局全选取消勾选
                $all_chexbox.prop("checked", false);

            }
            totalMoney();
        });
    });

    // 每个店铺与全选
    $group_chexbox.each(function() {
        $(this).click(function () {
            if($(this).is(':checked')) {
                //判断：所有店铺是否勾选
                var group_len = $group_chexbox.length;
                var num = 0;
                $group_chexbox.each(function () {
                    if ($(this).is(':checked')) {
                        $(this).parents().nextAll().find('.goods_chex').prop("checked", true);
                        num++;
                    }
                    else {
                        $(this).parents().nextAll().find('.goods_chex').prop("checked", false);
                    }
                });
                if (num == group_len) {
                    $all_chexbox.prop("checked", true);
                }
            }
            else {
                var group_len = $group_chexbox.length;
                var num = 0;
                $group_chexbox.each(function () {
                    if ($(this).is(':checked')) {
                        $(this).parents().nextAll().find('.goods_chex').prop("checked", true);
                        num++;
                    }
                    else {
                        $(this).parents().nextAll().find('.goods_chex').prop("checked", false);
                    }
                });
                //单个店铺取消勾选，全局全选取消勾选
                $all_chexbox.prop("checked", false);
            }
            totalMoney();
        });
    });

    // 单个店铺与其商品
    // 店铺中的商品有一个未选中，则该店铺全选按钮取消选中，若全都选中，则全选打对勾
    $goods_group.each(function () {
        // 店铺下的商品
        var $goods_chexbox = $(this).find('.goods_chex');
        $goods_chexbox.each(function () {
            $(this).click(function () {
                if ($(this).is(':checked')) {
                    //判断：如果所有该店铺的商品都选中则该店铺全选打对勾
                    var goods_lens = $goods_chexbox.length;
                    var num = 0;
                    $goods_chexbox.each(function () {
                        if ($(this).is(':checked')) {
                            num++;
                        }
                    });
                    if (num == goods_lens) {
                        $(this).parents().parents().parents().parents().children().eq(0).find('.group_chex').prop("checked", true);
                    }
                }
                else {
                    //否则，店铺全选取消
                    $(this).parents().parents().parents().parents().children().eq(0).find('.group_chex').prop("checked", false);
                }
                totalMoney();
            });
        });

    });

    $every_goods.each(function(){

        var now_count = 0;
        var now_price = 0;
        var re_count = /^\d+$/;

        // 每个商品的数量
        var $count_con = $(this).find('.s_count input');
        var $goods_count = $count_con.eq(1);
        var $count_add = $count_con.eq(2);
        var $count_less = $count_con.eq(0);
        
        // 每个商品的单价
        var $one_price = $(this).find('.s_oneprice em');
        // 每个商品的小计
        var $many_price = $(this).find('.s_manyprice em');

        var c_one_price = parseInt(parseFloat($one_price.html())*100);

        // 当前的商品数量
        $goods_count.keyup(function() {

            now_count = parseInt($(this).val()); 
            
            if(now_count == 0 | !(re_count.test(now_count))) {
                now_count = 1;
            }
            $(this).val(now_count);
            now_price = now_count*c_one_price/100;
            $many_price.html(now_price);
            totalMoney();
        });

        $count_add.click(function() {
            now_count = parseInt($goods_count.val());
            now_count++;
            $goods_count.val(now_count);
            now_price = now_count*c_one_price/100;
            $many_price.html(now_price);
            totalMoney();
        });

        $count_less.click(function() {
            now_count = parseInt($goods_count.val());
            now_count--;
            if(now_count<1){
                now_count = 1;
            }
            $goods_count.val(now_count);
            now_price = now_count*c_one_price/100;
            $many_price.html(now_price);
            totalMoney();
        });
    });

    function totalMoney() {
        var total_money = 0;
        var total_count = 0;
        // 结算区域
        var $settle_right = $('.settle_right');
        // 已选商品的总价
        var $all_price = $settle_right.find('em');

        $goods_chexbox.each(function () {
            
            if ($(this).is(':checked')) {
                var money = $(this).parents().parents().find('.s_manyprice h6 em');
                var count = $(this).parents().parents().find('.s_count input').eq(1);
                total_money += parseFloat(money.html())*100;
                total_count += parseInt(count.val());
            }
        });
        if(total_money!=0 && total_count!=0){
            $all_price.html(total_money/100);
            $settle_right.find('input').addClass('se_enabled');
        }
        else {
            $all_price.html('0.00');
            $settle_right.find('input').removeClass('se_enabled');
        }
    };
});