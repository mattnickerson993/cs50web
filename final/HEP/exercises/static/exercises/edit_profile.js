updateProfileForm = document.querySelector('.update-profile')


document.getElementById('edit-btn').addEventListener('click', () => {
        updateProfileForm.style.display = "block"
})

document.getElementById('close-profile-button').addEventListener('click', () => {
    updateProfileForm.style.display = "none"
})

