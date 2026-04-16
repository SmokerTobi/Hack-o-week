#Goal: Train a Logistic Regression model to predict failure based on sensor readings (Proximity, Temperature, Pressure).

#Python Code:
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
df = pd.read_csv('IIoT_Smart_Parking_Management.csv') 
X = df[['Sensor_Reading_Proximity', 'Weather_Temperature']]
y = df['Failure'] 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LogisticRegression()
model.fit(X_train, y_train)
print(f"Model Accuracy: {model.score(X_test, y_test)*100}%")
