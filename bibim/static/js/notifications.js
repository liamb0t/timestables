const messageCounter = document.querySelector('#message_count');
const count = messageCounter.dataset.count;
const notificationDiv = document.querySelector('.notification');

document.addEventListener('DOMContentLoaded', function() {
  get_notifications();
});

// change notification badge if new messages
function update_message_counter(count) {
  if (count > 0) {
    messageCounter.textContent = count;
    notificationDiv.classList.add('new');
  }
  else {
    notificationDiv.classList.remove('new');
  }
}
  
function get_notifications() {
  const since = 0;
  setInterval(function() {
    fetch(`/notifications?since=${since}`)
    .then(response => response.json())
    .then(data => {
      console.log(data)
      data.forEach(notification => {
        if (notification['name'] == "unread_message_count") {
          update_message_counter(notification['data']);
        }
      });
    })
  }, 10000);
};

