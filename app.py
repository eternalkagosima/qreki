#!/usr/bin python3
# -*- coding: utf-8 -*-

# flask run
# localhost:5000/?year=2021&month=2&day=25
# {"day":14,"leap_month":0,"month":1,"rokuyou":"\u53cb\u5f15","year":2021}

from flask import Flask, jsonify, make_response, request
import json
from qreki import Kyureki
from datetime import datetime,timedelta,timezone
import calendar

app = Flask(__name__)
JST = timezone(timedelta(hours=+9),'JST')
now = datetime.now(JST)
nyear = now.year
nmonth = now.month
nday = now.day
# qrk = Kyureki(nyear,nmonth,0,nday)
ret = []

def calcDay(y,m,d):
	qrk = Kyureki(y,m,0,d)
	qstr = Kyureki.from_ymd(y,m,d)
	result = {
		'date': str.format("{0}/{1}/{2}",y,m,d),
		'qreki': {
			'year': 	qstr[0],
			'month':	qstr[1],
			'leap_month':	qstr[2],
			'day':		qstr[3],
			'rokuyou':	qrk.ROKUYOU[(int(qstr[1])+int(qstr[3])) % 6]
		}
	}
	return result

def calcMonth(y,m):
	lastD = calendar.monthrange(y,m)[1] + 1
	# print("/",lastD,"/")
	resp = []
	for d in range(1,lastD):
		resp.append(calcDay(y,m,d))
	return resp

def calcYear(y):
	resp = []
	for m in range(1,13):
		# print("/",m,"/")
		resp.append(calcMonth(y,m))
	return resp

@app.route('/', methods=['GET'])
def calcRoku():
	ret = []
	
	#今日で計算
	# print("year=/",request.args.get("year"),"/")
	# print("month=/",request.args.get("month"),"/")
	# print("day=/",request.args.get("day"),"/")
	if request.args.get("year") is  None:
		ret.append(calcDay(nyear,nmonth,nday))
		return make_response(jsonify(ret))
	else:
		year = int(request.args.get("year",""))
		# print("year=/",year,"/")
		#年があって月がなければ年間計算 月単位に配列にする
		if request.args.get("month") is None:
			ret.append(calcYear(year))
			return make_response(jsonify(ret))
		else:
			month = int(request.args.get("month",""))
			if month not in range(1,13): return make_response(jsonify(ret))
			# print("month=/",month,"/")
			#年があって月があって日がなければ月間計算 月単位に配列にする
			if request.args.get("day") is None:
				ret.append(calcMonth(year,month))
				return make_response(jsonify(ret))
			else:
				day = int(request.args.get("day",""))
				if day not in range(1,32): return make_response(jsonify(ret))
				# print("day=/",day,"/")
				#年も月も日もあればその日を計算
				ret.append(calcDay(year,month,day))
				return make_response(jsonify(ret))
			
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000,debug=True)