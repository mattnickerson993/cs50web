

programToggleButton = document.querySelector('.program-view')
programToggleButton.onclick = function(){
    console.log('working')
    items = Array.from(document.querySelectorAll('.program-item'))
    items.forEach(item => {
        item.classList.toggle('hide')
    })
    
}

exercisePrograms = Array.from(document.querySelectorAll('.exerciseToggler'))
exercisePrograms.forEach(program => {
    
    program.addEventListener('click', (e) => {
        console.log('working')
        exercises = Array.from(document.querySelectorAll(`.exercises${program.dataset.id}`))
        exercises.forEach(exercise => {
            exercise.classList.toggle('hide')
        })
        
    }, {})
})


// const programs = Array.from(document.querySelectorAll('.program-item'))
// programs.forEach(program => {
//     program.addEventListener('click', (e)=> getExercises(program.dataset.id, program),{once: true})
    
    
// })


// async function getExercises(id , programel){
    

//     let response = await fetch(`/exercise/programs/retrieve/${id}`)
//     let data = await response.json()
//     let newDiv = document.createElement('div')
//     newDiv.innerHTML =''
//     data.contents.forEach(exercise => {
//         newDiv.innerHTML+=`
//         <div class="">${exercise}</div>
//         `
//     })
//     programel.appendChild(newDiv)
    

// }
