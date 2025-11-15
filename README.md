# ED_itinerary
Copies your next destination to a clipboard from a txt file. 
Use pansh.co.uk/tourist/ to get a optimal path frm A to Z via what ever systems you need. 

If you skip a destination, it will let you know.
Ignores visists to systems not on your itinerary.txt

Your config.json file should look like this
```
{
    "JOURNAL_DIR": "/home/yourname/EDlogs/",
    "ITINERARY_FILE": "itinerary.txt",
    "POLL_INTERVAL": 2.0
}
```
Your itinerary.txt should look like this:
```
System 1
System 2
System 3
```

Set up the venv and run in the script directory 

First time: 
```
sudo apt update && sudo apt install -y xclip
mkdir ed-itinerary 
cd ~/ed-itinerary
python3 -m venv .venv
source .venv/bin/activate
./ed_itinerary.py
```
next time 
```
cd ~/ed-itinerary
source .venv/bin/activate
./ed_itinerary.py
```
