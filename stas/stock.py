from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, make_response
)
from werkzeug.exceptions import abort

import tushare as ts
from stas.db import get_db
from stas.auth import login_required
from datetime import ( datetime, timedelta)
import time

ts.set_token('3aa33d14d53a936cb206ec55f8ebdb6f647dd1e6dca3785ab1632ee5')
bp = Blueprint('stock', __name__,url_prefix='/stock')

@bp.route('/')
@login_required
def index():
	pro = ts.pro_api()
	sse_index = pro.index_basic(market='SSE')
	stocks = pro.stock_basic(list_status='L')
	if stocks is not None and index is not None:
		return render_template('stock/index.html', stocks=stocks, index = sse_index)
	flash('No stocks')
	
@bp.route('/quote')
@login_required
def quote():
	
	ts_code = request.values['code']
	isindex  = request.values['index']
	if ts_code is not None:
		#q = pro.daily(ts_code=ts_code)
		if isindex is None:
			return render_template('stock/quote_hs.html',code=ts_code)
		else:
			return render_template('stock/quote_hs.html',code=ts_code, index = isindex)
	
	#flash('Stock code needed.')

@bp.route('/data')
@login_required	
def data():
	ts_code = request.values['code']
	#isindex = request.values['index']
	asset = 'E'
	if request.values['index']:
		asset = 'I'
	if ts_code is not None:
		pro = ts.pro_api()
		try:
			e_date = datetime.today()
			delta2y = timedelta(365*2)
			min30 = None
			count = 2
			while True:
				s_date = e_date - delta2y
				q = ts.pro_bar(ts_code=ts_code,asset=asset,freq='30min', start_date=s_date.strftime('%Y%m%d'), end_date=e_date.strftime('%Y%m%d'), ma=[5,13,21,34,55,89,144,233])
				if q is None or q.size==0:
					break
				if min30 is None:
					min30 = q
				else:
					min30 = min30.append(q,ignore_index=True)
				e_date = s_date
				print(e_date.isoformat()+"!")
				print(min30.size)
				count -= 1
				if count<2: 
					break
				time.sleep(12)
			
			# if isindex:
				# q = pro.index_daily(ts_code=ts_code)
			# else:
				# q = pro.daily(ts_code=ts_code)
			
			#print(min30.columns.values)	
			if min30:
				return jsonify({
						"columns":str(min30.columns.values),
						"data":min30.to_json(orient='values')
						})
				
			return jsonify({"error":"no data"})
			
		except Exception as e:
			return jsonify({"error":"Error:"+str(e)})
	return jsonify({"error":"Stock code needed."})

