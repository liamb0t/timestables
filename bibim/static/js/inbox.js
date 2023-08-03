const conversations = document.querySelectorAll('.conversation');
const messageDisplay = document.querySelector('.message-display');
const header = document.querySelector('.inbox-header')
const headerUsername = document.querySelector('.header-username')
const headerImg = document.querySelector('.header-img')
const headerLastSeen =  document.querySelector('.header-lastseen')
const headerLink =  document.querySelector('.header-link')
const messageBorder = document.querySelector('.message-input-border')

window.onload = function(){
    messageDisplay.scrollTop = messageDisplay.scrollHeight;
};  

conversations.forEach(convo => {
    convo.addEventListener('click', function() {
        messageDisplay.innerHTML = '';
        messageDisplay.style.alignItems = 'normal';
        messageDisplay.style.justifyContent = 'flex-end';
        messageDisplay.style.display = 'block';
        header.style.display = 'flex';
        messageBorder.style.display = 'flex'

        const user = this.dataset.user;
        headerUsername.innerHTML = this.dataset.username;
        headerImg.src = `/static/pics/${this.dataset.img}`;
        const time = this.dataset.lastseen.split(" ")[0]
        const unit = this.dataset.lastseen.split(" ")[1]
        
        if (time < 5 && unit == 'm') {
            headerLastSeen.innerHTML = 'Active now'
        }
        else {
            headerLastSeen.innerHTML = `Active ${this.dataset.lastseen} ago`;
        }
       
        headerLink.href = `/users/${this.dataset.username}`;
        updateURL(convo)
        fetch(`get_messages/${this.dataset.user}`)
        .then(response => response.json())
        .then(data => {
            displayMessages(data['conversation'])
           
            header.style.borderBottom = '1px solid gainsboro';
        })
    })
});

function displayMessages(history) {
    history.forEach(msg => {
        if (msg['current_user'] != msg['sender']) {
            isRead(msg);
        }
        const messageDiv = document.createElement('div');
        const container = document.createElement('div')
        messageDiv.innerHTML = msg['sender'] + ': ' + msg['content'];
        if (msg['sender'] != msg['current_user']) {
            container.setAttribute('class', 'message-container')
            messageDiv.setAttribute('class', 'message')
        }
        else {
            container.setAttribute('class', 'message-sent-container')
            messageDiv.setAttribute('class', 'message-sent')
            
        }
        container.appendChild(messageDiv)
        messageDisplay.appendChild(container);
    });
    messageDisplay.scrollTop = messageDisplay.scrollHeight;
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

function isRead(message) {
    if (!message['read']) {
        console.log(message['read'])
        fetch(`/message/${message['id']}`, {
            method: 'POST',
            body: JSON.stringify({
                read: true
            })
        })
    }
}