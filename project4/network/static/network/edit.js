document.addEventListener('DOMConentLoaded', function(){
    console.log('working')
});

editbtns = document.querySelectorAll('.btn-edit')
likebtns = document.querySelectorAll('.likebtn')


editbtns.forEach(btn => {
    btn.onclick = function() {
        editPost(this.dataset.id)
    }
        

})

likebtns.forEach(btn => {
    btn.onclick = function(){
        handleLike(this.dataset.id)
    }
})






async function editPost(post_id){
    
    const response = await fetch(`/posts/edit/${post_id}`)
    const data = await response.json()
    console.log(data.content)

    const newDiv = document.createElement('div')
    newDiv.classList.add('popup')
    newDiv.innerHTML =`
    <div class="popupbody">
        <textarea class="text" id="textitem" rows="4" cols="50"> ${data.content}</textarea>
        <div class="popupbtns">
            <button type="button" id="save"class="btn btn-outline-primary">Save</button>
            <button type="button" id="close" class="btn btn-outline-dark mr-0">X</button>
        </div>
    </div>
    `
    
    document.body.appendChild(newDiv)

    savebtn = document.getElementById('save')
    savebtn.addEventListener('click',(event) => {
        console.log('working')
        event.preventDefault()
        const postContent ={
            content: document.getElementById('textitem').value
        }
    
        fetch(`/posts/save/${post_id}`, {
            method: 'PUT',
            body: JSON.stringify(postContent)
        })
        .then(response => console.log(response))
        document.body.removeChild(newDiv)
        document.querySelector(`#content${post_id}`).innerHTML = `${postContent.content}`

        
    })


    closebtn = document.getElementById('close')
    closebtn.addEventListener('click',() => {
        document.body.removeChild(newDiv)
    })

    
}

async function handleLike(post_id){

    let response = await fetch(`/posts/like/${post_id}`)
    let json = await response.json()
    let likeCount = json.like_count.length
    console.log(json)
    currentDisplayedLikes = parseInt(document.querySelector(`.likecounter${post_id}`).innerHTML)
    if (likeCount > currentDisplayedLikes){
        document.querySelector(`.like${post_id}`).innerHTML = `👎`
    }
    else{
        document.querySelector(`.like${post_id}`).innerHTML= `👍`
    }
    document.querySelector(`.likecounter${post_id}`).innerHTML = likeCount
   
}