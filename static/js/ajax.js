function remove_from_cart(course) {
    const tr = document.getElementById(`tr${course}`);
    const total_price_label = document.getElementById('gg');
    $.get(`/cart/remove?course=${course}`).then(response => {
        tr.remove();
        swal("حذف شد", "دوره از سبد خرید حذف شد");
        const total_price_with_discount = response['total_price_with_discount']
        const total_price = response['total_price']
        if (response['count_course'] === 0) {
            document.getElementById('payment').remove()
            document.getElementById('cost').remove()
            document.getElementById('tooman').remove()
            document.getElementById('tr-title').remove()
            total_price_label.className = ''
            total_price_label.innerHTML = '<small> سبد خرید شما خالی است </small>'
        } else {
            if (total_price !== total_price_with_discount) {
                total_price_label.innerHTML = `<span class="text-muted" style="text-decoration: line-through;">${total_price}</span> / ${total_price_with_discount}`
            } else {
                total_price_label.textContent = `${total_price}`
            }
        }
    })
}

function add_to_cart(course) {
    const in_cart = document.getElementById('in-cart');
    $.get(`/cart/add?course=${course}`).then(response => {
        in_cart.className = 'btn btn-success btn-block text-white mt-3 py-2 font-12';
        in_cart.textContent = 'در سبد خرید شما موجود است';

        swal("افزوده شد", "دوره به سبد خرید شما افزوده شد");
    })
}

