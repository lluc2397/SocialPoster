# SocialPoster
I started using SQLAlchemy with Alembic for the ORM. As I want to use it with my website I switched to the Django ORM so it will be easier to implement, I also like the Django ORM, you need to writte less and is as flexible as SQLAlchemy (in my opinion, i'm probably wrong).

A little app that allows me to create, parse and share content on differents social medias (SM) like Facebook, Twitter, Youtube, Instagram and soon Google My business (GMB), Tiktok and Linkedin.

There is a CLI to use the main functions : create a short from an image and share it, resize a downloaded image and share it and finally share a downloaded video.
The CLI can be used to schedule these funtions and use them with crontab.

Other functions avaible are:
-Parse a youtube channel
-Download youtube videos and captions
-Share content across differents SM and do some crosspostage (currently it only supports repost Youtube videos and Facebook posts)

TODOS
(Some can be found on the final.py)
-Create class to post on Linkedin, Tiktok and GMB.
-Generalize more the current class so it would be possible to post some content created "on the fly"
-Create post text --> Post some text on twitter and Facebook
                --> Repost the tweet on old facebook
-Create general class to create posts with default values
-Be able to retweet own tweets
-Lookup for trending hashtags
-Download images from insta
-Do some exploratory data analysis to find the best kind of post for each social media
