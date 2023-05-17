function handleSubmit(event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const textareaValue = formData.get('myTextarea');

  // Create the payload
  const payload = {
      textAreaData: textareaValue
  };

  // Send a POST request to the route using AJAX
  fetch(`/post/${this.dataset.postId}/comment`, {
      method: 'POST',
      headers: {
      'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
  })
  .then(response => response.json())
  .then(comment => {
      // Create a new comment element and add it to the comments list
      const commentElement = document.createElement('li');
      commentElement.classList.add('comment');
      commentElement.innerHTML = `
          <a href="/users/${comment.author}">${comment.author}</a>
          <span>${comment.content}</span>
          <small>${comment.date_posted}</small>
      `;
      const commentsList = document.querySelector('.comments-list');
      commentsList.appendChild(commentElement);
      // Clear the content of the comment form
      this.reset();
  });
}