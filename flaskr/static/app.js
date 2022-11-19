$("#modify-user-table").on('click', '.delete-user-button', function(e) {
    var user_id = $(this).attr('user_id')

    var which_tr = $(this).closest("tr");

    which_tr.remove();

    $.ajax({
            type: "POST",
            url: "/delete_user",
            data: {"user_id" : user_id},
        })

    e.preventDefault();
});

$("#modify-user-table").on('click', '.confirm-user-button', function(e) {
    var user_id = $(this).attr('user_id')

    $(this).remove()

    $.ajax({
            type: "POST",
            url: "/confirm_user",
            data: {"user_id" : user_id},
        })

    e.preventDefault();
});

$("#all-products-table").on('click', '.add-product-to-cart', function(e) {
    var prod_id = $(this).attr('prod_id')

    $(this).remove()

    $.ajax({
            type: "POST",
            url: "/add_product_to_cart",
            data: {"prod_id" : prod_id},
        })

    e.preventDefault();
});

$("#modify-product-table").on('click', '.delete-product-button', function(e) {
    var prod_id = $(this).attr('prod_id')

    var which_tr = $(this).closest("tr");

    which_tr.remove();

    $.ajax({
            type: "POST",
            url: "/delete_product",
            data: {"prod_id" : prod_id},
        })

    e.preventDefault();
});

$("#modify-cart-table").on('click', '.delete-product-from-cart-button', function(e) {
    var prod_id = $(this).attr('prod_id')
    var cart_id = $(this).attr('cart_id')

    var which_tr = $(this).closest("tr");

    which_tr.remove();

    $.ajax({
            type: "POST",
            url: "/remove_product_from_cart",
            data: {"prod_id" : prod_id, "cart_id" : cart_id},
        })

    e.preventDefault();
});



