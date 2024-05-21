function fetchWishlist() {
    $.ajax({
        url: '/api/wishlist/',
        type: 'GET',
        success: function (response) {
            // console.log('Success:', response);
            // Do something with the response data
            $('.js-show-wishlist').each(function () {
                $(this).attr('data-notify', response.length);
            });
            $(".header-cart-wrapitem.wishlist").empty()
            response.items.length === 0 && $(".header-cart-wrapitem.wishlist").append("<li class='text-black'>Wishlist Is Empty.</li>")
            response.items.forEach(item => {
                $(".header-cart-wrapitem.wishlist").append(WishListCard(item))
            })
            $(".header-cart-total-price.wishlist").text(`$${response.cart_total_price}`)
            WishListProductDelete()

        },
        error: function (xhr, status, error) {
            console.error('Error:', error);
            $('.js-show-cart').each(function () {
                $(this).attr('data-notify', "0");
            });
        }
    });
}

function WishListCard(data) {
    const {image, name, price, id} = data;
    return (`
                    <li class="header-cart-item flex-w flex-t m-b-12">
                            <div class="header-cart-item-img-wishlist" data-product="${id}">
                                <img src="${image}" alt="${name}">
                            </div>

                            <div class="header-cart-item-txt p-t-8">
                                <a href="#" class="header-cart-item-name m-b-18 hov-cl1 trans-04">
                                   ${name}
                                </a>

                                <span class="header-cart-item-info">
                                    $${price}
                                </span>
                            </div>
                        </li>
    `)
}

function WishListProductDelete() {
    $(".header-cart-item-img-wishlist").each(function () {
        $(this).on("click", function () {
            const product_id = $(this).attr("data-product")
            WishListDeleteRequest(product_id, $(this))
        })
    })
}

function WishListDeleteRequest(product_id, varibale) {
    $.ajax({
        url: "/api/wishlist/",
        type: "POST",
        headers: {
            "X-CSRFToken": Cookies.get('csrftoken')
        },
        data: {
            product_id: product_id,
        },
        beforeSend: function () {
            varibale.off("click")
        },
        success: function (response) {
            // Handle successful response
            // console.log('Success:', response);
            $(`.wishlist-images-switch[data-product='${response.product_id}']`).empty();
            $(`.wishlist-images-switch[data-product='${response.product_id}']`).html(`
                        <a  class="btn-addwish-b2 dis-block pos-relative ${response.action=='added'?'js-addedwish-b2':'js-addwish-b2'}">
                                <img class="icon-heart1 dis-block trans-04" src="${staticUrl}images/icons/icon-heart-01.png" alt="ICON">
                                <img class="icon-heart2 dis-block trans-04 ab-t-l" src="${staticUrl}images/icons/icon-heart-02.png" alt="ICON">
                         </a>
                        `)

             mainData = mainData.map(item => {
                            if (item.id == response.product_id) {
                                if (response.action == "added") {
                                    return {...item, in_wishlist: true}
                                } else {
                                    return {...item, in_wishlist: false}
                                }

                            }
                            return {...item}
                        })

            fetchWishlist()
        },
        error: function (xhr, status, error) {
            // Handle error response
            console.error('Error:', error);
        },
        complete: function () {
            varibale.on("click")
        }
    })
}


$(window).ready(function () {
    // {#fetchCart()#}
    WishListProductDelete()
})

