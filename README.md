# prashnottar-django
Prashnottar, a Quora clone built using django.
![Home](/screenshots/home.png?raw=true)


## Features
* **Custom Front Page Trending/Ranking Algorithm:** The project uses a custom trending/ranking algorithm which ensures maximum interaction among users.
* **Topics Automatically Generated:** For every question entered by the user, topics are automatically generated using RAKE algorithm.
* **Voting:** Voting functionality for questions, answers & comments.
* **Nested Comments:** Threaded (Nested) comments upto 4 levels.
* **Similar Questions suggestion:** In the question detail page, for every question similar questions are suggested to the user.
* **Anonymous Users:** Ask/Answer questions anonymously.
* **Follow/Unfollow System:** Users can follow/unfollow other users as well as questions.
* **Notification System:** Robust Notification system built using django signals.
* **Request System:** Users can request answers for a question from other users.
* **Text Formatting:** Integration of django-summernote for better text formatting.
* Many more!

## Usage
1. Clone this repo using `https://github.com/singhkumarpratik/prashnottar-django.git`
2. Install dependencies using `pip install -r requirements.txt`
3. Migrate using `python manage.py migrate`
4. Load fixtures using <br/>
`python manage.py fixtures/users.json` <br/>
`python manage.py fixtures/qnA.json` <br/>
5. Run server using `python manage.py runserver`

## Demo
https://prashnottar-django.herokuapp.com/ <br/>
Test credentials: <br/>
username: johndoe@gmail.com <br/>
password: Wsy8r6TZW3bSk
