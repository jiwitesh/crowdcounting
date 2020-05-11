import csv


class Predict:

    def __init__(self, csvFilePath):
        self.mappingDict = {}
        self.csvFilePath = csvFilePath
        # self.modelname = modelname
        # self.feature = feature

    def createMappingDict(self):
        input_file = csv.DictReader(open(self.csvFilePath))
        for row in input_file:
            if row["lName"].strip().lower() in self.mappingDict:
                specificDataList = self.mappingDict[row["lName"].strip().lower()]
                specificDataList.append(row["lData"].strip().lower())
                self.mappingDict[row["lName"].strip().lower()] = specificDataList
            else:
                tempList = [row["lData"].strip().lower()]
                self.mappingDict[row["lName"].strip().lower()] = tempList
        print(self.mappingDict.keys())

    def getPrediction(self, inputString):
        for key in self.mappingDict.keys():
            templist = self.mappingDict[key]
            print(templist)
            if inputString.strip().lower() in templist:
                return key
        else:
            return "unknown"
        # response = {"response": result}
        # result = predict.getprediction(message, csvFilePath, feature, label, modelname)
        # print("jsonify output ", json.dumps(response))
        # print(Response(response))
