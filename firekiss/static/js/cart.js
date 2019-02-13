$(function () {
    // 商品购物车js

    // 全选
    // 整个购物车全选框改变时
    $('.all_chex').change(function () {
        // 全选是否选中
        is_checked = $(this).prop('checked');

        // 使每个复选框的状态与全选保持一致
        $('.se_body').find(':checkbox').each(function () {
             $(this).prop('checked', is_checked);
        });

        update_page_info();
    });

    // 除了顶级全选以外的复选框
    checkbox_count = $(':checkbox').length-1;

    // 购物车页面的所有复选框
    $(':checkbox').change(function () {
        if ($(this).prop('checked')){
            // 更该结算按钮样式，允许结算
            $('.settle_right').find('input').addClass('allow_settle');

            if($(':checked').length == checkbox_count){
                $('.all_chex').prop('checked', true);
            }
        }
        else {
            if ($(':checked').length <= 0) {
                // 未选中，不允许结算
                $('.settle_right').find('input').removeClass('allow_settle');
            }

            $('.all_chex').prop('checked', false);
        }
        update_page_info();
    });

    // 每个店铺全选框改变时
    $('.group_chex').change(function () {
        if ($(this).prop('checked')) {
            // 选中
            // 该店铺的所有商品选中
            $(this).parents('.s_group').find(':checkbox').prop('checked',true);

            if($(':checked').length == checkbox_count){
                // 全部选中
                $('.all_chex').prop('checked', true);
            }
        }
        else {
            // 该店铺的所有商品取消选中
           $(this).parents('.s_group').find(':checkbox').prop('checked',false);
        }
        update_page_info();
        if ($(':checked').length <= 0) {
            // 未选中，不允许结算
            $('.settle_right').find('input').removeClass('allow_settle');
        }
   });

    // 每个商品的复选框
    $('.goods_chex').change(function () {
        //该店铺的所有商品复选框
        group_chex_count = $(this).parents('.s_group').find(':checkbox').length-1;

        if ($(this).prop('checked')) {
            group_chexd = $(this).parents('.s_group').find(':checked').length;
            if(group_chexd == group_chex_count){
                // 全部选中
                $(this).parents('.s_group').find('.group_chex').prop('checked', true);
            }
            if($(':checked').length == checkbox_count){
                // 全部选中
                $('.all_chex').prop('checked', true);
            }
        }
        else {
            $(this).parents('.s_group').find('.group_chex').prop('checked', false);
        }
        update_page_info();

        if ($(':checked').length <= 0) {
            // 未选中，不允许结算
            $('.settle_right').find('input').removeClass('allow_settle');
        }
    });


    // 数量增加
    $('.update_goods_count').next().click(function () {
        // sku_id
        sku_id = $(this).prev().attr('sku_id');
        // 获取要添加的商品的数量
        count = $(this).prev().val();
        count = parseInt(count)+1;

        // 发送ajax请求，更新购物车商品记录
        update_cart_info(sku_id, count)

        if (update_success) {
            // 如果更新成功,更新商品数据
            // 设置商品的数量
            $(this).prev().val(count);

            // 设置商品小计
            update_goods_amount($(this).parents('.s_goods'));

            // 获取商品对应的复选框
            is_checked = $(this).parents('.s_goods').find(':checkbox').prop('checked');

            if(is_checked) {
                // 如果选中，更新页面信息
                update_page_info();
            }

            // 更新页面上的商品总数量
            $('.se_op').find('em').text(total_count);
        }
    });

    // 数量减少
    $('.update_goods_count').prev().click(function () {
        // sku_id
        sku_id = $(this).next().attr('sku_id');
        // 获取要添加的商品的数量
        count = $(this).next().val();
        count = parseInt(count)-1;
        if (count <= 0) {
            return
        }

        // 发送ajax请求，更新购物车商品记录
        update_cart_info(sku_id, count)

        if (update_success) {
            // 如果更新成功,更新商品数据
            // 设置商品的数量
            $(this).next().val(count);

            // 设置商品小计
            update_goods_amount($(this).parents('.s_goods'));

            // 获取商品对应的复选框
            is_checked = $(this).parents('.s_goods').find(':checkbox').prop('checked');

            if(is_checked) {
                // 如果选中，更新页面信息
                update_page_info();
            }

            // 更新页面上的商品总数量
            $('.se_op').find('em').text(total_count);
        }
    });

    // 手动输入商品数量
    $('.update_goods_count').keyup(function() {
        // 校验手动输入的正则
        re_count = /^\d+$/;
        // 获取要添加的商品的数量
        count = parseInt($(this).val());
        if(count == 0 | !(re_count.test(count))) {
            count = 1;
        }
        $(this).val(count);
    });
    $('.update_goods_count').blur(function() {
        // sku_id
        sku_id = $(this).attr('sku_id');
        // 获取要添加的商品的数量
        count = parseInt($(this).val());
        // 发送ajax请求，更新购物车商品记录
        update_cart_info(sku_id, count)

        if (update_success) {
            // 如果更新成功,更新商品数据
            // 设置商品的数量
            $(this).val(count);

            // 设置商品小计
            update_goods_amount($(this).parents('.s_goods'));

            // 获取商品对应的复选框
            is_checked = $(this).parents('.s_goods').find(':checkbox').prop('checked');

            if (is_checked) {
                // 如果选中，更新页面信息
                update_page_info();
            }

            // 更新页面上的商品总数量
            $('.se_op').find('em').text(total_count);
        }
    });

    // 删除商品
    $('.cart_del_goods').click(function () {
        // 商品id(sku_id)
        sku_id = $(this).parents('.s_goods').find('.update_goods_count').attr('sku_id');

        // csrf
        csrf = $('input[name="csrfmiddlewaretoken"]').val();

        content = {"sku_id": sku_id, "csrfmiddlewaretoken": csrf}

        // 店铺元素
        store_ele = $(this).parents('.s_group');
        // 商品元素
        goods_ele = $(this).parents('.s_goods');
        // 商品数量
        goods_len = $(this).parents('.s_group').find(':checkbox').length-1;

        // 发送ajax post 请求
        $.post('/cart/delete', content, function (data) {
            status = data.status;
            if (status == 200 ){
                // 删除成功
                // 判断该店铺剩余的商品数量
                if (goods_len <= 1) {
                    // 该店铺只有一件商品,删除店铺元素
                    store_ele.remove();
                }
                else {
                    // 该店铺只有一件商品,删除商品元素
                     goods_ele.remove();
                }

                // 获取要删除的商品的选中状态
                is_checked = goods_ele.find(':checkbox').prop('checked');

                if (is_checked){
                    // 已选中，更新页面信息
                    update_page_info();
                }

                // 更新页面上的商品总数量
                $('.se_op').find('em').text(total_count);

                if ($(':checked').length <= 0) {
                // 未选中，不允许结算
                $('.settle_right').find('input').removeClass('allow_settle');

                // 更新页面上的复选框数量
                checkbox_count = $(':checkbox').length-1;
            }
            }
            else {
                alert(data.msg);
            }
        })


    });

    // 计算被选中的商品的总价和总数量
    function update_page_info() {
        total_count = 0;
        total_price = 0;
        // 选中的商品所在的div
        $('.s_goods').find(':checked').parents('.s_goods').each(function () {
            // 获取商品的数目和小计
            count = $(this).find('.update_goods_count').val();
            amount = $(this).find('.update_amount_price').text();
            count = parseInt(count);
            amount = parseFloat(amount);
            total_count += count;
            total_price += amount;
        })

        // 设置被选中的商品的总件数和总价格
        $('.settle_right').each(function () {
            $(this).find('b').text(total_count);
            $(this).find('em').text(total_price.toFixed(2));
        })
    };

    // 发送ajax请求，更新购物车商品记录
    function update_cart_info(sku_id, count) {
        // ajax post请求
        // 商品id(sku_id),数量(count)
        // csrf
        csrf = $('input[name="csrfmiddlewaretoken"]').val();

        // 组织参数
        content = {
            "sku_id": sku_id,
            "count": count,
            "csrfmiddlewaretoken": csrf
        }

        update_success = false
        total_count = 0;

        // 设置发送同步的ajax请求
        $.ajaxSettings.async = false;
        // 发送ajax post请求
        $.post('/cart/update', content, function (data) {
            status = data.status
            if (status == 200) {
                // 更新成功
                update_success = true;
                total_count = data.total;
            }
            else {
                // 更新失败
                update_success = false;
                alert(data.msg);
            }
        });
         // 设置发送异步的ajax请求
        $.ajaxSettings.async = true;
    };

    // 设置商品小计
    function update_goods_amount(sku_ele) {
        // 数量
        count = sku_ele.find('.update_goods_count').val();
        // 优惠后价格
        price = sku_ele.find('.goods_real_price').text();
        // 小计
        amount = parseInt(count)*parseFloat(price);

        // 设置商品小计
        sku_ele.find('.update_amount_price').text(amount.toFixed(2));

    }
});