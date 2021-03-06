# PaperUpdater - EXPERIMENTAL BETA
A Python script for automating Paper Spigot updates.

## Documentation
### Prerequisites
- Python 3
- Requests (Python module)

### Get Started (Debian/Linux)
1. Install Python 3 if not already installed. Do so by executing <code>sudo apt update</code> and then <code>sudo apt install python3</code>
2. Install Requests if not already installed. Do so by executing <code>pip install requests</code>
3. Navigate to your server directory, and execute <code>git clone https://github.com/steel9/PaperUpdater.git</code>
4. Create the server scripts - you should have two. The first script should execute PaperUpdater, and then call the other script which actually starts the server. See example below.
5. Run <code>./PaperUpdater/update_paper.py -c</code> and set the desired Paper version and the path to your second server script (the one that does NOT call the updater script, the one that actually starts the server - start_noupdate.sh in the example).


### Example Usage
**start.sh** - script that is executed by systemd when starting server

    #!/bin/sh

    python3 PaperUpdater/update_paper.py -y
    sh ./start_noupdate.sh
**start_noupdate.sh** - script that actually starts the server, which is executed after updating Paper. The update script will automatically update the filename to the name of the downloaded server jar - **but ensure you write the placeholder filename exactly as below, so the script can recognize and replace it.**

    #!/bin/sh

    java -Xmx8G -jar paper-1.16.4-123.jar

### Parameter Options
|Parameter|Alternative|Definition|
|---|---|---|
|-c|--config|Opens the interactive configuration menu.|
|-y||Downloads and applies updates without asking.|
