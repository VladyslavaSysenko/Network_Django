document.addEventListener("DOMContentLoaded", () => {
    // Load followers and following
    if (window.location.pathname.slice(0, 6+userpage.length) === `/user/${userpage}`) {follow_info();}
    // Edit post
    edit();
    // Show active nav page
    nav_active();
    // Submit new post
    try{document.querySelector('#btn_new_post').addEventListener('click', new_post)}
    catch(e) {}
    
    try{
        // Un_like post
        like();
        // Like info
        like_info();
        // Follow/unfollow
        document.querySelector("#follow_btn").addEventListener("click", un_follow);
    }
    catch(e) {}
});
    

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrf_token = getCookie('csrftoken');


function nav_active() {
    let links = document.querySelectorAll('.nav-link');
    links.forEach(link => {
        if (link.href === window.location.href) {
            links.forEach(link => {
                link.classList.remove('active_nav');
            });
            link.classList.add('active_nav');
        }
    })
    }
 

function un_follow() {
    fetch(`/user/${userpage}/1`, {
        method: 'PUT',
        headers: { "X-CSRFToken": csrf_token }
    })
    .then(response => response.json())
    .then(result => {follow_info()});
}


function follow_info() {
    fetch(`/follow/${userpage}`,{
        method: 'PUT',
        headers: { "X-CSRFToken": csrf_token }
    })
    .then(response => response.json())
    .then(result => {
        // show amount of followers and followings
        document.querySelector("#followers_info").innerHTML = result.followers;
        document.querySelector("#following_info").innerHTML = result.following;
        // change button text if user followed
        if (userpage != username) {
            if (result.un_followed === 1) {
                document.querySelector("#follow_btn").innerHTML = "Unfollow"
            }
            // if user unfollowed
            else if (result.un_followed === 0) {
                document.querySelector("#follow_btn").innerHTML = "Follow"
            }
        }
    });
}


function like() {
    document.querySelectorAll(".post").forEach(post => {
        // update un_liked post
        post.querySelector(".heart").onclick = () => {
            fetch(`/like/change/${post.id.slice(5)}`,{
                method: 'PUT',
                headers: { "X-CSRFToken": csrf_token }
            })
            .then(response => response.json())
            .then(result => {
                // Update amount of likes
                like_info();
            });
        }
    })
}


function like_info() {
    document.querySelectorAll(".post").forEach(post => {
        fetch(`/like/info/${post.id.slice(5)}`,{
            method: 'PUT',
            headers: { "X-CSRFToken": csrf_token }
        })
        .then(response => response.json())
        .then(result => {
            heart = document.querySelector(`#${post.id}`).querySelector(".heart")
            // show amount of likes
            heart.innerHTML = result.amount_likes;
            // if liked
            if (result.un_liked === 1) {
                heart.className = "heart heart_liked"
            }
            // if unliked
            else if (result.un_liked === 0) {
                heart.className = "heart heart_unliked"
            }
        });
    })
}


function edit() {
    document.querySelectorAll(".post").forEach(post => {
        try {
            post.querySelector(".edit_div .edit_btn").onclick = () => {
                // get text of post
                text = post.querySelector(".text .textarea").innerHTML;
                // make text changeable
                post.querySelector(".text").innerHTML = `<span class="textarea" role="textbox" contenteditable autofocus">${text}</span>`
                // change edit to save button
                post.querySelector(".edit_div .edit_btn").innerHTML = "Save";
                post.querySelector(".edit_div .edit_btn").classList.replace("edit_btn","save_btn");
                // save changes on click
                post.querySelector(".edit_div .save_btn").onclick = () => {
                    save_edit(post);
                }
            }
        }
        catch(e) {return true;}
    })
}


function save_edit(post) {
    // get new text
    new_text = post.querySelector(".text .textarea").innerText;
    // make text unchangeable
    post.querySelector(".text").innerHTML = `<span class="textarea" role="textbox">${new_text}</span>`
    // change save to edit button
    post.querySelector(".edit_div .save_btn").innerHTML = "Edit";
    post.querySelector(".edit_div .save_btn").classList.replace("save_btn","edit_btn");
    // save changes
    fetch(`/edit/${post.id.slice(5)}`,{
        method: 'PUT',
        headers: { "X-CSRFToken": csrf_token },
        body: JSON.stringify({text: new_text})
    })
    // enable edit
    edit();
}


function new_post() {
    fetch(`/new`, {
        method: 'PUT',
        headers: { "X-CSRFToken": csrf_token },
        body: JSON.stringify({"text":document.querySelector('#text_new_post').innerText})
    })
    .then(response => response.json())
    .then(result => {
        if (result.success === "no") {
            alert("Post can't be empty")
        }
        else {
            window.location.pathname = `/user/${username}/1`;
        }
    });
}

