#!/bin/sh

wget -q -O - https://apt.mopidy.com/mopidy.gpg | sudo apt-key add -

sudo wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/jessie.list

sudo apt-get update
sudo apt-get install python-spotify

sudo apt-get install python-pip python-alsaaudio

sudo pip install Flask
sudo pip install flask-socketio
