from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import os
import re
import pyperclip

# Coded by firechip/firebfm
# Automatic translation from Chinese srt to English srt in Deepl
# Download chromedriver, put the exe in driver_path which is C:\Program Files (x86)\chromedriver.exe
# Enter path of srt folder, all srt in the folder will be translated

def remove_timeline(txtpath):
	with open(txtpath, 'r', encoding='utf-8') as f:
		contents = f.read()
		# remove num + timeline
		sub1 = re.sub(r'\d+\n.*', '', contents, 0, re.M)
		sub1 = re.sub(r'\n', '', sub1, 1, re.M)
		sub1 = re.sub(r'\n\n', '\n', sub1, 0, re.M)

	os.path.splitext(txtpath)[0]
	with open(os.path.splitext(txtpath)[0] + '.og.txt', 'w', encoding='utf-8') as f:
		f.write(sub1)

	return os.path.splitext(txtpath)[0] + '.og.txt'


def combine_srt(mysrt, wordtxt, finalsrt):
	with open(mysrt, 'r', encoding='utf-8') as f:
		srt = f.read()
		match = re.findall(r'\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+', srt)

	linerList = []
	liner = ""
	with open(wordtxt, "r", encoding="utf-8", errors='ignore') as wordfile:
		lines = wordfile.readlines()
		for line in lines:
			if line != '\n' and line is not lines[-1]:
				liner += line
			elif line is lines[-1]:
				liner += line
				linerList.append(liner)
			else:
				linerList.append(liner)
				liner = ""

	count = 0
	with open(finalsrt, 'w', encoding='utf-8') as resfile:
		for timeline in match:
			resfile.write(f"{count+1}\n")
			resfile.write(timeline+'\n')
			resfile.write(linerList[count])
			resfile.write("\n")
			count += 1

# Start a Selenium driver
driver_path=r'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(driver_path)

# Reach the deepL website
deepl_url = 'https://www.deepl.com/translator#ZH/EN/%0A'
#deepl_url = 'https://www.deepl.com/translator#EN/ZH/%0A'
driver.get(deepl_url)

print("enter path of srt folder")
srtpath = input()
listsrt = [os.path.join(srtpath, f) for f in os.listdir(srtpath) if f.endswith('.srt')]

