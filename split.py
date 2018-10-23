from xml.etree import ElementTree as Elm
from xml.dom import minidom
import re
from copy import deepcopy
import calendar

# open the file
html = Elm.parse('message.html').getroot()

# replace the messy in-tag style with a separate, neat .css file
head = html.find('head')
style = head.find('style')
css = re.sub('}', '\n}\n\n', style.text)
css = re.sub('{', '{\n', css)
css = re.sub(';', ';\n', css)
with open('style.css', 'w+') as f:
	f.write(css)
head.remove(style)
link = Elm.SubElement(head, 'link')
link.attrib = {'rel':'stylesheet', 'type':'text/css', 'href':'style.css'}
head[1], head[3] = head[3], head[1] # swap link and base so css is found

# iterate through the html cloning the head and body every time a new month of messages
# is encountered
months = {}
# since everything is annoyingly a div, get the proper main node with all messages
parent = html.find('./body/div/div/div/div[@class="_3a_u"]')
main = parent.find('./div[@role="main"]')
# remove the main from the tree, so the skeleton can be copied without copying all messages
parent.remove(main)

month_nums = {calendar.month_name[i]:str(i) for i in range(1,13)}

# reverse the order because for some reason facebook dumps them as last at the top, and
# I prefer top to be the beginning
for message in reversed(main):
	# For group chats there can be messages that don't have text that only list the
	# participants in the conversation. Just skip these.
	if len(message) < 3:
		print Elm.tostring(message)
		continue

	# Find the month the message belongs to, creating a new html tree if necessary.
	# Messages always go person, text, date, and date is always day, month, year, time,
	# so slice out the "month year" and make it "year number_month" for sake of file order
	time_stamp = message[2].text.split()
	date = time_stamp[2] + ' ' + month_nums[time_stamp[1]] + '_' + time_stamp[1]
	if date not in months: # then we have to make a new html tree
		months[date] = deepcopy(html)
		month_parent = months[date].find('./body/div/div/div/div[@class="_3a_u"]')
		month_main = Elm.SubElement(month_parent, 'main', {'class':'_4t5n', 'role':'main'})
	
	month_main.append(message)

# write the html back out
for month in months:
	cleaned = re.sub('<div[ ]*/>', '', Elm.tostring(months[month])) # because <div/>s mess up the formatting
	pretty = minidom.parseString(cleaned).toprettyxml()[23:] # chop off preamble
	with open(month + '.html', 'w') as f:
		f.write(pretty.encode('utf-8'))

print "done"
