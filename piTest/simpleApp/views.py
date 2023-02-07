from django.shortcuts import render
from django.http import HttpResponse
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import os
import json
from web3 import Web3, EthereumTesterProvider
from web3.middleware import geth_poa_middleware
from urllib.request import urlopen

addressContract = "0xF21a8dfb7F01792802d4a0d0C9905e01fc5A9672"


def getBatteryFromRFID(rfid):
    w3 = Web3(Web3.HTTPProvider('https://polygon-mumbai.infura.io/v3/c87232efea3046708a204b8abf889cb3'))
    w3.isConnected()
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    abi = json.load(open('../abi.json'))
    contract_instance = w3.eth.contract(address=addressContract, abi=abi)

    res = contract_instance.functions.rfidToBattery(rfid).call()
    battery_info = contract_instance.functions.getBatteryById(int(res)).call()
    battery_percentage = contract_instance.functions.getBatteryPercentage(int(res)).call
    return (battery_info,battery_percentage)
# Create your views here.

def getBatteriesByStation(station_id):
    w3 = Web3(Web3.HTTPProvider('https://polygon-mumbai.infura.io/v3/c87232efea3046708a204b8abf889cb3'))
    w3.isConnected()
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    abi = json.load(open('../abi.json'))
    contract_instance = w3.eth.contract(address=addressContract, abi=abi)
 
    res = contract_instance.functions.getBatteriesByStation(station_id).call()
    batteriesInfo = []
    for i in res:
        temp = {}
        batteryVal = contract_instance.functions.batteries(i).call()

        temp['id'] = batteryVal[0]
        temp['batteryPercentage'] = batteryVal[1]
        temp['lastBlocktime'] = batteryVal[2]
        temp['status'] = batteryVal[3]
        temp['currentStation'] = batteryVal[4]
        temp['currentUser'] = batteryVal[5]
        temp['metaABI'] = batteryVal[6]
        url = "https://gateway.ipfscdn.io/ipfs/"+temp['metaABI']

        response = urlopen(url)
        data_json = json.loads(response.read())

        temp['name'] = data_json['battery']['name']
        temp['capacity'] =  data_json['battery']['capacity']
        temp['current'] =  data_json['battery']['current']
        temp['voltage'] =  data_json['battery']['voltage']
        temp['maxTemperature'] =  data_json['battery']['maxTemperature']
        temp['company'] =  data_json['battery']['company']
        temp['dateOfManufacture'] =  data_json['battery']['dateOfManufacture']
        batteriesInfo.append(temp)
    # print(batteriesInfo)
    return res, batteriesInfo

def index(request):
    return render(request, 'simpleApp/index.html', {'counter': request.session['counter']})
    # if request.method == "POST":
    #   try:
    #      request.session['count'] +=1
    #   except:
    #      request.session['count'] = 0
    # else :
    #   request.session['count'] = 0
    #   return render(request, 'simpleApp/index.html')

def select(request):
    if request.method == "POST":
        try:
            request.session['counter'] +=1
        except:
            request.session['counter'] = 0
    else :
        request.session['counter'] = 0
        return render(request, 'simpleApp/select.html')

    return render(request, 'simpleApp/select.html', {'counter': request.session['counter']})

def scan(request):
    if request.method == "POST":
        reader = SimpleMFRC522()
        try:
            id, text = reader.read()
            idProc = hex(id)[2:-2]
            print(idProc)
            print(os.getcwd())
            batteryInfo = getBatteryFromRFID(idProc)
        finally:
            GPIO.cleanup()
            return render(request, 'simpleApp/battery.html',{"id":batteryInfo[0][0],"percentage":100, "inStation":batteryInfo[0][3], "station":batteryInfo[0][4],"user":batteryInfo[0][5],})

    return render(request, 'simpleApp/scan.html', {'scanned': True})

def battery(request):
    return render(request, 'simpleApp/battery.html')

def batteries(request):
    batteries, batteriesInfo = getBatteriesByStation(1)
    return render(request, 'simpleApp/batteries.html', {'batteries':batteries, 'batteriesInfo':batteriesInfo})