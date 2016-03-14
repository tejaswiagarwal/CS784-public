import os
import sys


if len(sys.argv) != 3:
	print "Usage: python pr.py <predictions file> <correct file>"
	sys.exit(1)

# Expected format: <id>\t<product name>\t<list of predicted brand names>\n
predictions_file = sys.argv[1]

# Expected format: <id>\t<product name>\t<correct brand name>\n
correct_file = sys.argv[2]

# Create dict of correct names to check against
golden_dict = {}
with open(correct_file, 'r') as fd:
	for line in fd:
		split_line = line.split('\t')
		prod_id = split_line[0].strip().lower()
		correct_name = split_line[2].strip().lower()
		golden_dict[prod_id] = correct_name

print str(golden_dict)
predicted_dict = {}
with open(predictions_file, 'r') as fd:
	for line in fd:
		split_line = line.split('\t')
		prod_id = split_line[0].strip().lower()
		predicted_name = split_line[2].strip().lower()				# .split(',') # to handle list of predictions
		predicted_dict[prod_id] = predicted_name


print len(predicted_dict)
correct_predictions = 0
for k,v in predicted_dict.items():
	if k not in golden_dict:
		print "{0} not found in the golden dict".format(k)
	if v == golden_dict.get(k):
		correct_predictions += 1
	else:
		print "For {0}, predicted - {1}, correct - {2}".format(k, v, golden_dict.get(k))

num_predicted = len(predicted_dict)
num_golden = len(golden_dict)

precision = correct_predictions/float(num_predicted)
recall = correct_predictions/float(num_golden)
f1 = (2*precision*recall)/(precision+recall)

print "Precision: {0}, Recall: {1}, F1: {2}".format(precision, recall, f1)
