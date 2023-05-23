function handleSubmit(event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const textareaValue = formData.get('myTextarea');
  const parentId = formData.get('parentId');
  const postId = this.dataset.postId;

  // Create the payload
  const payload = {
      textAreaData: textareaValue,
      parent_id: parentId
  };

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
      commentElement.innerHTML = `
        <div>
            <img class="user-pic" src="/static/pics/default.jpg" alt="User profile picture">
        </div>
        <div class="user-info">
            <div class="header">
                <div class="username">${comment["author"]}</div>
                ${comment.parent ? `<a href="${url_for('users.user_profile', username=comment.parent)}" style="color: rgb(53, 152, 157)">@${comment.parent}</a>` : ''}
                <div class="comment">${comment["content"]}</div>
            </div>
            <div class="footer">
                <div class="date">${comment["date_posted"]}</div>
                ${comment["likes_count"] > 0 ? `<div class="date" id="like-counter-${comment["id"]} data-count="${comment["likes_count"]}" style="display: block">${comment["likes_count"]} likes_count</div>` : `<div class="date" id="like-counter-${comment["likes_count"]}" data-count="${comment["likes_count"]}" style="display: none;">${comment["likes_count"]} likes</div>`}
                <div class="reply-btn" data-comment-id="${comment["id"]}" data-author="${comment["author"]}" data-post-id="${postId}">Reply</div>
            </div>
        </div>
      `;
      const commentsList = document.querySelector(`#post-comments-${postId}`);
      commentsList.appendChild(commentElement);
      // Clear the content of the comment form
      this.reset();
  });
}