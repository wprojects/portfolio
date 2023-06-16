import time
print('Witness Data written to DB')
import witness_db_to_csv
print('Witness Data written to CSV, updating to tables...')
time.sleep(3)
import witness_existing_table
time.sleep(3)
from witnessed import witnessed_existing_table
print('Witness automation complete')
