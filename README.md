# changelog
jan 11 2022, credits to wheezy1749
```
-- Added webdriver_manager as a dependency. Don't have to deal with installing or changing path to EXE file
-- Added command line argument functionality. Keeping the input() method. Simply call the script with the SRT path directory or file as the first command line argument.
-- Added "name "check so the script can also by imported as a module and the user can then use Sub2Eng() in their own code. This is how I'm currently using it. Very useful to add this to other scripts.
-- Changed the URL to use the autodetect language feature so the script can be used with Japanese/Korean/etc without any changes.
-- Allow input to be a single srt file OR a folder containing srt files (did error checking on the files/folder existing)
```

# deepl-srt
Use Selenium to automate translation of a foreign language srt (Chinese, Japanese, etc) to English on Deepl website. Enter the path of your srt folder and every srt will be translated.
The input srt must be in UTF-8 format and not have empty lines. If needed, use SubtitleEdit > tools > fix common errors > remove empty lines

## Installation

You need Chrome and download chromedriver and put it in the driver_path which is C:\Program Files (x86).
You need Python 3.6 or greater because I wrote f-strings in the code which is not a feature on older Python versions. I currently use Python 3.9 
```python
pip install selenium
pip install pyperclip
pip install webdriver-manager
```

## Usage example
```python
python deeplv4.py
```

## No future updates
If the website ever gets a redesign then the script will break. Just right click inspect for any new css classes like if the button is found inside a different container or the button css got renamed.

## Note this script is for Windows users
Ctrl C and Ctrl V is the copy paste command for Windows users. That's what I wrote the code to do. For MacOS users you need to change the copy paste command inside the code.

## References
Thanks to the towardsdatascience article on using Selenium and deepL to automate the translation of PowerPoint files
