from sklearn.linear_model import LinearRegression
import pandas as pd
import datetime as dt
from datetime import datetime
import PySimpleGUI as sg

print("This is the Roasting Predictor")

def generate_model():
	# get and collate data
	df = pd.read_csv("data.csv")
	subset = df[['numRoasts', 'numSmallRoasts', 'totalTime']]
	X = subset[['numRoasts', 'numSmallRoasts']]
	y = subset['totalTime']


	# train model
	reg = LinearRegression().fit(X, y)
	return reg


def predict(numRoasts, numSmallRoasts, reg):
	

	data = {'numRoasts': [numRoasts], 'numSmallRoasts': [numSmallRoasts]}
	x_pred = pd.DataFrame(data)
	pred = reg.predict(x_pred)

	return pred

def format_pred(pred, startHTime, startMTime):
	pred_h = int(pred[0] / 60)
	pred_m = int(pred[0] % 60)

	
	endHTime = int(startHTime) + pred_h
	
	if (startMTime == ''): startMTime = 0
	endMTime = int(startMTime) + pred_m

	if (endMTime >= 60):
		endHTime += 1
		endMTime -= 60

	if (endHTime >= 24):
		endHTime -= 24

	if (endHTime >= 12):
		endHTime -= 12
		formatted = f"finish at {endHTime}:{endMTime:02d} PM"
	elif (endHTime >= 0):
		formatted = f"finish at {endHTime}:{endMTime:02d} AM"
	else:
		formatted = "Something went wrong!"

	return formatted

def create_pred_window():
	layout = [  [sg.Text('Update')],
            [sg.Text("Number of Large Roasts", size = (18,1)), sg.Input("", key=f"BIG_ROAST", size = (11,1))], 
			[sg.Text("Number of Small Roasts", size = (18,1)), sg.Input("", key=f"SMALL_ROAST", size = (11,1))], 
			[sg.Text("Start Time (24h)", size = (18,1)), sg.Input("8", key=f"START_HOUR", size = (3,1)), 
			sg.Text(":", size = (1,1)), sg.Input("00", key=f"START_MIN", size = (3,1))], 
            [sg.Button("Predict!",key="PREDICT"), sg.Cancel()]] 

	window = sg.Window("Prediction", layout)

	while True:             
		event, values = window.read()

		if event in (sg.WIN_CLOSED, 'Cancel'):
 			break

		if event == "PREDICT":
			model = generate_model()
			prediction = predict(values['BIG_ROAST'], values['SMALL_ROAST'], model)
			text = format_pred(prediction, values['START_HOUR'], values['START_MIN'])
			show_prediction(text)

		window.refresh()
	window.close()

def show_prediction(text):
	layout = [[sg.Text(text)]]
	window = sg.Window("Prediction", layout)
	while True:             
		event, values = window.read()

		if event in (sg.WIN_CLOSED, 'Cancel'):
 			break
		window.refresh()
	window.close()

if __name__ == "__main__":
	#gui = input("do you want a gui? y/n: ")

	#if gui == "y" or gui == "Y":
	create_pred_window()
	#else:
	'''big = input("Thow many big roasts: ")
	small = input("Thow many small roasts: ")

	model = generate_model()
	predictions = predict(big, small, model)

	startHTime = input("start time (hour only, 24 hour time): ")
	startMTime = input("start time (minute only): ")

	result = format_pred(predictions, startHTime, startMTime)

	print(result)'''
