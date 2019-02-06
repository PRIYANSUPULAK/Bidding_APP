# Bidding_APP

## Project Overview
This is a Bidding Web app where you can freely sell your products or can bid on any of the available products of your choice.
This is a free to all platform for bidding.
In order to bid or post your product for auction you need to SignUp on this platform.
Signing up requires only a username and a password.
Password of the users are safe as they are hashed using an algorithm. So, even the creator or person handling the database can't find the exact password typed of the user.


## How to Run?
### PreRequisites
1. [python3](https://www.python.org/downloads/)
2. [flask] `pip install flask==0.9` `pip install Flask-Login==0.1.3`
3. [sqlalchemy] `apt-get -qqy install python-sqlalchemy`
4. [httplib2]  `pip install httplib2`
5. [SQLite3](https://linuxhint.com/install-sqlite-ubuntu-linux-mint/)    

### Clone the Repository to your local computer using command:
`git clone https://github.com/PRIYANSUPULAK/Bidding_APP.git`

#### The database includes two tables:
1. The **User** table includes the data of registered users.
2. The **Item** table includes one data of items having a reference column of User table.

### Run the program
`python main.py`

### Final Step:
#### Open Your Browser and go to `localhost:5000/`
