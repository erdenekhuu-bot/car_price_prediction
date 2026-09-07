import os
import sys
import django
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import numpy as np
import time
import math

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_price.settings")
django.setup()

from dataset.models import CarDataSet

categorical_columns = [
    'Manufacturer',
    'Model',
    'Category',
    'Leather interior',
    'Fuel type',
    'Gear box type',
    'Drive wheels',
    'Doors',
    'Wheel',
    'Color'
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            'cat',
            OneHotEncoder(handle_unknown='ignore'),
            categorical_columns
        )
    ],
    remainder='passthrough'
)

models = {
    'LinearRegression': LinearRegression(),
    'RandomForest': RandomForestRegressor(random_state=42),
    'GradientBoosting': GradientBoostingRegressor(random_state=42)
}

class Execute:
    def __init__(self):
        self.app=CarDataSet
        self.name=CarDataSet.__name__
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.parent_idr=os.path.dirname(self.script_dir)
        self.csv_path=os.path.join(self.parent_idr,'car_price_prediction.csv')
        self.df=pd.read_csv(self.csv_path)
        self.df['Mileage'] = (
            self.df['Mileage']
            .astype(str)
            .str.replace('km', '', regex=False)
            .str.replace(' ', '', regex=False)
        )
        self.df['Engine volume'] = (
            self.df['Engine volume']
            .astype(str)
            .str.replace('Turbo', '', regex=False)
            .str.strip()
        )
        self.df['Engine volume'] = pd.to_numeric(
            self.df['Engine volume'],
            errors='coerce'
        )
        self.df['Mileage'] = pd.to_numeric(
            self.df['Mileage'],
            errors='coerce'
        )
        self.df = self.df[self.df['Levy'] != '-']
        self.df['Levy'] = pd.to_numeric(
            self.df['Levy'],
            errors='coerce'
        )
        self.data = self.df.drop_duplicates()
        self.X = self.data.drop(
            columns=['Price', 'ID']
        )
        self.y = self.data['Price']
        self.model = Pipeline([
            ('preprocessor', preprocessor),
            ('regression', LinearRegression())
        ])
        X_train, X_test, y_train, y_test = train_test_split(
            self.X,
            self.y,
            test_size=0.2,
            random_state=42
        )
        self.model.fit(X_train, y_train)

    def action(self):
        X_train, X_test, y_train, y_test = train_test_split(
            self.X,
            self.y,
            test_size=0.2,
            random_state=42
        )
        model = Pipeline([
            ('preprocessor', preprocessor),
            ('regression', LinearRegression())
        ])
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        print([y_pred,mae,rmse,r2])

    def prepare_single_car(self, car_instance):
        data_dict = {
            'Levy': [car_instance.leavy],
            'Manufacturer': [car_instance.manufacturer],
            'Model': [car_instance.model],
            'Prod. year': [car_instance.prod_year],
            'Category': [car_instance.category],
            'Leather interior': [car_instance.leather_interior],
            'Fuel type': [car_instance.fuel_type],
            'Engine volume': [car_instance.engine_volume],
            'Mileage': [car_instance.mileage],
            'Cylinders': [car_instance.cylinders],
            'Gear box type': [car_instance.gear_bo_type],
            'Drive wheels': [car_instance.drive_wheel],
            'Doors': [car_instance.door],
            'Wheel': [car_instance.wheel],
            'Color': [car_instance.color],
            'Airbags': [car_instance.airbag]
        }

        df_single = pd.DataFrame(data_dict)
        df_single['Mileage'] = (
            df_single['Mileage'].astype(str)
            .str.replace('km', '', regex=False)
            .str.replace(' ', '', regex=False)
        )
        df_single['Engine volume'] = (
            df_single['Engine volume'].astype(str)
            .str.replace('Turbo', '', regex=False)
            .str.strip()
        )
        df_single['Engine volume'] = pd.to_numeric(df_single['Engine volume'], errors='coerce')
        df_single['Mileage'] = pd.to_numeric(df_single['Mileage'], errors='coerce')
        df_single['Levy'] = pd.to_numeric(df_single['Levy'], errors='coerce')

        return df_single

    def predict(self, car_instance):
        single_features = self.prepare_single_car(car_instance)
        prediction = self.model.predict(single_features)
        return math.ceil(float(prediction[0]))

    # only view to rest api
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
    app.action()

if __name__ == "__main__":
    main()