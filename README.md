# ArmyTracker
A Simple Army Tracker that allows for a user to log-in and view soldiers rank, name, and squad position. Validation is in place to be able to remove and add soldiers as well as change the password for the default admin created on first launch.
## Setup
1. Download Docker from the [Docker Website](https://www.docker.com/products/docker-desktop)
2. Download the latest release from the releases section
3. Extract the contents of the ZIP into any directory
4. From that directory run ```docker build -t army-tracker .```
5. Finished!
## First Run
On first run, login using the credentials
```
username: 'admin'
password: 'password1'
```
## Running
To run the application, run the command
```docker run -i -t -p 5000:5000 army-tracker```. There is a current issue where the IP address may change where you need to connect to from the terminal,
always connect to the website via ```http://172.0.0.1:5000```
