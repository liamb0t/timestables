const messageCounter = document.querySelector('#message_count');
const count = messageCounter.dataset.count;

document.addEventListener('DOMContentLoaded', function() {
  get_notifications()
  .then(since => {
    poller(since)
  })
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

function get_notifications(timestamp) {
  return new Promise((resolve, reject) => {
    let since = timestamp;
    fetch(`/notifications?since=${since}`)
      .then(response => response.json())
      .then(data => {
        update_message_counter(data['unread_message_count']);
        if (data['notifications']) {
          data['notifications'].forEach(notification => {
            if (notification) {
              since = notification['timestamp'];
              display_notification(notification);
            }
          });
        }
        resolve(since); // Resolve the Promise with the updated value of `since`
      })
      .catch(error => {
        reject(error); // Reject the Promise if there's an error
      });
  });
}

function updateNotifCount(n) {
  const counter = document.querySelector('#notifications_count');
  let count = parseInt(counter.dataset.count);

  if (!n['read']) {
    count += 1;
   
  }

  counter.dataset.count = count;
  counter.innerHTML = counter.dataset.count;
}


function poller(timestamp) {
  let timer = 60000; 
  let since = timestamp;
  setInterval(function() {
    get_notifications(since)
    .then(updatedSince => {
      since = updatedSince;
    })
  }, timer);
};

function display_notification(data) {
  notiContainer = document.querySelector('.notifications');
  notiDiv = document.createElement('div');
  const url = document.createElement('a');
  url.setAttribute('href', data['url']);
  url.appendChild(notiDiv)
  const html = notificationHTML(data)
  notiDiv.innerHTML = html;
  notiContainer.insertAdjacentElement('afterbegin', url);

  notiDiv.addEventListener('click', function() {
    if (!data['read']) {
      isRead(data['id']);
    }
  })
 
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

function isRead(notification_id) {
  fetch(`/open_notification/${notification_id}`, {
      method: 'POST',
      body: JSON.stringify({
          read: true
      })
  })
}