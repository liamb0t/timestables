let page = 1;
const postField = document.querySelector('#content');
const submitPostBtn = document.querySelector('#submit');
const overlay = document.querySelector('.overlay');
const popupContainer = document.querySelector('.likes-popup');

function paginate(id, btn) {
    const comments = document.querySelectorAll(`#post-comments-${id} .comment-container-hidden`)
    comments.forEach(comment => {
        comment.classList.toggle('comment-container')
    });
    btn.style.display = 'none';
}   

function handleReply(data) {
    const commentId = data["comment_id"];
    const author = data["author"];
    const postId = data["post_id"];
    const commentTextArea = document.getElementById(`post-textarea-${postId}`);
    const hiddenField = document.getElementById(`post-hidden-${postId}`);
    commentTextArea.value = '';
    commentTextArea.value += '@' + author + ' ';
    commentTextArea.focus();
    hiddenField.value = commentId;
}

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

document.addEventListener('DOMContentLoaded', () =>{
    load();
    
    const replyBtns = document.querySelectorAll('button');
    console.log(replyBtns)  
    replyBtns.forEach(btn => {
        btn.addEventListener('click', handleReply);
    });
});

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
    });

    likesText.textContent = `${post['likes']} likes`;
   
    const likeButton = document.createElement('i');
    likeButton.setAttribute('class', 'fa-regular fa-heart');
    likeButton.setAttribute('id', `like-counter-icon-${post['id']}`);
    likeButton.dataset.post_id = post['id'];
    if (post['liked']) {
        likeButton.style.color = 'red';
        likeButton.setAttribute('class', 'fa-solid fa-heart');
    }

    likesText.setAttribute('id', `like-counter-${post['id']}`);
    likesText.dataset.count = post['likes'];
    
    likes.append(likeButton);
    likes.appendChild(likesText);
   
    //add function to like button to handle likes on click 
    likeButton.addEventListener('click', handleLikes);
    
    // Create the footer element
    const footer = document.createElement('div');
    footer.classList.add('post-footer');
    
    // Create the comments element **********

    const comments = document.createElement('div');
    comments.classList.add('comments');
    comments.setAttribute('id', `post-comments-${post["id"]}`);
    
    if (post["comments"]) {
        let count = 0;
        let paginated = false;
        const limit = 5;

        post["comments"].forEach(comment => {
            count += 1;
            const commentContainer = document.createElement('div');
            commentContainer.classList.add('comment-container');

            if (count > limit) {
                commentContainer.setAttribute('class', 'comment-container-hidden');
                if (!paginated) {
                    paginated = true;
                    const container = document.createElement('div');
                    container.setAttribute('class', 'paginate-icon-container')
                    const paginateBtn = document.createElement('btn');
                    paginateBtn.setAttribute('class', "fa-regular fa-plus")
                    container.appendChild(paginateBtn)
                    comments.appendChild(container);
                    paginateBtn.addEventListener('click', function() {
                        paginate(post['id'], this);
                    })
                }
            }   
              
            const userPic = document.createElement('img');
            userPic.classList.add('user-pic');
            userPic.src = "/static/pics/default.jpg";
            userPic.alt = "User profile picture";
            commentContainer.appendChild(userPic);

            const userInfo = document.createElement('div');
            userInfo.classList.add('user-info');

            const header = document.createElement('div');
            header.classList.add('header');

            const username = document.createElement('div');
            username.classList.add('username');
            username.textContent = comment["author"];
            header.appendChild(username);

            if (comment['parent']) {
                const parentLink = document.createElement('a');
                parentLink.href = `user/${comment['parent']}`
                parentLink.style.color = "rgb(53, 152, 157)";
                parentLink.textContent = `@${comment['parent']}`;
                header.appendChild(parentLink);
            }

            const commentContent = document.createElement('div');
            commentContent.classList.add('comment');
            commentContent.textContent = comment["content"];
            header.appendChild(commentContent);

            userInfo.appendChild(header);

            const footer = document.createElement('div');
            footer.classList.add('footer');

            const date = document.createElement('div');
            date.classList.add('date');
            date.textContent = comment["date_posted"];
            footer.appendChild(date);

            //likes are not appearing yet cause haven't added like functionality to posts yet

            if (comment["likes_count"] > 0) {
                const likeCounter = document.createElement('div');
                likeCounter.classList.add('date');
                likeCounter.id = `like-counter-${comment["id"]}`;
                likeCounter.dataset.count = comment["likes_count"];
                likeCounter.style.display = "block";
                likeCounter.textContent = `${comment["likes_count"]} likes`;
                footer.appendChild(likeCounter);
            } else {
                const likeCounter = document.createElement('div');
                likeCounter.classList.add('date');
                likeCounter.id = `like-counter-${comment["id"]}`;
                likeCounter.dataset.count = comment["likes_count"];
                likeCounter.style.display = "none";
                likeCounter.textContent = `${comment["likes_count"]} likes`;
                footer.appendChild(likeCounter);
            }

            const replyBtn = document.createElement('div');
            replyBtn.classList.add('reply-btn');
            replyBtn.textContent = "Reply";
            replyBtn.addEventListener('click', function() {
                handleReply({ author: comment["author"], comment_id: comment["id"], post_id: post["id"] });
            });
            footer.appendChild(replyBtn);

            userInfo.appendChild(footer);
    
            commentContainer.appendChild(userInfo);

            comments.appendChild(commentContainer);

            const replies = document.createElement('div');
            replies.setAttribute('class', 'comment-replies');

            replies.style.display = 'none';

            
            if (comment["replies"].length > 0) {
                const showRepliesDiv = document.createElement('div');
                showRepliesDiv.innerHTML = `
                    <btn class="show-replies-btn" id="show-replies-btn-${comment['id']}" style="display: block" data-comment-id="${comment['id']}" data-replies-count="${comment['replies_count']}">&mdash;&mdash; View replies (${comment['replies_count']})</btn>`
                userInfo.append(showRepliesDiv)

                showRepliesDiv.addEventListener('click', function() {
                    replies.style.display = replies.style.display === 'block' ? 'none' : 'block';
                    this.children[0].innerHTML = replies.style.display === 'block' ? '&mdash;&mdash; Hide replies' : `&mdash;&mdash; View replies (${comment['replies_count']})`;
                })

                comment["replies"].forEach(reply => {
                    const replyDiv = document.createElement('div');
                    const html = `
                        <div class="comment-container">
                        <div>
                            <img class="user-pic" src="/static/pics/default.jpg" alt="User profile picture">
                        </div>
                        <div class="user-info">
                            <div class="header">
                            <div class="username">${reply["author"]}</div>
                            
                            <div class="comment">${reply["content"]}</div>
                            </div>
                                <div class="footer">
                                <div class="date">${reply["date_posted"]}</div>
                                
                                <div class="date" id="like-counter-${reply["id"]}" data-count="${reply["likes_count"]}" style="display: block">${reply["likes_count"]} likes</div>
                                
                                <div class="date" id="like-counter-${reply["id"]}" data-count="${reply["likes_count"]}" style="display: none;">${reply["likes_count"]} likes</div>
                                <div onclick="handleReply({ author: '${reply["author"]}', comment_id: ${reply["id"]}, post_id: ${post["id"]} })" class="reply-btn" data-comment-id="${reply['id']}" data-author="${reply['author']}">Reply</div>
                            </div> 
                        </div>
                        <div class="like-btn">
                            <div class="like-icon">
                            <i id="material-comment-like-icon-${reply["id"]}" class="fa-regular fa-heart" data-reply-id="${reply['id']}"></i>
                            </div>
                        </div>
                        </div>    
                    `;
                    replyDiv.innerHTML = html;
                    replies.appendChild(replyDiv);
                });
                userInfo.appendChild(replies)
            }

            });
        }
    
    
    // Create the comment container element
    
    
    // Create the form element
    const commentForm = document.createElement('form');
    commentForm.setAttribute('class', 'comment-form');
    commentForm.dataset.postId = post["id"];
    commentForm.addEventListener('submit', handleSubmit);

    const hiddenField = document.createElement('input');
    hiddenField.setAttribute('id', `post-hidden-${post.id}`);
    hiddenField.type = 'hidden';
    hiddenField.name = 'parent';
    hiddenField.value = '';
    commentForm.appendChild(hiddenField);

    
    // Create the textarea element
    const commentTextArea = document.createElement('textarea');
    commentTextArea.placeholder = 'Add a comment...';
    commentTextArea.setAttribute('name', 'myTextarea');
    commentTextArea.setAttribute('id', `post-textarea-${post.id}`);
    commentTextArea.setAttribute('class', 'lounge-comment-field');

    const submitBtn = document.createElement('button');
    submitBtn.type = 'submit';
    submitBtn.textContent = 'Post';
    submitBtn.style.display = 'none';
    submitBtn.setAttribute('class', 'post-comments-button')

    commentTextArea.addEventListener('input', function() {
        const value = this.value.trim();

        if (value === '') {
            submitBtn.style.display = 'none';
        }
        else {
            submitBtn.style.display = 'block';
        }
    })

   
    
    // Append the submit button to the form
    commentForm.appendChild(commentTextArea);
    commentForm.appendChild(submitBtn);
   
    
    // Append the form element to the comment container element
    comments.appendChild(commentForm);

    
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
