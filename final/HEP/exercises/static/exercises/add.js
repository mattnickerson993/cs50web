function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


const addBtn = document.querySelector('.add')

addBtn.onclick = () => {
    getPrograms()
}

async function getPrograms(){
    let response = await fetch(`/exercise/add`)
    let data = await response.json()
    console.log(data)
    displayPrograms(data)
    
}

function displayPrograms(programs){
    const dropdown = document.querySelector('.dropdown')
    const dropdownMenu = document.querySelector('.dropdown-menu')
    
    dropdownMenu.innerHTML = ''
    programs.forEach(program => {
        dropdownMenu.innerHTML += `
        <a data-programId="${program.id}" onclick="saveToProgram(${dropdownMenu.dataset.exercise}, ${program.id})"class="dropdown-item" href="#">${program.title}</a>
        `
    })
    dropdown.style.display = "block"
}

async function saveToProgram(exid, id){
    const response = fetch(`/exercise/add/save/${id}/${exid}`,{
        method: 'PUT',
        headers:{
            'X-CSRFToken':csrftoken
        },
        body: JSON.stringify({
            programId: id,
            exerciseId: exid

        })
    }
    )
    console.log(`You click on program with id of ${id}`)
}