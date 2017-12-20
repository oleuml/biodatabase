import pandas as pd
import sqlite3
from sys import argv
from tqdm import tqdm

def make_sql_database(db_name, csv_files):
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	for f in tqdm(csv_files):
		name = f.split("/")[1].split(".")[0];
		data = pd.read_csv(f)
		if(name.startswith("chr")):
			data.set_index(['start', 'stop'], inplace = True)
			data.to_sql(name=name, con=conn, if_exists = 'replace', index=True)
		else:
			data.to_sql(name=name, con=conn, if_exists = 'replace', index=False)
		conn.commit()

	c.close()
	conn.close()
	