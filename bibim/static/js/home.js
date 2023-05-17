let page = 1;
const postField = document.querySelector('#content');
const submitPostBtn = document.querySelector('#submit');
const overlay = document.querySelector('.overlay');
const popupContainer = document.querySelector('.likes-popup');

overlay.addEventListener('click', function() {
    overlay.style.display = 'none';
    popupContainer.style.display = 'none';
    document.body.classList.remove("body-no-scroll");
})

const likersDiv = document.createElement('div');
likersDiv.setAttribute('class', 'likers-div');

document.querySelectorAll('.like-counter').forEach(counter => {
    counter.addEventListener('click', function() {
        createLikesPopup()
    })
});

document.addEventListener('DOMContentLoaded', load);

window.onscroll = () => {
    if (Math.ceil(window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
        load();
    }
}

function load() {

    const current_page = page;
    page += 1;

    fetch(`posts/${current_page}`)
    .then(response => response.json())
    .then(data => {
        data['posts'].forEach(post => {
            add_post(post);
            console.log(post)
        });
    })
}

function handleLikes() {
    const post_id = this.dataset.post_id;
    const icon = document.getElementById(`like-counter-icon-${post_id}`);
    const counter = document.getElementById(`like-counter-${post_id}`);
    let count = parseInt(counter.dataset.count);

    fetch(`like-post/${post_id}`)
    .then(response => response.json())
    .then(data => {
        if (data['liked']) {
            counter.innerHTML = `${count + 1} likes`;
            counter.dataset.count = count + 1;
            icon.setAttribute('class', 'fa-solid fa-heart');
            icon.style.color = 'red'
        }
        else {
            counter.innerHTML = `${count - 1} likes`;
            counter.dataset.count = count - 1;
            icon.setAttribute('class', 'fa-regular fa-heart');
            icon.style.color = 'black'
        }
    })
}

function add_post(post) {
    // Get the container for the posts
    const postContainer = document.querySelector('.posts');
    postContainer.style.minHeight = '100vh';
    
    // Create a new post element
    const newPost = document.createElement('div');
    newPost.classList.add('post');
    
    // Create the header element
    const header = document.createElement('div');
    header.classList.add('post-header');

    // Create the profile picture element
    const profilePic = document.createElement('img');
    profilePic.src = `static/pics/${post['profile_pic']}`;
    profilePic.classList.add('post-profile-pic');
    
    header.insertBefore(profilePic, header.firstChild);
    
    // Create the author link and username element
    const authorLink = document.createElement('a');
    authorLink.href = `/users/${post['author']}`;
    
    const username = document.createElement('h2');
    username.classList.add('post-username');
    username.textContent = post['author'];
    
    authorLink.appendChild(username);
    header.appendChild(authorLink);

    // Create span element 
    const span = document.createElement('span');
    span.classList.add('post-span');
    span.innerHTML = '&#8226;'
    header.appendChild(span);
    
    // Create the date posted element
    const datePosted = document.createElement('p');
    datePosted.classList.add('post-date');
    datePosted.textContent = post['date_posted'];
    header.appendChild(datePosted);
    
    // Create the content element
    const content = document.createElement('div');
    content.classList.add('post-content');
    
    const contentText = document.createElement('p');
    contentText.textContent = post['content'];
    content.appendChild(contentText);

    
    // Create likes elements
    const likes = document.createElement('div');
    likes.classList.add('post-likes');
    const likesText = document.createElement('p');
    likesText.setAttribute('class', 'like-counter');

    // Displays the pop up for likers of a post 
    likesText.addEventListener('click', function() {
        const overlay = document.querySelector('.overlay');
        popupContainer.innerHTML = '';
        const header = document.createElement('h3');
        header.innerHTML = 'Likes';
        popupContainer.appendChild(header);
        post["likers"].forEach(liker => {
            createLikesPopup(liker); 
        });
        popupContainer.style.display = 'block';
        overlay.style.display = 'block';
        document.body.classList.add("body-no-scroll");
    })

    likesText.textContent = `${post['likes']} likes`;
   
    const likeButton = document.createElement('icon');
    likeButton.setAttribute('class', 'fa-regular fa-heart');
    likeButton.setAttribute('id', `like-counter-icon-${post['id']}`);
    likeButton.dataset.post_id = post['id'];
    if (post['liked']) {
        likeButton.style.color = 'red';
        likeButton.setAttribute('class', 'fa-solid fa-heart');
    }

    likesText.setAttribute('id', `like-counter-${post['id']}`);
    likesText.dataset.count = post['likes'];
    
    likes.append(likeButton)
    likes.appendChild(likesText);
   
    //add function to like button to handle likes on click 
    likeButton.addEventListener('click', handleLikes)
    
    // Create the footer element
    const footer = document.createElement('div');
    footer.classList.add('post-footer');
    
    // Create the comments element
    const comments = document.createElement('div');
    comments.classList.add('post-comments');
    
    // Create the comment container element
    const commentContainer = document.createElement('div');
    commentContainer.classList.add('comment-container');

    // Create comment list container
    const commentsList = document.createElement('ul');
    commentsList.classList.add('comments-list');
    comments.appendChild(commentsList);
    
    // Create the form element
    const commentForm = document.createElement('form');
    commentForm.setAttribute('class', 'comment-form');
    commentForm.dataset.postId = post["id"]
    commentForm.addEventListener('submit', handleSubmit);
    
    // Create the textarea element
    const commentTextArea = document.createElement('textarea');
    commentTextArea.placeholder = 'Add a comment...';
    commentTextArea.setAttribute('name', 'myTextarea');

    const submitBtn = document.createElement('button');
    submitBtn.type = 'submit';
    submitBtn.textContent = 'Submit';
    
    // Append the submit button to the form
    commentForm.appendChild(commentTextArea);
    commentForm.appendChild(submitBtn);
    
    // Append the form element to the comment container element
    commentContainer.appendChild(commentForm);
    
    // Append the comment container element to the comments element
    comments.appendChild(commentContainer);
    
    // Append the header, content, likes, and footer elements to the new post element
    newPost.appendChild(header);
    newPost.appendChild(content);
    newPost.appendChild(likes);
    newPost.appendChild(footer);
    
    // Append the comments element to the footer element
    footer.appendChild(comments);
    
    // Append the new post element to the post container
    postContainer.appendChild(newPost);
    
}

// Function to create the likes popup
function createLikesPopup(user) {
  // Create the main container div

  // Create the content div
  const contentDiv = document.createElement('div');
  contentDiv.classList.add('likes-content');

  // Create the user list
  const userList = document.createElement('ul');
  userList.classList.add('user-list');

  // Create a sample user list item
  const userItem = document.createElement('li');

  // Create the user info container
  const userInfo = document.createElement('div');
  userInfo.classList.add('user-info');

  // Create the link to the user profile
  const userProfileLink = document.createElement('a');
  userProfileLink.href = `/users/${user["username"]}`;

  // Create the user profile picture
  const userProfileImg = document.createElement('img');
  userProfileImg.src =  `static/pics/${user['profile_pic']}`;
  userProfileImg.alt = 'User Profile Picture';

  // Create the username span
  const usernameSpan = document.createElement('span');
  usernameSpan.classList.add('username');
  usernameSpan.textContent = user["username"];

  // Create the follow button
  const followButton = document.createElement('button');
  followButton.classList.add('follow-button');
  followButton.textContent = 'Follow';

  // Append the elements together
  userProfileLink.appendChild(userProfileImg);
  userProfileLink.appendChild(usernameSpan);
  userInfo.appendChild(userProfileLink);
  userInfo.appendChild(followButton);
  userItem.appendChild(userInfo);
  userList.appendChild(userItem);
  contentDiv.appendChild(userList);
  popupContainer.appendChild(contentDiv);

  // Append the likes popup to the document body
  document.body.appendChild(popupContainer);
}

// Call the function to create the likes popup