for srt in listsrt:
	txtpath = remove_timeline(srt)

	# count length of chracters
	with open(txtpath, 'r', encoding='utf-8') as f:
		all_text = f.read()	
	numC = len(all_text)

	sentence = ""
	list_sentence = []
	chunk = ""
	chunks = []
	finaltext = ""
	content = ""
	counter = 1

	print(f'Working on {os.path.basename(srt)}')
	if numC < 5000:
		print('the whole text can be pasted')
		# Get the input_area
		input_css = 'div.lmt__inner_textarea_container textarea'
		input_area = driver.find_element_by_css_selector(input_css)
		pyperclip.copy(all_text)
		input_area.clear()
		input_area.send_keys(Keys.CONTROL+ "v")
		# wait for translation
		time.sleep(14)

		# Getting button location on  the html tree
		button_css = ' div.lmt__target_toolbar__copy button' 

		# Getting the button object
		button = driver.find_element_by_css_selector(button_css)

		# Extracting its position
		y = button.location['y']

		# Positionning the button into the screen
		driver.execute_script("window.scrollTo(0, {})".format(y - 150))

		time.sleep(2)

		# Getting the button object
		# (again - its position has been actualized and we need to get the new positions for the click)
		button = driver.find_element_by_css_selector(button_css)

		# Making the click => translation is now in our pyperclip
		button.click()
		button.click()

		time.sleep(2)

		# Assign to content = pyperclip contents
		content = pyperclip.paste()
		#content = re.sub(r'\nTranslated with www\.DeepL\.com/Translator \(free version\)', '', content, 0, re.M)
		finaltext += content
		pyperclip.copy('')
		input_area.clear()
	else:
		# list of lines
		with open(txtpath, 'r', encoding='utf-8') as f:
			lines = f.readlines()

		
		for line in lines:
			if line != '\n' and line != lines[-1]:
				sentence += line
			else:
				sentence += line
				list_sentence.append(sentence)
				sentence = ""

		for sentence in list_sentence:
			if len(chunk) <= 4950 and sentence != list_sentence[-1]:
				chunk += sentence
			elif sentence == list_sentence[-1]:
				chunk += sentence
				chunks.append(chunk)
				chunk = ""
			else:
				chunks.append(chunk)
				chunk = ""
				chunk += sentence


		for chunk in chunks:
			# Get the input_area
			input_css = 'div.lmt__inner_textarea_container textarea'
			input_area = driver.find_element_by_css_selector(input_css)

			chunk = ''.join(chunk)
			#print(chunk)
			# Set the sentence into the pyperclip
			pyperclip.copy(chunk)

			# Making sure that there is no previous text
			input_area.clear()

			# Pasting the copied sentence into the input_area
			input_area.send_keys(Keys.CONTROL+ "v")

			# For MacOS
			#input_area.send_keys(Keys.SHIFT, Keys.INSERT)

			# Wait for translation to appear on the web page
			time.sleep(14)

			# Getting button location on  the html tree
			button_css = ' div.lmt__target_toolbar__copy button' 

			# Getting the button object
			button = driver.find_element_by_css_selector(button_css)

			# Extracting its position
			y = button.location['y']

			# Positionning the button into the screen
			driver.execute_script("window.scrollTo(0, {})".format(y - 150))

			time.sleep(2)

			# Getting the button object
			# (again - its position has been actualized and we need to get the new positions for the click)
			button = driver.find_element_by_css_selector(button_css)

			# Making the click => translation is now in our pyperclip
			button.click()
			button.click()

			time.sleep(2)

			# Assign to content = pyperclip contents
			content = pyperclip.paste()
			#content = re.sub(r'\nTranslated with www\.DeepL\.com/Translator \(free version\)', '', content, 0, re.M)
			finaltext += content

			input_area.clear()

			#content = content.replace("\n\n", "\n")
			# testing, debugging, checking chunk files for errors
			'''
			with open(srtpath+f'\\chnk_{os.path.basename(srt)}-0{counter}.txt', 'w', encoding='utf-8-sig') as g:
			    g.write(content)

			with open(srtpath+f'\\chnk_{os.path.basename(srt)}-0{counter}.txt', 'r', encoding='utf-8-sig') as g:
			    lines = g.read()
			    xx = lines.replace("\n\n", "\n")

			with open(srtpath+f'\\chnk_{os.path.basename(srt)}-0{counter}.txt', 'w', encoding='utf-8-sig') as g:
			    g.write(xx)

			counter += 1
			print(f'CHUNK is')
			print(f'{chunk}')
			print(f'content is')
			print(f'{content}')
			'''
			print(f'chunk {counter} is done')
			counter += 1
			content = ""
			pyperclip.copy('')
	#finaltext = finaltext.replace("\n\n", "\n")
	completeName = os.path.splitext(srt)[0] + '.en.txt'
	finaltext = finaltext.replace("\nTranslated with www.DeepL.com/Translator (free version)", "")
	with open(completeName, 'w', encoding='utf-8') as g:
	    g.write(finaltext)

	with open(completeName, 'r', encoding='utf-8') as g:
	    finaltext2 = g.read()
	    finaltext3 = finaltext2.replace("\n\n", "\n")
	    finaltext3 = finaltext3.replace("\n\n\n", "\n")

	with open(completeName, 'w', encoding='utf-8') as g:
	    g.write(finaltext3)

	finalsrt = os.path.splitext(srt)[0] + '.dl.en.srt'
	try:
		combine_srt(srt, completeName, finalsrt)
	except IndexError:
		print("ERROR FAILED")
		continue
	# delete text files
	#os.remove(completeName)
	#os.remove(txtpath)

	print(f'{os.path.basename(finalsrt)} IS COMPLETED')
driver.quit()
