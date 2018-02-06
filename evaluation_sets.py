# --------------------------------------------------------
# Partition of datasets into training, validation, and test 
# sets for flowcharts and math expressions.
# Written by Frank Julca Aguilar
# --------------------------------------------------------

import numpy as np

train_fraction = 0.8
np.random.seed(1)


def read_train_val_sets(file_names_path):
    with open(file_names_path) as f:
        train_files = f.readlines()

    train_files = [x.strip() for x in train_files]
    num_train = int(train_fraction * len(train_files))
    np.random.shuffle(train_files)
    train_set = train_files[:num_train]
    val_set = train_files[num_train:]
    return train_set, val_set

def read_test_set(file_names_path):
    with open(file_names_path) as f:
        test_set = f.readlines()
    return [x.strip() for x in test_set]

flowchart_train_set, flowchart_val_set = read_train_val_sets('datasets/flowcharts/flowchart_train.txt')
math_train_set, math_val_set = read_train_val_sets('datasets/math/math_train.txt')

flowchart_test_set = read_test_set('datasets/flowcharts/flowchart_test.txt')
math_test_set = read_test_set('datasets/math/math_test.txt')

evaluation_set = {'flowchart_train_set': flowchart_train_set, 'flowchart_val_set': flowchart_val_set, 
'math_train_set': math_train_set, 'math_val_set': math_val_set, 'flowchart_test_set': flowchart_test_set, 
'math_test_set': math_test_set}

if __name__ == '__main__':
	print(len(flowchart_train_set))
	print(len(flowchart_val_set))
	print(len(flowchart_test_set))
	print(len(math_train_set))
	print(len(math_val_set))
	print(len(math_test_set))
	print(math_train_set[:10])
	print(math_val_set[:10])
	print(math_test_set[:10])





