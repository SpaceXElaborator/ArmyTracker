FROM python:3.8-slim-buster
WORKDIR /ArmyTracker
add . /ArmyTracker
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 5000
CMD ["python3", "Tracker.py"]