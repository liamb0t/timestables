const messageCounter = document.querySelector('#message_count');
const count = messageCounter.dataset.count;

document.addEventListener('DOMContentLoaded', function() {
  get_notifications();
});

// change notification badge if new messages
function update_message_counter(count) {
  if (count > 0) {
    messageCounter.textContent = count;
    messageCounter.style.display = 'block'
  }
  else {
    messageCounter.style.display = 'none'
  }
}
  
function get_notifications() {
  let since = 0;
  let timer = 10000;
  setInterval(function() {
    fetch(`/notifications?since=${since}`)  
    .then(response => response.json())
    .then(data => {
      update_message_counter(data['unread_message_count']);
      if (data['notifications']) {
        if (since > 0) {
          const counter = document.querySelector('#notifications_count');
          const count = parseInt(counter.dataset.count);
          const new_count = count + data['notifications'].length;
          counter.innerHTML = new_count;
          counter.dataset.count = new_count;
        }
        data['notifications'].forEach(notification => {
          since = notification['timestamp'];
          display_notification(notification);
        });
      }
    })
  }, timer);
};

function load_notifications() {
  fetch(`/notifications`)
    .then(response => response.json())
    .then(data => {
      data['notifications'].forEach(notification => {
        display_notification(notification)
      });
    })
}

function display_notification(data) {
  notiContainer= document.querySelector('.notifications');
  notiDiv = document.createElement('div');
  const url = document.createElement('a');
  url.setAttribute('href', `/open_notification/${data.id}`);
  url.appendChild(notiDiv)
  const html = notificationHTML(data)
  notiDiv.innerHTML = html;
  notiContainer.insertAdjacentElement('afterbegin', url);
}

const notificationsBtn = document.querySelector('.notifications-link');

notificationsBtn.addEventListener('click', function() {
  const notificationsDiv = document.querySelector('.notifications');
  notificationsDiv.style.display = notificationsDiv.style.display === 'block' ? 'none' : 'block';
});

function notificationHTML(data) {
  const type = data['type']
  const user_data = data['user_data'];
  const sent_data = data['sent_data'];

  if (type === 'post_comment' || type === 'material_comment' || type === 'comment_reply') {
    return `${sent_data['author']} ${data['html']}: ${sent_data['content']}`
  }
  else {
    return `${sent_data['author']} ${data['html']} ${user_data['content']}`
  }
}