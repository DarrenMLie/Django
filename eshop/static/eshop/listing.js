// script for listing.html **
document.addEventListener("DOMContentLoaded", () => {
    // cartforms onsubmit **
    document.querySelector('#cartform').onsubmit = () => {
        // get listing_id and amount **
        listing_id = document.querySelector('#listing_id').value
        amount = document.querySelector('#amount').value

        // post changes to view **
        fetch('/cart', {
            method: 'POST',
            body: JSON.stringify({
                listing_id: listing_id,
                amount: amount
            })
        })
        .then(response => response.json())
        .then(result => {
            // debugging **
            console.log(result);

            // update page elements **
            // change incart amount **
            document.querySelector('#incart').innerHTML = +document.querySelector('#incart').innerHTML + +amount
            // add message **
            if (amount > 0) document.querySelector('#message').innerHTML = '(Product added to cart)'
        });
        
        // don't submit form **
        return false
    }

    // commentform onsubmit **
    document.querySelector('#commentform').onsubmit = () => {
        // get listing_id and comment **
        listing_id = document.querySelector('#listing_id').value
        comment = document.querySelector('#comment').value

        // post changes to view **
        fetch(`/comment=${listing_id}`, { // id sent here instead of body **
            method: 'POST',
            body: JSON.stringify({
                comment: comment
            })
        })
        .then(response => response.json())
        .then(result => {
            // debugging **
            console.log(result);

            // update page elements **
            // empty textarea **
            document.querySelector('#comment').value = ''
            // update comment section **
            li = document.createElement('li')
            username = document.querySelector('#request_user').value
            li.innerHTML = `${username}: ${comment}`
            if (document.querySelector('#nocomment')) {
                document.querySelector('#commentlist').innerHTML = ''
                document.querySelector('#commentlist').append(li)
            } else {
                document.querySelector('#commentlist').append(li)
            }
        });
        
        // don't submit form **
        return false
    }
})