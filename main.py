from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,EmailStr,AnyUrl,computed_field
from typing import Optional,List,Dict,Literal,Annotated
import pickle
import pandas as pd

#import the ml model

with open ('model.pkl','rb') as f:
    model=pickle.load(f)

app=FastAPI()

#pydantic model to validate
class userinput(BaseModel):
    
    age:Annotated[int,Field(...,gt=0,lt=120,description='Age of the user')]
    weight:Annotated[float,Field(...,gt=0,description='weight of the user')]
    height:Annotated[float,Field(...,gt=0,lt=2.5,description='height of the user in meters')]
    income_lpa:Annotated[float,Field(...,description='Annual salary of the user')]
    smoker:Annotated[bool,Field(...,description='Is the user a smoker')]
    city:Annotated[str,Field(...,description='city of the user')]
    occupation:Annotated[Literal['student', 'private_job', 'business_owner', 'government_job',
       'freelancer', 'retired'],Field(...,description = 'Occupation of the user')]
    
    @computed_field
    @property
    def bmi(self)->float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def lifestyle_risk(self)->str:
        if self.bmi and self.smoker>30:
            return 'high'
        elif self.bmi and self.smoker>27:
            return 'medium'
        else:
            return 'low'
    
    @computed_field
    @property
    def age_group(self)->str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        else:
            return "senior"
    
    @computed_field
    @property
    def city_tier(self)->int:
        tier_1_cities = [
        "Mumbai",
        "Delhi",
        "Bangalore",
        "Chennai",
        "Hyderabad",
        "Kolkata",
        "Pune"
        ]
    
        tier_2_cities = [
            "Indore",
            "Bhopal",
            "Nagpur",
            "Jaipur",
            "Jabalpur",
            "Lucknow",
            "Surat",
            "Patna"
        ]
        
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
    
@app.post('/predict')
def predict(data:userinput):
    input_df=pd.DataFrame([
        {
           'bmi':data.bmi,
           'age_group':data.age_group,
           'lifestyle_risk':data.lifestyle_risk,
           'city_tier':data.city_tier,
           'income_lpa':data.income_lpa,
           'occupation':data.occupation
        }]
    )
    prediction=model.predict(input_df)[0]

    return JSONResponse(content={'predicted_category':prediction},status_code=200)

## -------------------- DATA FLOW --------------------
# 1. Client sends input as JSON.
# 2. FastAPI passes JSON to the UserInput (Pydantic) model.
# 3. Pydantic validates the data and converts types (e.g., "22" -> int, "1.75" -> float).
# 4. Computed fields (bmi, age_group, lifestyle_risk, city_tier) are generated automatically.
# 5. The validated data is converted into a pandas DataFrame.
# 6. The DataFrame is passed to the trained ML model for prediction.
# 7. model.predict() returns a NumPy array; [0] extracts the single prediction.
# 8. FastAPI converts the Python dictionary into a JSON response and sends it to the client.
# ---------------------------------------------------

##why to calculate feilds again even we have already done it previously in th model?
#because model has learnt from the computed fields like bmi.. but the user is providing basic feilds like age,height..
#hence we compute computed feilds then convert then into dataframe and pass it to the model