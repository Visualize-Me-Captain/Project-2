from flask import Flask, render_template
import os
import csv
 
app = Flask (__name__)
    with open('file.csv') as csvDataFile: csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        print(row)
 
@app.route("/")
def index():
    data = dataset.html
    #return dataset.html
    return render_template('index.html', data=data)
 
if __name__ == "__main__":
    app.run()