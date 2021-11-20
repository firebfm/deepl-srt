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

# Coded by
# Automatic translation from Chinese srt to English srt in Deepl
# Download chromedriver, put the exe in driver_path which is C:\Program Files (x86)\chromedriver.exe
# Enter path of srt folder, all srt in the folder will be translated

def remove_timeline(txtpath):
	with open(txtpath, 'r', encoding='utf-8') as f:
		contents = f.read()
		# remove num + timeline
		sub1 = re.sub(r'\d+\n\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d', '', contents, 0, re.M)
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
			elif line != '\n' and len(linerList) == len(match)-1:
				liner += line
				linerList.append(liner)
				break
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

def paste_it(chunk):
	# Get the input_area
	input_css = 'div.lmt__inner_textarea_container textarea'
	input_area = driver.find_element_by_css_selector(input_css)
	pyperclip.copy(chunk)
	input_area.clear()
	input_area.send_keys(Keys.CONTROL+ "v")
	# For MacOS
	#input_area.send_keys(Keys.SHIFT, Keys.INSERT
	numC = len(chunk)
	if numC < 500:
		time.sleep(6)
	elif numC < 980:
		time.sleep(9)
	elif numC < 1546:
		time.sleep(10)
	elif numC < 2635:
		time.sleep(10)
	elif numC < 4000:
		time.sleep(17)
	else:
		time.sleep(18)

	# Getting button location on  the html tree
	button_css = 'div.lmt__target_toolbar__copy_container button'

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

	time.sleep(1)

	# Assign to content = pyperclip contents
	content = pyperclip.paste()
	input_area.clear()

	return content

# Start a Selenium driver
driver_path=r'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(driver_path)
# driver_path_2='C:\\Program Files (x86)\\geckodriver.exe'
# driver_2 = webdriver.Firefox(driver_path)

# Reach the deepL website

deepl_url = 'https://www.deepl.com/translator#ZH/EN/%0A'
driver.get(deepl_url)

print("enter path of srt folder")
srtpath = input()
listsrt = [os.path.join(srtpath, f) for f in os.listdir(srtpath) if f.endswith('.srt')]
skipArr = []

for srt in listsrt:
	txtpath = remove_timeline(srt)

	# count length of chracters
	with open(txtpath, 'r', encoding='utf-8') as f:
		all_text = f.read()
		match = re.search(r'\n\n\n', all_text)
		if match:
			print('Blank lines detected. Skipping...')
			skipArr.append(srt)
			continue

	sentence = ""
	list_sentence = []
	chunk = ""
	chunks = []
	finaltext = ""
	content = ""
	counter = 1

	print(f'Working on {os.path.basename(srt)}')
	if len(all_text) < 5000:
		print('the whole text can be pasted')
		content = paste_it(all_text)
		#content = re.sub(r'\nTranslated with www\.DeepL\.com/Translator \(free version\)', '', content, 0, re.M)
		finaltext += content
		pyperclip.copy('')
	else:
		# list of lines
		with open(txtpath, 'r', encoding='utf-8') as f:
			lines = f.readlines()

		
		for line in lines:
			if line != '\n' and line is not lines[-1]:
				sentence += line
			else:
				sentence += line
				list_sentence.append(sentence)
				sentence = ""

		for sentence in list_sentence:
			if len(chunk) <= 4950 and sentence is not list_sentence[-1]:
				chunk += sentence
			elif sentence is list_sentence[-1]:
				chunk += sentence
				chunks.append(chunk)
				chunk = ""
			else:
				chunks.append(chunk)
				chunk = ""
				chunk += sentence


		for chunk in chunks:
			chunk = ''.join(chunk)
			content = paste_it(chunk)
			#content = re.sub(r'\nTranslated with www\.DeepL\.com/Translator \(free version\)', '', content, 0, re.M)
			finaltext += content

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
	finaltext = finaltext.replace("(coll.) (colloquial)", "really")
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
	os.remove(completeName)
	os.remove(txtpath)

	print(f'{os.path.basename(finalsrt)} IS COMPLETED')
print(f'Number of srt that got skipped: {len(skipArr)}')
print(skipArr)
#driver.quit()
