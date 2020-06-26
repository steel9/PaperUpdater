# PaperUpdater
A Python script for automating Paper Spigot updates

## Documentation
### Get Started (Linux)
1. Navigate to your server directory, and execute 'git clone https://github.com/steel9/PaperUpdater.git'
2. Call the script before starting the server in the script, with the -y parameter. See example below.

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
