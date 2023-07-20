const goingBtn = document.querySelector('.create-btn')
goingBtn.addEventListener('click', function() {
    handleGoing(this.dataset.id)
})


function handleGoing(id) {
    const meeting_id = id
    fetch(`/going/${meeting_id}`)  
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if (data['going']) {
            goingBtn.innerHTML = 'Going'
        }
        else {
            goingBtn.innerHTML = 'Not going'
        }
    })
}