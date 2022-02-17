function add_to_cart(item_id) {
    let csrfToken = Cookies.get('csrftoken')

    document.querySelector('#add_to_cart').onclick = function () {
        data = {
            Id: item_id
        }

        fetch('/api/cart/', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
        }).then(res => {
            console.log(res.status)
            if (res.status === 500) {
                alert('服务器错误')
                return
            }
            return res.json()
        }).then(json => {
            alert(json.detail)
        })
    }
} 