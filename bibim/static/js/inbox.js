const conversations = document.querySelectorAll('.conversation');
const messageDisplay = document.querySelector('.message-display');


conversations.forEach(convo => {
    convo.addEventListener('click', function() {
        fetch(`get_messages/${this.dataset.user}`)
        .then(response => response.json())
        .then(data => {
            console.log(data)
            displayMessages(data['conversation'])
        })
    })
});

function displayMessages(history) {
    messageDisplay.innerHTML = '';
    history.forEach(msg => {
        const messageDiv = document.createElement('div');
        messageDiv.innerHTML = msg['sender'] + ':' + msg['content'];
        console.log(msg)
        if (msg['sender'] != msg['current_user']) {
            messageDiv.setAttribute('class', 'message')
        }
        else {
            messageDiv.setAttribute('class', 'message-sent')
        }
        messageDisplay.appendChild(messageDiv);
    });
}