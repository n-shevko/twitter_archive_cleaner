## How to Install

    git clone https://github.com/n-shevko/twitter_archive_cleaner.git
    cd twitter_archive_cleaner
    pip install -r packages

## How to use

    python parser.py -f /path/to/archive/folder

It will generate 'parser-output' folder inside '/path/to/archive/folder' folder.  

There will be 2 result files inside 'parser-output' folder:

result.html

result.pdf     


File result.html will use files from parser-output/media folder. 
So don't rename this folder.

## Other options for parser.py

--pdf           Generate pdf version. Turned on by default.  --download      Download the original size images (may take 1-2 hours). Turned off by default.

Based on https://github.com/timhutton/twitter-archive-parser

