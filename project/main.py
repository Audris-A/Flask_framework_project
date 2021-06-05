import matplotlib.pyplot as plt
from matplotlib import cm
from PIL import Image
import datetime
import io
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import sys
import base64
import math
import copy
from flask_pymongo import PyMongo
from flask import Flask, render_template, request
import numpy as np

venue_id = 0

x_min = 0
y_min = 0
x_max = 0
y_max = 0
coordinates = []
xCoordArr = []
yCoordArr = []
OFFSET = 0
distinctRecordsWithTime = {}

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
app.config["MONGO_URI"] = sys.argv[1]
mongodb_client = PyMongo(app)
database = mongodb_client.db
locationCollection = ""

@app.route("/", methods=['POST', 'GET'])
def home():
    return render_template("layout.html")


@app.route("/about", methods=['POST', 'GET'])
def about():
    return render_template("about.html")


@app.route("/analysis", methods=['POST', 'GET'])
def analysis():
    allVenues = database.deploymentVenues.find({})

    return render_template("analysis.html", venues=allVenues, deployment_names=[])


@app.route("/analysis_type", methods=['POST', 'GET'])
def analysis_type():
    system = request.form.get('system')
    venue = request.form.get('venue')

    if venue:
        if system == 'Decawave':
            allDeploymentDays = database.deploymentDays.find(
                {"localization_sys_name": "Decawave", "venue_id": int(venue)})
        elif system == 'Eliko':
            allDeploymentDays = database.deploymentDays.find({"localization_sys_name": "Eliko", "venue_id": int(venue)})
        else:
            allDeploymentDays = database.deploymentDays.find({})
    else:
        allDeploymentDays = []

    return render_template("analysis_type.html", deployment_names=allDeploymentDays)


@app.route('/plotSystemData', methods=['POST', 'GET'])
def createPlot():
    global locationCollection
    global database
    global zoneImageCollection
    global x_min
    global x_max
    global y_min
    global y_max
    x_min = 1000
    x_max = -1000
    y_min = 1000
    y_max = -1000

    distinctRecords = {}
    requestType = request.form['type']  # 1 -> Decawave, 2 -> Eliko

    dateFrom = request.form['dateFrom']
    timeFrom = request.form['timeFrom']
    dateTo = request.form['dateTo']
    timeTo = request.form['timeTo']
    miliSeconds = ".000000"

    datetimeFrom = dateFrom + " " + timeFrom + miliSeconds
    datetimeTo = dateTo + " " + timeTo + miliSeconds

    deploymentName = request.form['deploymentName']

    zoneImageCollection = database["zoneImages"]

    if requestType == "Decawave":
        locationCollection = database["location"]
        zoneId = request.form['zoneId']
        if not zoneId:
            zoneId = request.form.getlist('zoneId')

        offset = int(request.form['offset'])

        # add image functionality for Decawave

        fig, ax = plt.subplots()
        output = io.BytesIO()

        distinctRecords = formatDecawaveData(datetimeFrom, datetimeTo, zoneId, offset, deploymentName)
    elif requestType == "Eliko":
        locationCollection = database["ElikoLocations"]

        imageRecord = 0
        for rec in zoneImageCollection.find({"zone_id": deploymentName, "system_id": 2}):
            imageRecord = rec
            break

        img = Image.open(BytesIO(base64.b64decode(imageRecord["image_value"])))

        fig, ax = plt.subplots()
        output = io.BytesIO()

        distinctRecords = formatElikoData(datetimeFrom, datetimeTo, deploymentName)

        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)

    colors = iter(cm.rainbow(np.linspace(0, 1, len(distinctRecords))))
    for key in distinctRecords:
        plt.scatter(distinctRecords[key][0], distinctRecords[key][1], color=next(colors))

    fig.set_size_inches(30, 15)
    try:
        ax.imshow(img, extent=[x_min, x_max, y_min, y_max])
    except:
        print("No image")

    FigureCanvas(fig).print_png(output)

    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(output.getvalue()).decode('utf8')

    return render_template("index.html", image=pngImageB64String)


