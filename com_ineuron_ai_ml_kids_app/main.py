from flask import Flask, request
from flask import Response
import pandas as pd
import requests as req
from com_ineuron_ai_ml_forKids_model_training.train import Training
from com_ineuron_ai_ml_kids_model_predict.test1 import IneuronPredict
import os
import json

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)

app.config['DEBUG'] = True
@app.route("/predict", methods=['GET'])
def predictRoute():
	print("inside predictionRoute")
	print(request.args.get('messageText'))
	message = request.args.get('messageText')
	#input = str("What the shit have you done")
	print(message)
	csvFilePath = "../data/data.csv"
	modelname = "finalized_model.sav"
	feature = "lData"
	label = "lName"
	predict = IneuronPredict()
	result = predict.getprediction(message, csvFilePath, feature, label, modelname)
	print(result)
	return Response(result)


@app.route("/train", methods=['POST'])
def trainModel():
	#req_data = request
	print(request.json['data'])
	with open('../data/data.json', 'w', encoding='utf-8') as f:
		json.dump(request.json['data'], f, ensure_ascii=False, indent=4)
	dataFrame = pd.read_json('../data/data.json')
	dataFrame.to_csv(r'../data/data.csv', index = None, header=True)
	#print(dataFrame)
	fileLocation = "data"
	filename = "test.csv"
	feature = "lData"
	label = "lName"
	modelname = "finalized_model.sav"
	#training = Training(fileLocation, filename)
	training = Training()
	training.execute(dataFrame, feature, label, modelname)

	return Response("Success")


#port = int(os.getenv("PORT"))
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)
	#app.run(port=8080)
