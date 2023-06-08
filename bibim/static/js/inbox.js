const conversations = document.querySelectorAll('.conversation');
const messageDisplay = document.querySelector('message-display');

conversations.forEach(convo => {
    convo.addEventListener('click', function() {
        fetch(`get_messages/${this.dataset.user}`)
        .then(response => response.json())
        .then(data => {
            displayMessages(data['conversation'])
        })
    })
});

function displayMessages(history) {
    history.forEach(msg => {
       console.log(msg)
    });
}