def formatElikoData(datetimeFrom, datetimeTo, deploymentName):
    global locationCollection
    global x_min
    global x_max
    global y_min
    global y_max

    #records = []
    distinctRecords = {}

    date_time_str_from = datetimeFrom
    date_time_str_until = datetimeTo

    timeFrom = datetime.datetime.strptime(date_time_str_from, '%d.%m.%Y %H:%M:%S.%f')
    timeUntil = datetime.datetime.strptime(date_time_str_until, '%d.%m.%Y %H:%M:%S.%f')

    for rec in locationCollection.find({"zone_id": deploymentName}):
        timestampVal = datetime.datetime.strptime(rec["timestamp"], '%d.%m.%Y %H:%M:%S.%f')
        if rec["error_msg"] == "" and timestampVal >= timeFrom and timestampVal <= timeUntil:
            tagId = str(rec["tag_id"])
            if tagId not in distinctRecords:
                distinctRecords[tagId] = [[], []]
            distinctRecords[tagId][0].append(float(rec["x_coordinate"]))
            distinctRecords[tagId][1].append(float(rec["y_coordinate"]))

            val_x = float(rec["x_coordinate"])
            val_y = float(rec["y_coordinate"])

            if val_x < x_min:
                x_min = copy.deepcopy(val_x)

            if val_y < y_min:
                y_min = copy.deepcopy(val_y)

            if val_x > x_max:
                x_max = copy.deepcopy(val_x)

            if val_y > y_max:
                y_max = copy.deepcopy(val_y)

    return distinctRecords

    # For data with timestamp
    """
            coordinates.append([float(x["x_coordinate"]), float(x["y_coordinate"])])

            records.append(x)
    if len(records) > 0:
        date_time_str_from = datetimeFrom
        date_time_str_until = datetimeTo

        timeFrom = datetime.datetime.strptime(date_time_str_from, '%d.%m.%Y %H:%M:%S.%f')
        timeUntil = datetime.datetime.strptime(date_time_str_until, '%d.%m.%Y %H:%M:%S.%f')

        for rec in records:
            timestampVal = datetime.datetime.strptime(rec["timestamp"], '%d.%m.%Y %H:%M:%S.%f')
            if timestampVal >= timeFrom and timestampVal <= timeUntil:
                tagId = str(rec["tag_id"])
                if tagId not in distinctRecords:
                    distinctRecords[tagId] = [[], []]
                distinctRecords[tagId][0].append(float(rec["x_coordinate"]))
                distinctRecords[tagId][1].append(float(rec["y_coordinate"]))

                if tagId not in distinctRecordsWithTime:
                    distinctRecordsWithTime[tagId] = {}
                    distinctRecordsWithTime[tagId]["x"] = []
                    distinctRecordsWithTime[tagId]["y"] = []
                    distinctRecordsWithTime[tagId]["timestamp"] = []
                    distinctRecordsWithTime[tagId]["zone_id"] = []

                distinctRecordsWithTime[tagId]["x"].append(float(rec["x_coordinate"]))
                distinctRecordsWithTime[tagId]["y"].append(float(rec["y_coordinate"]))
                distinctRecordsWithTime[tagId]["timestamp"].append(timestampVal)
                distinctRecordsWithTime[tagId]["zone_id"].append(rec["zone_id"])

                xCoordArr.append(float(rec["x_coordinate"]))
                yCoordArr.append(float(rec["y_coordinate"]))"""


