import os
import sys
from collections import defaultdict
import itertools

if len(sys.argv) != 3:
	print "Usage: python extract.py <dictionary file> <product names file>"
	sys.exit(1)

# Expected format: <id>\t<list of predicted brand names>\n
dictionaryfile = sys.argv[1]

# Expected format: <id>\t<product name>\t<correct brand name>\n
development_set = sys.argv[2]

# Import dictionary into array
dictionary= []
productnames=[]
productids=[]
brandnames = defaultdict(list)
dictwithfrequencies = defaultdict(list)
final_array =defaultdict(list)

folder_name = './stage2'
def writeto_file(filename):

	global folder_name
	with open(os.path.join(folder_name,filename), 'w') as fd:
		for p in productnames:
			i = productnames.index(p)
			fd.write("{0}\t{1}\t{2}\n".format(productids[i],productnames[i].encode("UTF-8"),final_array[i]))


with open(dictionaryfile, 'r') as fd:
	for line in fd:
		split_line = line.split('\t')
		value = split_line[0].strip().lower()
		frequency = split_line[1].strip().lower() 
		dictionary.append(value.lower())
		dictwithfrequencies[value.lower()]=frequency


#Import product names into array -- Development SET I 
with open(development_set, 'r') as fd:
	for line in fd:
		split_line = line.split('\t')
		product_id = split_line[0].strip().lower()
		productids.append(product_id)
		product_name = split_line[1].strip().lower()
		productnames.append(product_name)



#Now we have product names and dictionaries, let's compare them. 
for p in productnames: 
	i = productnames.index(p)
	a = p.split()
	for element in a:
		indexOfElement = a.index(element)
		try:
			if a[indexOfElement-1] == 'for' or a[indexOfElement+1] == 'compatible':
				pass
			else:
				for item in dictionary:
					if item.lower() == element:
						brandnames[i].append(item)
		except IndexError:
			for item in dictionary:
				if item.lower() == element:
					brandnames[i].append(item)

	#If you didn't find any brandname maybe it's of size 2, hence take all possible combinations and compare
	for x, y in itertools.izip(a, a[1:]):
		x = x+" "+y
		for item in dictionary:
			if item.lower() == x.lower():
				brandnames[i].append(item)
	
	#Check for size = 3			
	
	for x, y, z in itertools.izip(a, a[1:1:]):
		x = x+" "+y+" "+z
		#print x
		for item in dictionary:
			if item.lower() == x.lower():
				brandnames[i].append(item)

  #Check for size = 4 
	d = [a[j:j+4] for j in xrange(len(a)-3)]
	
	for item in d:
		x = " ".join(item)
	
		for item in dictionary:
			if item.lower() == x.lower():
				brandnames[i].append(item)
	if not brandnames[i]:
		brandnames[i].append("NoBrand")


#Now remove keys with lesser frequency

valuestoretain = ""
#If length is 1, no need to check frequency, else check frequencies, find maximum and retain the maximum one
for key in brandnames:
	
	length = len(brandnames[key])
	if length == 1:
		
		final_array[key]=brandnames[key][0]
	if length != 1:
		maximum = 0
		for i in range (0,length):
			if (int(dictwithfrequencies.get(brandnames[key][i])) > maximum): 
				maximum = int(dictwithfrequencies.get(brandnames[key][i]))
				valuestoretain = brandnames[key][i]
		final_array[key] = valuestoretain


#Write results back to file matching by indexes
print final_array
writeto_file("result1.txt")

