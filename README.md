# ED_itinerary
Copies your next destination to a clipboard from a txt file. 
Use spansh.co.uk/tourist/ to get the optimal path from A to Z via whatever systems you need. 

If you skip a destination on your list, it will let you know.
Script ignores visits to systems not in your itinerary.txt

## config.json

Your config.json file should look like this
```
{
    "JOURNAL_DIR": "/home/yourname/EDlogs/",
    "ITINERARY_FILE": "itinerary.txt",
    "POLL_INTERVAL": 2.0
}
```

## itinerary.txt

Your itinerary.txt should look like this:
System 1 is your starting system, Sys 20 is you last system where you 
```
System 1
System 2
System 3
...
System 20
```
Last system on the list can be the one where you end your trip. 

## Run the program 

Set up the "venv" and run the program in the same directory. 

First time: 
```
sudo apt update && sudo apt install -y xclip
mkdir ~/ed-itinerary 
cd ~/ed-itinerary
python3 -m venv .venv
source .venv/bin/activate
./ed_itinerary.py
```
next time 
```
cd ~/ed-itinerary && source .venv/bin/activate && ./ed_itinerary.py
```
