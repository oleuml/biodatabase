import sqlite3
from multiprocessing import Pool

def execute_data_models(chr_name, model, region):
	conn = sqlite3.connect('chr{}.db'.format(chr_name))

	c = conn.cursor()
	c.execute('SELECT COUNT(*) FROM (' +
		'SELECT chr{}_models.start AS start1,'.format(chr_name) +
		'chr{}_models.stop AS stop1,'.format(chr_name) +
		'chr{}_annotations.start AS start2,'.format(chr_name) +
		'chr{}_annotations.stop AS stop2 '.format(chr_name) + 
		'FROM chr{}_models, chr{}_annotations '.format(chr_name, chr_name) + 
		'WHERE chr{}_annotations.type = {} '.format(chr_name, region) +
		'AND chr{}_models.model = {}) '.format(chr_name, model) +
		'WHERE start2 <= start1 AND stop1 <= stop2;')

	return [model, region, c.fetchone()[0]]

def execute_data_variants(chr_name, variant, region):
	conn = sqlite3.connect('chr3.db')

	c = conn.cursor()
	c.execute('SELECT COUNT(*) FROM (' +
		'SELECT chr{}_variants.start AS start1,'.format(chr_name) +
		'chr{}_variants.stop AS stop1,'.format(chr_name) +
		'chr{}_annotations.start AS start2,'.format(chr_name) +
		'chr{}_annotations.stop AS stop2 '.format(chr_name) + 
		'FROM chr{}_variants, chr{}_annotations '.format(chr_name, chr_name) + 
		'WHERE chr{}_annotations.type = {} '.format(chr_name, region) +
		'AND chr{}_variants.variant = {}) '.format(chr_name, variant) +
		'WHERE start2 <= start1 AND stop1 <= stop2;')

	return [variant, region, c.fetchone()[0]]

def execute_data_snp():
	return None

if __name__ == '__main__':
	chr_name = 3
	with Pool(7) as pool:
		results = pool.starmap(execute_data_models, [(chr_name, model, region) for model in range(0, 3) for region in range(1, 4)])
		results += pool.starmap(execute_data_variants, [(chr_name, variant, region) for variant in range(0, 18) for region in range(1, 4)])
	print(results)

