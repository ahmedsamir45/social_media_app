
const posts = document.querySelectorAll('.post');


posts.forEach(post => {
    const likeButton = post.querySelector('.btnLike');
    const dislikeButton = post.querySelector('.btnDislike');
    const commentButton = post.querySelector('.btnComment');
    const commentsSection = post.querySelector('.comments');
    

    likeButton.addEventListener('click', function() {
        const likeIcon = likeButton.querySelector('.bi'); 
        likeButton.classList.toggle('liked'); 
        likeIcon.classList.toggle('text-primary');
        
        if (likeButton.classList.contains('liked')) {
            dislikeButton.classList.remove('disliked');
            const dislikeIcon = dislikeButton.querySelector('.bi');
            dislikeIcon.classList.remove('text-danger'); 
        }
    });


    dislikeButton.addEventListener('click', function() {
        const dislikeIcon = dislikeButton.querySelector('.bi'); 
        dislikeButton.classList.toggle('disliked'); 
        dislikeIcon.classList.toggle('text-danger'); 
        
        if (dislikeButton.classList.contains('disliked')) {
            likeButton.classList.remove('liked'); 
            const likeIcon = likeButton.querySelector('.bi');
            likeIcon.classList.remove('text-primary');
        }
    });

    
    commentButton.addEventListener('click', function() {
        commentsSection.classList.toggle('active'); 
    });
});
