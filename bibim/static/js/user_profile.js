const postBtn = document.querySelector('.user-posts');
const materialsBtn = document.querySelector('.user-materials');
const commentsBtn = document.querySelector('.user-comments');

postBtn.addEventListener('click', Contents(postBtn.dataset.Username, 'posts'));
materialsBtn.addEventListener('click', Contents(materialsBtn.dataset.Username, 'materials'));
commentsBtn.addEventListener('click', Contents(commentsBtn.dataset.Username, 'comments'));

function Contents(username, view) {
    fetch(`/users/${username}/${view}`)
    .then(response => response.json())
    .then(contents => {
        contents.forEach(entry => {
            if (view == 'posts') {
                displayPosts(entry['author'], entry['date_posted'], entry['content'], entry['likes'])
            }
            else if (view == 'materials') {
                displayMaterials()
            }
            else if (view == 'comments') {
                displayComments()
            }
            else {
                return none
            }
        });
    })
}

function displayPosts(poster, date, title, content, profilePicture, likes) {
    // Create elements for the new post
    const postContainer = document.createElement('div');
    const postLink = document.createElement('a');
    const post = document.createElement('div');
    const postHeader = document.createElement('div');
    const profileImg = document.createElement('img');
    const postInfo = document.createElement('div');
    const postUser = document.createElement('div');
    const postDate = document.createElement('div');
    const postBody = document.createElement('div');
    const postTitle = document.createElement('h2');
    const postContent = document.createElement('p');
    const postFooter = document.createElement('div');
    const postLikes = document.createElement('div');
    
    // Add content to the new post elements
    profileImg.src = profilePicture;
    profileImg.alt = 'Profile Picture';
    postUser.textContent = poster;
    postDate.textContent = date;
    postTitle.textContent = title;
    postContent.textContent = content;
    postLikes.textContent = likes;
    
    // Add classes to the new post elements
    postContainer.classList.add('post-container');
    post.classList.add('post');
    postHeader.classList.add('post-header');
    profileImg.classList.add('profile-picture');
    postInfo.classList.add('post-info');
    postUser.classList.add('post-user');
    postDate.classList.add('post-date');
    postBody.classList.add('post-body');
    postTitle.classList.add('post-title');
    postContent.classList.add('post-content');
    postFooter.classList.add('post-footer');
    postLikes.classList.add('post-likes');
    
    // Append the new post elements to the post container div
    postContainer.appendChild(postLink);
    postLink.appendChild(post);
    post.appendChild(postHeader);
    postHeader.appendChild(profileImg);
    postHeader.appendChild(postInfo);
    postInfo.appendChild(postUser);
    postInfo.appendChild(postDate);
    post.appendChild(postBody);
    postBody.appendChild(postTitle);
    postBody.appendChild(postContent);
    post.appendChild(postFooter);
    postFooter.appendChild(postLikes);
    document.querySelector('.post-container').appendChild(postContainer);
  }
  