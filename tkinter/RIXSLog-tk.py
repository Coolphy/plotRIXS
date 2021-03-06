import os
import h5py
import numpy as np
import csv
import tkinter as tk
import time
# from tkinter import filedialog


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

def get_FileCreateTime(filePath):
    t = os.path.getctime(filePath)
    return TimeStampToTime(t)

def listFile(fileDir):
    list = sorted(os.listdir(fileDir))
    # list.sort(key=lambda fn: os.path.getmtime(fileDir + fn))
    return list


def getInfo(inputpath, filename):

    f = h5py.File(inputpath + "/" + filename, "r")

    PhotonEnergy = round(
        np.mean(f["entry"]["instrument"]["NDAttributes"]["PhotonEnergy"][()]), 2
    )
    PolarMode = np.mean(f["entry"]["instrument"]["NDAttributes"]["PolarMode"][()])
    if PolarMode == 0:
        Polarization = "LH"
    elif PolarMode == 1:
        Polarization = "LV"
    elif PolarMode == 2:
        Polarization = "C+"
    else:
        Polarization = "C-"

    Temp = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleTemp"][()]), 2)

    xx = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleXs"][()]), 3)
    yy = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleYs"][()]), 3)
    zz = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleZ"][()]), 3)
    Tht = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleTheta"][()]), 2)
    Phi = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SamplePhi"][()]), 2)
    Tilt = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleTilt"][()]), 2)

    AcqTime = np.mean(f["entry"]["instrument"]["NDAttributes"]["AcquireTime"][()])
    SplitTime = np.mean(f["entry"]["instrument"]["NDAttributes"]["ExposureSplit"][()])
    ExitSlit = np.mean(f["entry"]["instrument"]["NDAttributes"]["ExitSlit"][()])
    Ring = round(
        np.mean(f["entry"]["instrument"]["NDAttributes"]["BeamCurrent"][()]), 0
    )
    Date = get_FileCreateTime(inputpath + "/" + filename)
    fileInfo = [
        filename[:-6],
        PhotonEnergy,
        Polarization,
        Temp,
        xx,
        yy,
        zz,
        Tht,
        Phi,
        Tilt,
        AcqTime,
        SplitTime,
        ExitSlit,
        Ring,
        Date,
    ]
    return fileInfo


def makeLog(inputpath, outputpath):
    f = open(outputpath + "/logbook.csv", "w", newline="")
    writer = csv.writer(f)
    fileList = listFile(inputpath)
    writer.writerow(
        [
            "Files",
            "Energy(eV)",
            "Polar",
            "Temperature(K)",
            "X(mm)",
            "Y(mm)",
            "Z(mm)",
            "Theta",
            "Phi",
            "Tilt",
            "AcqTime(s)",
            "SplitTime(s)",
            "Slit(um)",
            "RingCurrent",
            "Date",
        ]
    )

    for x in fileList[::3]:
        try:
            writer.writerow(getInfo(inputpath, x))
        except:
            print("file " + str(x) + " is broken!")

    f.close()


def getvalue():
    global inputpath, outputpath
    inputpath = entry1.get()
    outputpath = entry2.get()
    makeLog(inputpath, outputpath)


input = tk.Tk()
input.title("RIXSLog")

L1 = tk.Label(input, text="RIXS data path", font=48)
L1.grid(row=0, column=0, padx=10, pady=5)
entry1 = tk.Entry(input, width=80, font=48)
entry1.grid(row=0, column=1, padx=10, pady=5)
L2 = tk.Label(input, text="LOG save path", font=48)
L2.grid(row=1, column=0, padx=10, pady=5)
entry2 = tk.Entry(input, width=80, font=48)
entry2.grid(row=1, column=1, padx=10, pady=5)
button = tk.Button(input, text="Make it !", font=48, command=getvalue)
button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

# col_count, row_count = input.grid_size()
# for col in range(col_count):
#     input.grid_columnconfigure(col, minsize=250)
# for row in range(row_count):
#     input.grid_rowconfigure(row, minsize=40)

input.mainloop()
