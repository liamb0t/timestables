const links = document.querySelectorAll('.sidebar ul li a');

links.forEach((link) => {
  link.addEventListener('click', (event) => {
    // Remove the 'active' class from all links
    links.forEach((link) => {
      link.classList.remove('active');
    });

    // Add the 'active' class to the clicked link
    link.classList.add('active');

    // Store the active link information in localStorage
    localStorage.setItem('activeLink', link.getAttribute('href'));
  });
});

const sidebarOptions = document.querySelectorAll('.sidebar-option');
const materialsLink = document.getElementById('materials-link');

materialsLink.addEventListener('click', function() {
  sidebarOptions.forEach(elem => {
    if (elem.style.display === 'none' || elem.style.display === '') {
      elem.style.display = 'block';
    }
    else {
      elem.style.display = 'none';
    }
  });
})

// Check if there is an active link in localStorage
const activeLink = localStorage.getItem('activeLink');
if (activeLink) {
  const link = document.querySelector(`.sidebar ul li a[href="${activeLink}"]`);
  if (link) {
    link.classList.add('active');
  }
}

function handleSubmit(event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const textareaValue = formData.get('myTextarea');
  const parentId = formData.get('parent');
  console.log(parentId)
  const postId = this.dataset.postId;

  // Create the payload
  const payload = {
      textAreaData: textareaValue,
      parent_id: parentId
  };

  if (textareaValue != '') {
    // Send a POST request to the route using AJAX
    fetch(`/post/${postId}/comment`, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(comment => {
        // Create a new comment element and add it to the comments list
        const commentElement = document.createElement('div');
        commentElement.classList.add('comment-container');
        commentElement.setAttribute('id', `${comment['id']}`)
        commentElement.innerHTML = `
        <div>
            <img class="user-pic" src="/static/pics/${comment['pic']}" alt="User profile picture">
        </div>
        <div class="user-info">
            <div class="header">
                <div class="username">${comment["author"]}</div>
                ${comment.parent ? `<a href="/user/${comment['parent']}" style="color: rgb(53, 152, 157)">@${comment['parent']}</a>` : ''}
                <div class="comment">${comment["content"]}</div>
            </div>
            <div class="footer">
                <div class="date">${comment["date_posted"]}</div>
                ${comment["likes_count"] > 0 ? `<div class="date" id="like-counter-${comment["id"]} data-count="${comment["likes_count"]}" style="display: block">${comment["likes_count"]} likes_count</div>` : `<div class="date" id="like-counter-${comment["likes_count"]}" data-count="${comment["likes_count"]}" style="display: none;">${comment["likes_count"]} likes</div>`}
                <div class="reply-btn" data-comment-id="${comment["id"]}" data-author="${comment["author"]}" data-post-id="${postId}">Reply</div>
                <i class="fa fa-ellipsis" id="ellipsis-icon" onclick=displayOverlay(${comment['id']})></i>
            </div>
        </div>
        `;
        const commentsList = document.querySelector(`#post-comments-${postId}`);
        const firstElement = commentsList.firstChild;
        commentsList.insertBefore(commentElement, firstElement);
        // Clear the content of the comment form
        this.reset();
    });
    }
  }

function displayOverlay(id) {
  overlay.style.display = 'block'
  optionsDiv.style.display = 'block'
  handleDelete(id)
}

function handleDelete(id) {
  document.querySelector('.delete-form').addEventListener('submit', function(event) {
    event.preventDefault()
    fetch(`/comment/delete/${id}`, {
      method: 'POST',
      headers: {
      'Content-Type': 'application/json'
      },
  })
      .then(response => response.json())
      .then(function() {
        comment.innerHTML = ''
        document.querySelector('.modal-dialog').style.display = 'none'
        document.querySelector('overlay').style.display = 'none'
        document.getElementById('deleteModal').classList.remove('show')
      })
  })
  
}

function updatePost() {
  fetch(`/post/${postId}/edit`, {
    method: 'GET',
})
  .then(response => response.json())
  .then(data => {
    document.querySelector(`#post-content-${data['id']}`).innerHTML = data['content'];
  })
}