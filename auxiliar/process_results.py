import sys


def generate_output(log_file, exposome_file, output_file):
	"""

	:param log_file:
	:param exposome_file:
	:param output_file:
	:return:
	"""

	log = open(log_file, 'r', encoding='utf-8')
	lines = log.readlines()
	lines.reverse()
	log.close()

	predictive_classes = []
	tensor_lines = False
	for line in lines:
		if 'device=' in line:
			predictive_class = line.split(',')[0][-1]
			predictive_classes.append(predictive_class)
			tensor_lines = True
		else:
			if tensor_lines:
				break

	exposome = open(exposome_file, 'r', encoding='utf-8')
	exposome.readline()  # skip header
	exposome_lines = exposome.readlines()

	dataset_lines = []
	for line in exposome_lines:
		sentence = line.split('\t')[-1][:-1]
		dataset_lines.append(sentence)

	if len(predictive_classes) != len(dataset_lines):
		raise AssertionError('Mismatched files length', len(predictive_classes), len(dataset_lines))

	label_to_pair_type = {'no_relation': '0', 'effect': '1', 'mechanism': '2', 'advise': '3', 'int': '4'}
	pair_type_to_label = {v: k for k, v in label_to_pair_type.items()}

	out_file = open(output_file, 'w', encoding='utf-8')
	for line_number, element in enumerate(predictive_classes):
		# if predictive_classes[line_number] != '0':  # change to all
		out_file.write(pair_type_to_label[predictive_classes[line_number]] + '\t' + dataset_lines[line_number] + '\n')

	out_file.close()


def main():
	"""Usage example: python3 ...

	:return:
	"""

	results_file = sys.argv[1]
	original_file = sys.argv[2]
	processed_file = sys.argv[3]

	generate_output(results_file, original_file, processed_file)

	return


if __name__ == '__main__':
	main()

