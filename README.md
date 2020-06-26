# PaperUpdater
A Python script for automating Paper Spigot updates.

## Documentation
### Get Started (Linux)
1. Navigate to your server directory, and execute <code>git clone https://github.com/steel9/PaperUpdater.git</code>
2. Run <code>python3 PaperUpdater/update_paper.py -c</code> and set the desired Paper version and the path to your server script (the one that does NOT call the updater script, that actually starts the server).
3. Create another server script - you should have two. The first script should execute PaperUpdater, and then call the other script which actually starts the server. See example below.

### Example Usage
start.sh - script that is executed by systemd when starting server

    #!/bin/sh

    python3 PaperUpdater/update_paper.py -y
    sh ./start_noupdate.sh
start_noupdate.sh - script that actually starts the server, which is executed after updating Paper (replace '\_123' with the build number of your server jar)

    #!/bin/sh

    java -Xmx8G -jar paper_123.jar

### Parameter Options
|Parameter|Alternative|Definition|
|---|---|---|
|-c|--config|Opens the interactive configuration menu.|
|-y||Downloads and applies updates without asking.|
