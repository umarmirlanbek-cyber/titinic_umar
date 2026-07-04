from fastapi import FastAPI
import joblib
import uvicorn
from pydantic import BaseModel

titanic_app = FastAPI()

model = joblib.load('model_titanic.pkl')
scaler = joblib.load('scaler_titanic.pkl')

class TitanicSchema(BaseModel):
    Pclass: int
    Sex: str
    Age: int
    FamilySize: int
    Fare: float
    Embarked: str

@titanic_app.post('/predict')
async def predict_survived(titanic: TitanicSchema):
    titanic_data = titanic.model_dump()

    sex = titanic_data.pop('Sex')
    sex_0_1 = [1 if sex == 'male' else 0]

    embarked = titanic_data.pop('Embarked')
    embarked_0_1 = [1 if embarked == 'S' else 0]

    data = list(titanic_data.values()) + sex_0_1 + embarked_0_1
    scaler_data = scaler.transform([data])
    pred = model.predict(scaler_data)[0]
    prediction = 'Survived' if pred.item() == 1 else 'Not Survived'

    return {'Answer': prediction}

if __name__ == '__main__':
    uvicorn.run(titanic_app, host='127.0.0.1', port=9000)