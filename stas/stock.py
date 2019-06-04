from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

import tushare as ts
from stas.db import get_db
from stas.auth import login_required

bp = Blueprint('stock', __name__)

@bp.route('/')
@login_required
def index():
	pro = ts.pro_api()
	stocks = pro.stock_basic(list_status='L')
	if stocks is not None:
		return render_template('stock/index.html', stocks=stocks)
	flash('No stocks')