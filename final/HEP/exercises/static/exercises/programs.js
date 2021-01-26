

programToggleButton = document.querySelector('.program-view')
programToggleButton.onclick = function(){
    
    items = Array.from(document.querySelectorAll('.program-item'))
    items.forEach(item => {
        item.classList.toggle('hide')
        if (item.classList.contains('hide')){
            exItems = Array.from(document.querySelectorAll(`.exercises${item.dataset.id}`))
            exItems.forEach(ex =>{
                ex.classList.add('hide')
            })
        }
        
    })
    
}

exercisePrograms = Array.from(document.querySelectorAll('.exerciseToggler'))
exercisePrograms.forEach(program => {
    
    program.addEventListener('click', (e) => {
        
        exercises = Array.from(document.querySelectorAll(`.exercises${program.dataset.id}`))
        exercises.forEach(exercise => {
            exercise.classList.toggle('hide')
        })
        
    }, {})
})


