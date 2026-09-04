import os
import sys
import django
import pandas as pd
from sklearn import linear_model
import time

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_price.settings")
django.setup()

from dataset.models import CarDataSet

class Execute:
    def __init__(self):
        self.app=CarDataSet
        self.name=CarDataSet.__name__
        self.parent_idr=os.path.dirname(os.getcwd())
        self.csv_path=os.path.join(self.parent_idr,'car_price_prediction.csv')
        self.df=pd.read_csv(self.csv_path)
        self.df['Mileage'] = (
            self.df['Mileage']
            .astype(str)
            .str.replace('km', '', regex=False)
            .str.replace(' ', '', regex=False)
        )
        self.df = self.df[self.df['Levy'] != '-']
        self.data = self.df.drop_duplicates()

    def execute(self):
        print(self.data.head(30))

    def sync_data(self):
        records=self.data.to_dict(orient='records')
        total=len(records)
        for index,row in enumerate(records,start=1):
            start_time=time.time()
            self.app.objects.update_or_create(
                id=row['ID'],
                defaults={
                    'price': row['Price'],
                    'leavy': row['Levy'],
                    'manufacturer': row['Manufacturer'],
                    'model': row['Model'],
                    'prod_year': row['Prod. year'],
                    'category': row['Category'],
                    'leather_interior': row['Leather interior'],
                    'fuel_type': row['Fuel type'],
                    'engine_volume': row['Engine volume'],
                    'mileage': row['Mileage'],
                    'cylinders': row['Cylinders'],
                    'gear_bo_type': row['Gear box type'],
                    'drive_wheel': row['Drive wheels'],
                    'door': row['Doors'],
                    'wheel': row['Wheel'],
                    'color': row['Color'],
                    'airbag': row['Airbags'],
                }
            )
            iteration_time = time.time() - start_time
            print(f"[{index}/{total}] Processed ID {row['ID']} in {iteration_time:.4f} seconds")


def main():
    app = Execute()
    app.sync_data()

if __name__ == "__main__":
    main()