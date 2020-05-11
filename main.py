from wsgiref import simple_server

from flask import Flask, request, jsonify
from flask import Response
import pandas as pd

from com_ai_ineuron_utils.utils import createDirectoryForTrainingImages, deleteExistingTrainingFolder
from com_ineuron_ai_ml_kids_model_predict.TextClassification import Predict
import os
import json
from flask_cors import CORS, cross_origin

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True

trainingDataFolderPath = "data/"
@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRoute():
    try:
        if request.json['messageText'] is not None and request.json['userId'] is not None and request.json['projectId'] is not None:
            message = request.json['messageText']
            userId = str(request.json['userId'])
            projectId = str(request.json['projectId'])
            csvFilePath = trainingDataFolderPath + userId + "/" + projectId + "/data.csv"
            # print("userID and projectId given is",userId, projectId)
            # print("Data sent for prediction is :",request.json['messageText'])
            # csvFilePath = "data/data.csv"
            # modelname = "finalized_model.sav"
            # feature = "lData"
            # predictObj = Predict(csvFilePath, modelname, feature)
            predictObj = Predict(csvFilePath)
            predictObj.createMappingDict()
            result = predictObj.getPrediction(message)
    except ValueError:
        return Response("Value not found inside  json data")
    except KeyError:
        return Response("Key value error incorrect key passed")
    except Exception as e:
        return Response((str(e)))
    return Response(result)


@app.route("/train", methods=['POST'])
@cross_origin()
def trainModel():

    try:
        if request.json['userId'] is not None:
            userId = str(request.json['userId'])
            # path = trainingDataFolderPath+userId
        if request.json['projectId'] is not None:
            projectId = str(request.json['projectId'])
            # path = path + "/" + projectId
        # print("userId is {} and projectId is {}".format(userId,projectId))

        createDirectoryForTrainingImages(userId, projectId)
        # print("Directory is created successfully!!!")
        path = trainingDataFolderPath + userId + "/" + projectId
        # print("path created is...", path)
        if request.json['data'] is not None:
            # print("data given for training is :",request.json['data'])
            with open(path + '/data.json', 'w', encoding='utf-8') as f:
                json.dump(request.json['data'], f, ensure_ascii=False, indent=4)
            # print("training data is at the path...", path)
            dataFrame = pd.read_json(path + '/data.json')
            dataFrame.to_csv(path + '/data.csv', index=None, header=True)
    except ValueError as val:
        return Response("Value not found inside  json data")
    except KeyError as keyval:
        return Response("Key value error incorrect key passed")
    except Exception as e:
        return Response(e)

    # print(dataFrame)
    # fileLocation = "data"
    # filename = "test.csv"
    # feature = "lData"
    # label = "lName"
    # modelname = "finalized_model.sav"
    # training = Training(fileLocation, filename)
    # training = Training()
    # training.execute(dataFrame, feature, label, modelname)

    return Response("Success")


@app.route("/deleteuserproject", methods=["GET"])
@cross_origin()
def deleteUserProjectFolder():
    try:
        if request.args.get("userId") is not None:
            userId = request.args.get("userId")
            userIdAndProjectId = trainingDataFolderPath + userId
        if request.args.get("projectId") is not None:
            projectId = request.args.get("projectId")
            userIdAndProjectId = userIdAndProjectId + "/" + projectId

        # pathForExitingFolder = "ids/" + userId
        deleteExistingTrainingFolder(userIdAndProjectId)

    except Exception as e:
        return e
    return "Operation Successfully completed"


@app.route("/noofusers", methods=["GET"])
@cross_origin()
def getTrainingImagesFolders():
    try:
        for root, dirs, files in os.walk("data"):
            print("%s these are the images you have trained so far" % dirs)
            return Response("%s these are the images you have trained so far" % dirs)
        return "We don't have any images for training so far"
    except Exception as e:
        return e
    return "We don't have any images for training so far"


# port = int(os.getenv("PORT"))
if __name__ == "__main__":
    host = '0.0.0.0'
    port = 5000
    httpd = simple_server.make_server(host, port, app)
    # print("Serving on %s %d" % (host, port))
    httpd.serve_forever()
# app.run(port=8080)
