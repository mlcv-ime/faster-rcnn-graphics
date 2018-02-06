import os.path as osp
import sys

def add_path(path):
	if path not in sys.path:
		sys.path.insert(0, path)

my_dir = osp.dirname(__file__)
tf_path = osp.join(my_dir, '..', 'models', 'research')
print(tf_path)
add_path(tf_path)
