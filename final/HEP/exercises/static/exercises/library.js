
// in case user accesses via back button

document.addEventListener('DOMContentLoaded', () => {
    startingExerciseVal = document.querySelector('.libary-input')
    getExercises(startingExerciseVal)

})

// handle current page tracking
let currentPage = 0;
prevButton = document.getElementById('prev')
nextButton = document.getElementById('next')

// handle input box and set getExercises function on change.
let libraryInput= document.querySelector('.library-input')


libraryInput.onkeyup = (e) => {
    let {value} = e.target
    // avoid changes on backspace
    if (e.keyCode === 8){
        return
    }
    getExercises(value)

}

prevButton.onclick = () =>{
    currentPage -= 1
    getExercises(libraryInput.value)
}

nextButton.onclick = () =>{
    currentPage += 1
    getExercises(libraryInput.value)
    
}






async function getExercises(val){
    
    cardContainer = document.querySelector('.card-container')
    cardContainer.innerHTML =''
    
    const response = await fetch(`/exercise/library/retrieve/${val}`)
    const data = await response.json()
    // handle pagination
    if(data && data.length > 0){
        document.getElementById('exercise-nav').style.display = 'block'
    }
    else{
        document.getElementById('exercise-nav').style.display = 'none'
    }

    
    let numExercises = data.length
    let exPerPage = 6;
    let minPage = exPerPage * currentPage
    let maxPage = minPage + exPerPage - 1
    let pages = Math.ceil(numExercises/exPerPage);
    
    // handle button display 
    prevButton.disabled = currentPage > 0 ? false: true
    nextButton.disabled = currentPage < pages - 1 ? false: true
    // handle display of exercises
    
    
    data.forEach( (exercise, index) => {
        
        if (index>= minPage && index <= maxPage){
            cardContainer.innerHTML +=`
            <div id="indy-card" class="card m-4" style="max-width: 18rem;">
                <img class="card-img-top" src=${exercise.image} alt="Card image cap">
                <div class="card-body">
                    <h5 class="card-title"><a href="${parseInt(exercise.id)}">${exercise.title}</a></h5>
                    <p class="card-text">${exercise.description}</p>  
                </div>
                <div class="card-footer d-flex justify-content-between">
                    <small class="align-self-center text-muted">${exercise.author}</small>
                    <img style="max-width: 50px; max-height: 50px;"class="profile-img rounded-circle img-fluid" src="${exercise.author_pic}">
                </div>
            </div>
        `
        }
        

        
    })
}
