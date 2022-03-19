var update_btns = document.getElementsByClassName('update-cart')

for(var i=0; i<update_btns.length; i++){
    update_btns[i].addEventListener('click', function(){
        var id = this.dataset.item
        var action = this.dataset.action
        console.log('Item : t ', id, ' action : ', action)
        AddToCart(id, action)
    })
}

function AddToCart(id, action){
    console.log("Updating cart")
    var url = '/update-cart/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body:JSON.stringify({
            'item': id, 'action': action
        })
    })
        .then((response) =>{
            return response.text()
            })
        .then((data) =>{
            console.log('data : ', data)
            })
}