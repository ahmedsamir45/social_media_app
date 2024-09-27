
document.addEventListener('DOMContentLoaded', function() {
    const posts = document.querySelectorAll('.post');
    const commentForms = document.querySelectorAll('.comment-form');

    posts.forEach(post => {
        const likeButton = post.querySelector('.btnLike');
        const dislikeButton = post.querySelector('.btnDislike');
        const commentButton = post.querySelector('.btnComment');
        const commentsSection = post.querySelector('.comments');

        likeButton.addEventListener('click', function() {
            handleReaction(this, 'like', dislikeButton);
        });

        dislikeButton.addEventListener('click', function() {
            handleReaction(this, 'dislike', likeButton);
        });

        commentButton.addEventListener('click', function() {
            commentsSection.classList.toggle('active');
        });
    });

    function handleReaction(button, action, oppositeButton) {
        const postId = button.dataset.postId;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
        // Optimistic UI update
        const currentCount = parseInt(button.textContent.trim().split(' ')[1] || '0');
        const newCount = button.classList.contains(`${action}d`) ? currentCount - 1 : currentCount + 1;
        updateButtonState(button, newCount, !button.classList.contains(`${action}d`), action);
    
        if (oppositeButton.classList.contains(action === 'like' ? 'disliked' : 'liked')) {
            const oppositeCount = parseInt(oppositeButton.textContent.trim().split(' ')[1] || '0');
            updateButtonState(oppositeButton, oppositeCount - 1, false, action === 'like' ? 'dislike' : 'like');
        }
    
        // Disable the button to prevent rapid clicks
        button.disabled = true;
    
        fetch(`/api/${action}/${postId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update with actual server data
                updateButtonState(button, data.count, data.liked !== undefined ? data.liked : false, action);
                
                // Define oppositeAction based on current action
                const oppositeAction = action === 'like' ? 'dislike' : 'like';
                updateButtonState(oppositeButton, data[`${oppositeAction}_count`] || "0", false, oppositeAction);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Revert optimistic update on error
            updateButtonState(button, currentCount, !button.classList.contains(`${action}d`), action);
        })
        .finally(() => {
            // Re-enable the button after the response
            button.disabled = false;
        });
    }

    function updateButtonState(button, count, isActive, action) {
        const icon = button.querySelector('.bi');
        
        button.innerHTML = `<i class="bi fa-${isActive ? 'solid' : 'regular'} fa-thumbs-${action === 'like' ? 'up' : 'down'} i-${action}"></i> ${count}`;
        
        if (isActive) {
            button.classList.add(`${action}d`);
            icon.classList.add(action === 'like' ? 'text-primary' : 'text-danger');
        } else {
            button.classList.remove(`${action}d`);
            icon.classList.remove(action === 'like' ? 'text-primary' : 'text-danger');
        }
    }

    // Comment functionality
    commentForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const postId = this.dataset.postId;
            const contentInput = this.querySelector('input[name="content"]');
            const content = contentInput.value.trim();

            if (content) {
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

                fetch(`/api/add_comment/${postId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': csrfToken
                    },
                    body: `content=${encodeURIComponent(content)}`
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Create new comment element
                        const newComment = document.createElement('div');
                        newComment.className = 'comment';
                        newComment.innerHTML = `
                            <span>
                                <img src="${data.image || "/static/globalproject/imgs/usr.jpg"}" alt="">
                                <span>
                                    <a href="/usrinfo/${data.user_id}/">${data.username}</a>
                                </span>
                            </span>
                            <p>${data.content}</p>
                        `;

                        // Add new comment to the comments section
                        const commentsSection = document.querySelector(`#comments-${postId}`);
                        const firstComment = commentsSection.querySelector('.comment');
                        if (firstComment) {
                            commentsSection.insertBefore(newComment, firstComment);
                        } else {
                            commentsSection.appendChild(newComment);
                        }

                        // Clear input field
                        contentInput.value = '';

                        // Update comment count
                        const commentButton = `${data.count_comment}`
                        if (commentButton) {
                            const commentCount = parseInt(commentButton.textContent.trim().split(' ')[1] || '0');
                            commentButton.innerHTML = `<i class="bi fa-regular fa-comment i-comm"></i> ${commentCount + 1}`;
                        }
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        });
    });


})