# **Network**

A Twitter-like social network website based on Django and JavaScript for making posts and following users.

---

## **Detailed description**

You can either read or watch a video https://youtu.be/54f612DewTk

>***New Post***: Users who are signed in can write a new text-based post.
>
>***All Posts***: The “All Posts” link in the navigation bar takes the user to a page where they can see all posts from all users, with the most recent posts first.
>
>***Profile Page***: Clicking on a username loads that user’s profile page. Signed-in users can follow or unfollow the person.
>
>***Following***: The “Following” link in the navigation bar takes the signed-in user to a page where they see all posts made by followed users.
>
>***Edit Post***: Users can click an “Edit” button on any of their own posts to edit that post.
>
>***"Like" and "Unlike"***: Users can click a button on any post to toggle whether or not they like that post.

---
## **To start the app**

- Cd into the network directory. 
- Run ***pip install -r requirements.txt*** to install all requirements.
- Run ***python manage.py runserver*** to start up the Django web server, and visit the website in your browser.

You can register as usual user or log into superuser via  
username - *superuser*  
password - *superuser*  
and go to http://127.0.0.1:8000/admin/ to see django admin interface.

---
## **To change database**

- In your terminal, cd into the network directory. 
- Run ***python manage.py makemigrations network*** to make migrations.
- Run ***python manage.py migrate*** to apply migrations to your database.