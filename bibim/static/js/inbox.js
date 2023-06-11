const conversations = document.querySelectorAll('.conversation');
const messageDisplay = document.querySelector('.message-display');


conversations.forEach(convo => {
    convo.addEventListener('click', function() {
        updateURL(convo)
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
        if (msg['sender'] != msg['current_user']) {
            messageDiv.setAttribute('class', 'message')
        }
        else {
            messageDiv.setAttribute('class', 'message-sent')
        }
        messageDisplay.appendChild(messageDiv);
    });
}

function updateURL(div) {
    const id = div.dataset.user;
    // Get the current URL
    const currentUrl = 'http://127.0.0.1:5000/inbox';

    // Add the GET parameter to the URL
    const newUrl = currentUrl + `?user=${id}`; // Replace 'param' and 'value' with your desired parameter name and value

    // Update the new URL
    history.pushState(null, null, newUrl);
}