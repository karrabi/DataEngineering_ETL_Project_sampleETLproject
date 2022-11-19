import pandas as pd
import time

import loader 
from logger import Log


def update_dim_tables():
    
    loader.update_dim_symbols()
    loader.update_dim_resolutions()
    
    

def load_fact_tables():
    
    loader.load_Transformed_data()

def main():

    while True:
        now = int(time.time())
        if now % 3600 == 3480: # 58th min of every hour
            update_dim_tables()
            Log('{} - Update Dim Tables finished'.format(now))
            
            load_fact_tables()
            Log('{} - Load Fac Tables finished'.format(now))

            time.sleep(1)

if __name__ == '__main__':
    main()
    