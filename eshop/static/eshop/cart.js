// script for cart.html **
document.addEventListener("DOMContentLoaded", () => {
    // query for all remove form buttons **
    document.querySelectorAll('.removeform').forEach(button => {
        // set button onclicks **
        button.onclick = function() {
            // get id and price **
            product_id = this.dataset.id
            product_price = this.dataset.price

            // post changes to view **
            fetch('/cart', {
                method: 'POST',
                body: JSON.stringify({
                    product_id: product_id,
                })
            })
            .then(response => response.json())
            .then(result => {
                // debugging **
                console.log(result);

                // update page elements **
                // remove product from page **
                document.querySelector(`#product-${product_id}`).remove()
                // update subtotal **
                document.querySelector('#subtotal').innerHTML = (+document.querySelector('#subtotal').innerHTML - +product_price).toFixed(2).replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')
            });
            
            // don't submit form **
            return false
        }
    })
})