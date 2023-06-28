const editBtn = document.querySelector('#ellipsis-icon')
const overlay = document.querySelector('.overlay');
const optionsDiv = document.querySelector('.options-popup');
const editor = document.querySelector('.post-editor')
const optionsDivSecondary = document.querySelector('.options-popup-secondary');

document.addEventListener('DOMContentLoaded', function() {
    optionsDiv.style.display = 'none'
    editBtn.addEventListener('click', function() {
        overlay.style.display = 'block'
        optionsDivSecondary.style.display = 'block'
    })
})

document.querySelector('.delete-btn').addEventListener('click', function() {
    overlay.style.display = 'none'
    optionsDivSecondary.style.display = 'none'
})

overlay.addEventListener('click', function() {
    optionsDivSecondary.style.display = 'none'
    overlay.style.display = 'none'
})

