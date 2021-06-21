from flask import Flask, render_template, request
# import jsonify
import requests
import pickle
import numpy as np
import datetime
app = Flask(__name__)
model = pickle.load(open('./model/random_forest_reg_carprice.pkl', 'rb'))

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':

        Present_Price = (float(request.form['Present_Price']) / 1348)

        Kms_Driven = int(request.form['Kms_Driven'])

        Kms_Driven2 = np.log(Kms_Driven)

        Owner = int(request.form['Owner'])

        year = int(request.form['Year'])
        now = datetime.datetime.now()
        age = now.year - year

        fuel_type = request.form['Fuel_Type']
        if(fuel_type == 'Petrol'):
            x0_Petrol = 1
            x0_Diesel = 0
            x0_CNG = 0
        elif(fuel_type == 'Diesel'):
            x0_Petrol = 0
            x0_Diesel = 1
            x0_CNG = 0
        elif(fuel_type == 'CNG'):
            x0_Petrol = 0
            x0_Diesel = 0
            x0_CNG = 1
        else:
            x0_Petrol = 0
            x0_Diesel = 0
            x0_CNG = 0

        seller_type = request.form['Seller_Type']
        if(seller_type == 'Individual'):
            x0_Individual = 1
            x0_Dealer = 0
        elif(seller_type == 'Dealer'):
            x0_Individual = 0
            x0_Dealer = 1
        else:
            x0_Individual = 0
            x0_Dealer = 0

        transmission = request.form['Transmission']
        if(transmission == 'Manual'):
            x0_Automatic = 0
            x0_Manual = 1
        elif(transmission == 'Automatic'):
            x0_Automatic = 1
            x0_Manual = 0
        else:
            x0_Automatic = 0
            x0_Manual = 0

        prediction = model.predict([[Present_Price, Kms_Driven2, Owner, age, x0_Dealer,
                                     x0_Individual, x0_CNG, x0_Diesel, x0_Petrol, x0_Automatic, x0_Manual]])

        output = round((prediction[0] * 100000 * 0.013), 0)

        if output < 0:
            return render_template('index.html', prediction_text="Sorry, unable to produce a price.")
        else:
            return render_template('index.html', prediction_text="You could sell the car at {} USD".format(output))
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
