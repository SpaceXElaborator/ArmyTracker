# ArmyTracker
An all-in-one Tracker for military companies. Easy setup and installation to get started and simple buttons and viewing for anyone to be able to use. Starting from version 7.0 onward, admins/Platoon Sergeants will be able to start editing what is tracked and presented when viewing soliders. Comes with a calendar to see what soldiers are doing for any specific day. Soldiers can request Appointments and Team Leads have the ability to accept or deny with messages to be sent back to the soldier. Tracked information will be added to the calendar without any extra steps besides accepting.
## Testing
  To test the features of the calendar as they are right now, you will have to add soldier "Sean Rahman" as a SPC. The calendar dates will then show for that soldier on the days: May 18, 19, 20. If you'd like to see you're own calendar events, check the very bottom of "Tracker.py" To see the syntax for adding your own even with a given date and time.
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
## Coming Soon
1. Custom tracker options
2. Calender events [+]
3. Color to easy show who is red on what
4. Add/Remove other admins
5. Add/Remove documents for quicker and easier tracking