def formatDecawaveData(datetimeFrom, datetimeTo, zoneId, offset, deploymentName):
    global x_min
    global x_max
    global y_min
    global y_max
    global locationCollection

    #records = []
    distinctRecords = {}

    date_time_str_from = datetimeFrom
    date_time_str_until = datetimeTo

    timeFrom = datetime.datetime.strptime(date_time_str_from, '%d.%m.%Y %H:%M:%S.%f')
    timeUntil = datetime.datetime.strptime(date_time_str_until, '%d.%m.%Y %H:%M:%S.%f')

    if isinstance(zoneId, list):
        for rec in locationCollection.find({"zone_id": {"$in": zoneId}, "name": deploymentName}):
            timestampVal = datetime.datetime.strptime(rec["timestamp"], '%Y-%m-%d %H:%M:%S.%f')
            if not math.isnan(rec["x_coordinate"]) and timestampVal >= timeFrom and timestampVal <= timeUntil:
                rec["x_coordinate"] = rec["x_coordinate"] - offset
                rec["y_coordinate"] = rec["y_coordinate"] - offset

                tagId = str(rec["tag_id"])
                if tagId not in distinctRecords:
                    distinctRecords[tagId] = [[], []]
                distinctRecords[tagId][0].append(float(rec["x_coordinate"]))
                distinctRecords[tagId][1].append(float(rec["y_coordinate"]))

                val_x = float(rec["x_coordinate"]) - offset
                val_y = float(rec["y_coordinate"]) - offset

                if val_x < x_min:
                    x_min = copy.deepcopy(val_x)

                if val_y < y_min:
                    y_min = copy.deepcopy(val_y)

                if val_x > x_max:
                    x_max = copy.deepcopy(val_x)

                if val_y > y_max:
                    y_max = copy.deepcopy(val_y)

                # For data with timestamp
                #coordinates.append([float(x["x_coordinate"]), x["y_coordinate"]])

                #records.append(x)
    else:
        for rec in locationCollection.find({"zone_id": zoneId, "name": deploymentName}):
            timestampVal = datetime.datetime.strptime(rec["timestamp"], '%Y-%m-%d %H:%M:%S.%f')
            if not math.isnan(rec["x_coordinate"]) and rec["x_coordinate"] > offset\
               and timestampVal >= timeFrom and rec["y_coordinate"] > offset\
               and timestampVal <= timeUntil:
                rec["x_coordinate"] = rec["x_coordinate"] - offset
                rec["y_coordinate"] = rec["y_coordinate"] - offset

                tagId = str(rec["tag_id"])
                if tagId not in distinctRecords:
                    distinctRecords[tagId] = [[], []]
                distinctRecords[tagId][0].append(float(rec["x_coordinate"]))
                distinctRecords[tagId][1].append(float(rec["y_coordinate"]))

                val_x = float(rec["x_coordinate"]) - offset
                val_y = float(rec["y_coordinate"]) - offset

                if val_x < x_min:
                    x_min = copy.deepcopy(val_x)

                if val_y < y_min:
                    y_min = copy.deepcopy(val_y)

                if val_x > x_max:
                    x_max = copy.deepcopy(val_x)

                if val_y > y_max:
                    y_max = copy.deepcopy(val_y)

    return distinctRecords

    # For data with timestamp
    """
                coordinates.append([float(x["x_coordinate"]), x["y_coordinate"]])

                records.append(x)

    if len(records) > 0:
        date_time_str_from = datetimeFrom
        date_time_str_until = datetimeTo

        timeFrom = datetime.datetime.strptime(date_time_str_from, '%d.%m.%Y %H:%M:%S.%f')
        timeUntil = datetime.datetime.strptime(date_time_str_until, '%d.%m.%Y %H:%M:%S.%f')

        for rec in records:
            timestampVal = datetime.datetime.strptime(rec["timestamp"], '%Y-%m-%d %H:%M:%S.%f')
            if timestampVal >= timeFrom and timestampVal <= timeUntil:
                tagId = str(rec["tag_id"])
                if tagId not in distinctRecords:
                    distinctRecords[tagId] = [[], []]
                distinctRecords[tagId][0].append(float(rec["x_coordinate"]))
                distinctRecords[tagId][1].append(float(rec["y_coordinate"]))

                if tagId not in distinctRecordsWithTime:
                    distinctRecordsWithTime[tagId] = {}
                    distinctRecordsWithTime[tagId]["x"] = []
                    distinctRecordsWithTime[tagId]["y"] = []
                    distinctRecordsWithTime[tagId]["timestamp"] = []
                    distinctRecordsWithTime[tagId]["zone_id"] = []

                distinctRecordsWithTime[tagId]["x"].append(float(rec["x_coordinate"]))
                distinctRecordsWithTime[tagId]["y"].append(float(rec["y_coordinate"]))
                distinctRecordsWithTime[tagId]["timestamp"].append(timestampVal)
                distinctRecordsWithTime[tagId]["zone_id"].append(rec["zone_id"])

                xCoordArr.append(float(rec["x_coordinate"]))
                yCoordArr.append(float(rec["y_coordinate"]))
    """

if __name__ == "__main__":
    app.run(debug=True)
