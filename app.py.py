#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib


# In[4]:


app = Flask(__name__)


# In[5]:


# Load the trained model
model = joblib.load('fish_species_model.pkl')


# In[6]:


@app.route('/')
def home():
    return 'Fish Species Prediction API'


# In[7]:


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        weight = float(data['weight'])
        length1 = float(data['length1'])
        length2 = float(data['length2'])
        length3 = float(data['length3'])
        height = float(data['height'])
        width = float(data['width'])

        input_data = np.array([[weight, length1, length2, length3, height, width]])
        prediction = model.predict(input_data)[0]
        return jsonify({'species': int(prediction)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# In[ ]:





# In[9]:


get_ipython().system('pip install Flask gunicorn')


# In[ ]:




