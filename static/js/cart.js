function fetchCart() {
    $.ajax({
        url: '/api/cart/',
        type: 'GET',
        success: function (response) {
            console.log('Success:', response);
            // Do something with the response data
            $('.js-show-cart').each(function () {
                $(this).attr('data-notify', response.length);
            });
            $(".header-cart-wrapitem").empty()
            response.items.length === 0 && $(".header-cart-wrapitem").append("<li class='text-black'>Cart Is Empty.</li>")
            response.items.forEach(item=> {$(".header-cart-wrapitem").append(cartCard(item))})
            $(".header-cart-total-price").text(`$${response.cart_total_price}`)
            cartProductDelete()

        },
        error: function (xhr, status, error) {
            console.error('Error:', error);
            $('.js-show-cart').each(function () {
                $(this).attr('data-notify', "0");
            });
        }
    });
}

function cartCard(data) {
    const {image, name, price,id} = data.product;
    return (`
        <li class="header-cart-item flex-w flex-t m-b-12">
        <div class="header-cart-item-img" data-product='${id}' data-color="${data.color?data.color.id : ''}" data-size="${data.size? data.size.id:''}">
            <img src="${image}" alt="${name}">
        </div>
            
        <div class="header-cart-item-txt p-t-8">
            <a href="#" class="header-cart-item-name m-b-18 hov-cl1 trans-04">
            ${name}
            <small class="header-cart-item-info2">
                ${data.size?"(size:" + data.size.size + ")":""} ${data.color?"(color:" + data.color.color + ")":""} 
            </small>
            </a>
            <span class="header-cart-item-info">
            ${data.quantity} x $${price}
            </span>
        </div>
    </li>
    `)
}


function cartProductDelete(){
    $(".header-cart-item-img").each(function (){
        $(this).on("click", function(){
            const product_id = $(this).attr("data-product")
            const size_id = $(this).attr("data-size")
            const color_id = $(this).attr("data-color")
            cartDeleteRequest(product_id, size_id, color_id)
        })
    })
}

function cartDeleteRequest(product_id,size_id,color_id) {
   $.ajax({
                    url:"/api/cart/delete/",
                    type:"POST",
                    headers: {
                        "X-CSRFToken": Cookies.get('csrftoken')
                    },
                    data:{
                        product_id: product_id,
                        size_id: size_id,
                        color_id: color_id,
                    },
                    success: function (response) {
                        // Handle successful response
                        console.log('Success:', response);
                        fetchCart()
                    },
                    error: function (xhr, status, error) {
                        // Handle error response
                        console.error('Error:', error);
                    },
                })
}




$(window).ready(function(){
            // {#fetchCart()#}
            cartProductDelete()
        })