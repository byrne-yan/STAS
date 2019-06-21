DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS candidate;

CREATE TABLE user(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL
);

CREATE TABLE candidate(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	code TEXT UNIQUE NOT NULL
);

CREATE TABLE stock(
	ts_code TEXT PRIMARY KEY,
	symbol 	TEXT NOT NULL,
	name TEXT NOT NULL,
	area TEXT NOT NULL,
	industry TEXT NOT NULL,
	fullname TEXT NOT NULL,
	enname 	TEXT NOT NULL,
	market 	TEXT NOT NULL,
	exchange TEXT NOT NULL, --  SSE上交所 SZSE深交所 HKEX港交所
	curr_type TEXT NOT NULL,
	list_status CHARACTER , 	-- 	上市状态： L上市 D退市 P暂停上市
	list_date 	DATE,  	
	delist_date DATE, 	
	is_hs 	CHARACTER -- 	N H S	
}

CREATE TABLE kseries(
	ts_code TEXT PRIMARY KEY,
	symbol 	TEXT NOT NULL,
	open FLOAT NOT NULL,
	high FLOAT NOT NULL,
	low FLOAT NOT NULL,
	close FLOAT NOT NULL,
)


