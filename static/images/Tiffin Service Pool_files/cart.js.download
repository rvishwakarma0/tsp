var updateBtns = document.getElementsByClassName('update-cart')

for(i=0; i<updateBtns.length;i++){
    updateBtns[i].addEventListener('click',function(){
        var tiffinId = this.dataset.tiffin
        var action = this.dataset.action
        console.log('tiffinId:',tiffinId,'action:',action)

        console.log('user:',user)
        if (user === 'AnonymousUser') {
            addCookieItem(tiffinId, action)
        }
        else{
            UpdateUserOrder(tiffinId, action)
        }
    })
}

function addCookieItem(tiffinId, action){
    console.log("not logged in")
    if(action == 'add'){
        if(cart[tiffinId]== undefined){
            cart[tiffinId]={'quantity':1}
        }
        else{
            cart[tiffinId]['quantity'] +=1
        }
    }
    if(action == 'remove'){
        cart[tiffinId]['quantity'] -= 1
        if(cart[tiffinId]['quantity']<=0){
            console.log('item should be deleted')
            delete cart[tiffinId];
        }
    }
    console.log('cart:',cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
    location.reload()
}

function UpdateUserOrder(tiffinId, action){
    console.log('User is logged in, sending data... ')
    console.log(tiffinId)

    var url='/update_item/'
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'tiffinId':tiffinId, 'action':action})
    })

    .then((response)=>{
        return response.json()
    })

    .then((data)=>{
        console.log('data', data)
        location.reload()
    })
}