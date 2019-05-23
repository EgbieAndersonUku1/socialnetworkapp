
# Social network application

This is social network application that I wrote because I needed to understand how facebook works. It allows the user to create a profile, login, edit their profile, adding profile images, add friends, block users, post or delete messages, change or reset passwords and much much more.


# How to use the application

  - First register your details and a confirmation email will be send to the registered email your provided
  - Once confirmed you be able to log into the application
  - Sometimes for a hotmail account the confirmation message or any message send by the application might go to your junk mai. Check your junk mail if the message is not found in your regular email. The email address associated with the application will appear as socialbooknetworkapplication. Click the link or copy and paste to the url field

# Finding a user in the application
  - To find a user add the name of user first add a slash followed by the name to the end of the url  e.g. https://absocialnetwork.com/<username to find here> or http://127.0.0.1:5000/<username to find here> if you are running it on your local computer and click enter. Once entered click enter and you be taking the user profile page, you can then add them send a friend request if you want. 
  
# Accept a friend a request or deny
To find all the people that have sent you a friend requests click the pending_friend tab. This will display all your pending friend requests

# Viewing friends
To find all the people that are friends with, click on view friends. This will display all your friends 

# Viewing blocked people 
To find all the people that have block click on blocked list. This will display all the people you have blocked along with an option to unblock

On a side not the application also send the user a pending friend request to their email.


### Using Gmail to run the application

The application uses gmail as it means of sending emails, registration code, resetting or changing password codes, friend request emails, informs the user if their password has been changed and much more. For the application to use the gmail you must do a couple of a things.

  - First you must turn on the secure-less-app in your gmail account
  - Go to utils/emailer/sender.py and enter your gmail address and password in the top bit of the global variables and hit save.


### Installation

To run application on your local computer, download the application and run
```
$ sudo apt-get install -r requirement.txt
$ Start the database by running mongodb you might have to add sudo in some commputers
$ go to the run.py file and type "python run.py"
$ go to the url field and type http://127.0.0.1:5000
```
.


### Todos

 - Complete the rest of doc string for my methods and functions

### Running the program live
To run the program live navigate to the https://absocialnetwork.com. The application uses https which is a secure encryption that scrambles data over the internet.
 
   
  


