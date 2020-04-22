#!/usr/bin/python3

from os import name
from sys import argv
from time import sleep
from xmltodict import parse
from requests import get, post
from collections import Counter
from dateutil.parser import parse as time

if len(argv) != 2:
	exit(f"Usage: python3 {argv[0]} <s3 bucket url>")

print(r"""
                   ____
                  (_  _)
        .  .       / /
     .`_._'_..    / /
     \   o   /   / /
      \ /   /  _/ /_ 
`. ~. `\___/'./~.' /.~'`.
.`'`.`.'`'`.~.`'~.`'`.~`
  B u c k e t   S i f t""" + "\n")

files, mimes, totalSize = [], [], 0

# Remove trainling slashes
url = argv[1].strip("/")
# Add a protocol if if wasn't supplied
url = "http://" + url if url[:4] != "http" else url
# Prime the pump with the first bucket page's URL
pageURL = url

# Helper function to print bold (if on *nix) or return bold string
def printB (s, r=0):
	nix = name.lower() != "nt"
	s = '\033[1m' * nix + s + '\033[0m' * nix
	if r:
		return s
	print(s)

class file:
	def __init__(self, name, size, date):
		self.name = name
		self.size = size
		self.date = date

# Bad practice, but ¯\_(ツ)_/¯
while True:
	fileDict = parse(get(pageURL, verify=False, timeout=20).content)
	
	# If we get a webpage error an single file XML responce (i.e end)
	if ("Contents" not in fileDict["ListBucketResult"] or
		len(fileDict["ListBucketResult"]["Contents"]) == 5):
		break
		
	# Extract the name date and size from each file
	for i in fileDict["ListBucketResult"]["Contents"]:
		name = i["Key"]
		date = time(i["LastModified"])
		size = int(i["Size"])
		
		# Keep a running total of the total bucket size
		totalSize += size
		
		# Running list of files and extentions
		files.append(file(name, size, date))
		mimes.append(name.split(".")[-1].lower())
		
	print(f"Pulled {len(files)} files     ", end="\r")
	# Hope we don't get rate limited, I'm sure this can be optimised
	if len(files) % 10000 == 0 and len(files):
		print("10s Rate limit sleep", end="\r")
		sleep(10)
	else:
		sleep(1)
	# You request the next page by specifying the last file on the prior page
	pageURL = url + "/?marker=" + files[-1].name 

# Convert total bucketsize from bits to GBs
totalSize = round(totalSize / 1000 / 1000 / 1000, 3)
print(f"\n{len(files)} files totaling {totalSize} GB\n")

printB("Number of files by type ignoring single occurrences")
count = Counter(mimes)
for mime, tally in count.most_common():
	print(f"  .{mime[:13].ljust(13, ' ')} {tally}") if tally > 1 else ""

printB("\nNewest files")
# Sort files by inner date key (newest first)
files.sort(key=lambda x: x.date, reverse=True)
# Just the ten most recent files
for file in files[:10]:
	# Dates are fine, doesn't need to me time-granular
	date = str(file.date).split(" ")[0]
	print(f"  {date}\t{url}/{file.name}")
	
printB("\nLargest files")
# Sort files by inner size field (largest first)
files.sort(key=lambda x: x.size, reverse=True)
# Just the ten largest thanks
for file in files[:10]:
	# Convert bits to MBs or GBs if over 999MB
	size = round(file.size / 1000 / 1000, 3)
	if size > 999:
		print(f"  {size / 1000} GB\t{url}/{file.name}")
	else:
		print(f"  {size} MB\t{url}/{file.name}")
	
# Create a small TXT to test anonymous uploading
upload = "uploadTest.txt"
with open(upload, "w") as uploadFile:
	uploadFile.write("This has been an anonymous upload test.")
# Send a POST request with our upload test file to see if anon upload is enabled
r = post(url, files={'file': open(upload,'r')}, data={'key': upload})
# If we get a 2XX response, it likely worked
if 200 <= r.status_code < 300:
	printB("\n[!!!!!] Anonymous upload enabled [!!!!!]")
else:
	print("\nAnon upload disabled")
	
# Array of files in format: URL + file
lines = [url + "/" + file.name for file in files]
# Dump raw file list to files.txt
with open("files.txt", "w") as out:
	out.write("\n".join(lines))

# Now we're going to generate our tree
print("Generating tree files... Sit tight.", end="\r")
treeLines, files, printedFiles, printedDirs, treeDirLines = [], [], [], [], []

# Return a list of exploded filenames e.g a/b/c > ['a', 'b', 'c']
for line in lines:
	line = line.strip()
	if line != "": # Drop empty lines
		broken = line.split("/")[2:] # Ignore protocol
		files.append([x for x in broken if x]) # Drop empty items

# The way this works is that every bit of every file becomes a line
# but then we unique lines, so we don't have 1000s of repeats
for f in sorted(files):
	# And for each of its bits
	for idx, dir in enumerate(f):
		count = 0
		# If this is the last bit
		if dir == f[-1]:
			# If this file hasn't been printed yet
			if f not in printedFiles:
				# Generate a line with required nesting, add it to running list
				z = "    " * idx + "" + dir
				treeLines.append(z)
				printedFiles.append(f)
		# If this is the second last bit (and inherently a directory)
		elif dir == f[-2]:
			# Have we printed this directory yet?
			if f[:-1] not in printedDirs:
				# How many files are in this directory?
				for all in files:
					if f[:-1] == all[:-1]:
						count += 1
				# Save line with required nesting and bold it
				z = "    " * idx + printB(dir, 1) + f"[{count}]"
				treeLines.append(z)
				printedDirs.append(f[:-1])
		# If this is another bit
		else:
			# Add a line for this bits' directory if we don't have it already
			if f[:idx + 1] not in printedDirs:
				z = "    " * idx + printB(dir, 1)
				treeLines.append(z)
				printedDirs.append(f[:idx + 1])
				
# Write the unique lines to tree.txt
with open("tree.txt", "w") as tre:
	tre.write("\n".join(treeLines) + "\n")
	
# Get only directory lines, and add those to dirTree.txt
[treeDirLines.append(i) if '\033[0m' in i else "" for i in treeLines]
with open("dirTree.txt", "w") as tre:
	tre.write("\n".join(treeDirLines) + "\n")
	print("                                  ")