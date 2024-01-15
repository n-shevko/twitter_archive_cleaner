## How to Install

    git clone https://github.com/n-shevko/twitter_archive_cleaner.git
    cd twitter_archive_cleaner
    pip install -r packages

    for mac os:
    brew install python-tk 
    
    for ubuntu:
    sudo apt-get install python3-tk 

## How to use

    python parser.py

This command will open a tkinter UI. After pressing the "Run" button, 
it will generate a 'parser-output' folder inside the archive folder. 

There will be 2 result files inside 'parser-output' folder:

result.html

result.pdf     


File result.html will use files from parser-output/media folder. 
So don't rename this folder.

Based on https://github.com/timhutton/twitter-archive-parser

