// document.addEventListener('DOMConentLoaded', function(){
//     console.log('working')
// });

// select all edit and like buttons on page and configure functionality

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
    
    // GET request to server side
    const response = await fetch(`/posts/edit/${post_id}`)
    const data = await response.json()

    // display content via popup modul
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

    // display save button option
    savebtn = document.getElementById('save')
    savebtn.addEventListener('click',(event) => {
        console.log('working')
        event.preventDefault()
        const postContent ={
            content: document.getElementById('textitem').value
        }
        // server side PUT request if save button is clicked
        fetch(`/posts/save/${post_id}`, {
            method: 'PUT',
            body: JSON.stringify(postContent)
        })
        .then(response => console.log(response))
        document.body.removeChild(newDiv)
        // display updated post without having to reload entire page
        document.querySelector(`#content${post_id}`).innerHTML = `${postContent.content}`

        
    })

    // close edit post module option
    closebtn = document.getElementById('close')
    closebtn.addEventListener('click',() => {
        document.body.removeChild(newDiv)
    })

    
}

async function handleLike(post_id){

    // server side request for like count
    let response = await fetch(`/posts/like/${post_id}`)
    let json = await response.json()
    let likeCount = json.like_count.length
    
    currentDisplayedLikes = parseInt(document.querySelector(`.likecounter${post_id}`).innerHTML)
    // handle whether like or unlike option is appropriate to display
    if (likeCount > currentDisplayedLikes){
        document.querySelector(`.like${post_id}`).innerHTML = `👎`
    }
    else{
        document.querySelector(`.like${post_id}`).innerHTML= `👍`
    }
    // display new like count without page reload
    document.querySelector(`.likecounter${post_id}`).innerHTML = likeCount
   
}