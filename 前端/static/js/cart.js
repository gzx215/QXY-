function remove_cart(item_id) {
    fetch(`/api/cart/${item_id}`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
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
        document.querySelector(`#tr_${item_id}`).remove()
    })
} 