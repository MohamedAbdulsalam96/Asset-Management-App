# Copyright (c) 2022, Lithe-Tech Limited and contributors
# For license information, please see license.txt

import datetime
import frappe
from frappe import _



def execute(filters=None):
	if not filters:
		filters = {}
	#columns, data = [], []
	today = datetime.date.today()
	year = today.year-2
	year2 = today.year-1
	year3 = today.year
	

	columns = get_columns(year, year2, year3)
	#years = frappe.db.sql("""SELECT DISTINCT YEAR(transaction_date) FROM `tabAsset Movement`""")
	#list_years = list(years.values())
	#columns.append(str(years[1][0]))
	data = get_data(filters, year, year2, year3)
	return columns, data


def get_columns(year, year2, year3):

	return [
		_("ID") + ":Data/:120",
		_("S/L") + ":Data/:120",
		_("Item Name") + ":Link/Item:120",
		_("Brand") + ":Link/Item:120",
		_("Model") + ":Link/Item:120",

		
		_("Purchase Date") + ":Date/Asset:120",
		_("Asset Number") + ":Data/Asset:120",
		

		
		_(str(year)+" Location") + ":Data/Asset:120",
		_(str(year)+" Condition") + ":Data/Asset Repair:120",

		_(str(year2)+" Location") + ":Data/Asset:120",
		_(str(year2)+" Condition") + ":Data/Asset Repair:120",

		_(str(year3)+" Location") + ":Data/Asset:120",
		_(str(year3)+" Condition") + ":Data/Asset Repair:120",

		_("Remark") + ":Data/Asset:120",




	]
	# year  = 2 years Back
	# year2 = Previous year
	# year3 = Existing year


def get_data(filters=None, year=None, year2=None, year3=None):
		
	conditions, filters = get_conditions(filters)


	# result = frappe.db.sql("""select a.name, a.serial_number, a.item_name, i.brand, i.description, a.purchase_date, a.asset_name,   d2020.%s, c2020.condition, d2021.%s, c2021.condition, d2022.%s, c2022.condition, a.remark  from tabAsset a 
	# left join tabItem i on a.item_code = i.item_code
	# left Join  (select asset, failure_date, repair_status, CASE WHEN repair_status='Pending' THEN 'NOT OK' WHEN repair_status = 'Damage' THEN 'DAMAGE' WHEN repair_status = 'Disposal' THEN 'DISPOSAL' ELSE 'OK' END AS 'condition' from `tabAsset Repair` where YEAR(failure_date)=%s ORDER BY failure_date) as c2022 on a.name = c2022.asset
	# left Join  (select asset, failure_date, repair_status, CASE WHEN repair_status='Pending' THEN 'NOT OK' WHEN repair_status = 'Damage' THEN 'DAMAGE' WHEN repair_status = 'Disposal' THEN 'DISPOSAL' ELSE 'OK' END AS 'condition' from `tabAsset Repair` where YEAR(failure_date)=%s ORDER BY failure_date) as c2021 on a.name = c2021.asset
	# left Join  (select asset, failure_date, repair_status, CASE WHEN repair_status='Pending' THEN 'NOT OK' WHEN repair_status = 'Damage' THEN 'DAMAGE' WHEN repair_status = 'Disposal' THEN 'DISPOSAL' ELSE 'OK' END AS 'condition' from `tabAsset Repair` where YEAR(failure_date)=%s ORDER BY failure_date) as c2020 on a.name = c2020.asset
	# left Join  (select a.name, ami.target_location '%s' from tabAsset a join `tabAsset Movement Item` ami on a.name = ami.asset join `tabAsset Movement` am on ami.parent = am.name where YEAR(am.transaction_date)=%s order by am.transaction_date) as d2020 on a.name = d2020.name
	# left join  (select a.name, ami.target_location '%s' from tabAsset a join `tabAsset Movement Item` ami on a.name = ami.asset join `tabAsset Movement` am on ami.parent = am.name where YEAR(am.transaction_date)=%s order by am.transaction_date) as d2021  on a.name = d2021.name
	# left join  (select a.name, ami.target_location '%s' from tabAsset a join `tabAsset Movement Item` ami on a.name = ami.asset join `tabAsset Movement` am on ami.parent = am.name where YEAR(am.transaction_date)=%s order by am.transaction_date) as d2022  on a.name = d2022.name %s
	# """% (year, year2, year3, year3, year2, year, year, year, year2, year2,  year3, year3, conditions))
	
	# return result

	result = frappe.db.sql("""select a.name, a.serial_number, a.item_name, i.brand, i.description, a.purchase_date, a.asset_name,   lc_2.target_location lc_2, cc_2.condition cc_2, lc_1.target_location lc_1, cc_1.condition cc_1, lc.target_location lc, cc.condition cc, a.remark  from tabAsset a 
	left join tabItem i on a.item_code = i.item_code
	left Join  (SELECT * FROM (	
	select asset, failure_date, repair_status, CASE WHEN repair_status='Pending' THEN 'NOT OK' WHEN repair_status = 'Damage' THEN 'DAMAGE' WHEN repair_status = 'Disposal' THEN 'DISPOSAL' ELSE 'OK' END AS 'condition', ROW_NUMBER() OVER (PARTITION BY asset ORDER BY failure_date DESC) as n
 	from `tabAsset Repair` where YEAR(failure_date)=%s) as X WHERE n <= 1) as cc on a.name = cc.asset
	left Join  (SELECT * FROM (	
	select asset, failure_date, repair_status, CASE WHEN repair_status='Pending' THEN 'NOT OK' WHEN repair_status = 'Damage' THEN 'DAMAGE' WHEN repair_status = 'Disposal' THEN 'DISPOSAL' ELSE 'OK' END AS 'condition', ROW_NUMBER() OVER (PARTITION BY asset ORDER BY failure_date DESC) as n
 	from `tabAsset Repair` where YEAR(failure_date)=%s) as X WHERE n <= 1) as cc_1 on a.name = cc_1.asset
	left Join (SELECT * FROM (	
	select asset, failure_date, repair_status, CASE WHEN repair_status='Pending' THEN 'NOT OK' WHEN repair_status = 'Damage' THEN 'DAMAGE' WHEN repair_status = 'Disposal' THEN 'DISPOSAL' ELSE 'OK' END AS 'condition', ROW_NUMBER() OVER (PARTITION BY asset ORDER BY failure_date DESC) as n
 	from `tabAsset Repair` where YEAR(failure_date)=%s) as X WHERE n <= 1) as cc_2 on a.name = cc_2.asset
	
	left Join (SELECT * FROM ( select a.name, ami.target_location, ROW_NUMBER() OVER (PARTITION BY asset order by am.transaction_date desc) as n from tabAsset a join `tabAsset Movement Item` ami on a.name = ami.asset join `tabAsset Movement` am on ami.parent = am.name where YEAR(am.transaction_date)=%s) as X where n <= 1) as lc on a.name = lc.name
	
	left join (SELECT * FROM ( select a.name, ami.target_location, ROW_NUMBER() OVER (PARTITION BY asset order by am.transaction_date desc) as n from tabAsset a join `tabAsset Movement Item` ami on a.name = ami.asset join `tabAsset Movement` am on ami.parent = am.name where YEAR(am.transaction_date)=%s) as X where n <= 1) as lc_1  on a.name = lc_1.name
	
	left join (SELECT * FROM ( select a.name, ami.target_location, ROW_NUMBER() OVER (PARTITION BY asset order by am.transaction_date desc) as n from tabAsset a join `tabAsset Movement Item` ami on a.name = ami.asset join `tabAsset Movement` am on ami.parent = am.name where YEAR(am.transaction_date)=%s) as X where n <= 1) as lc_2  on a.name = lc_2.name %s
	"""% (year3, year2, year, year3, year2, year, conditions))
	return result



def get_conditions(filters):
	conditions="" 
	if filters.get("asset_category"): conditions += "where a.asset_category = '%s'" % filters["asset_category"]
	if filters.get("location"): conditions += "and a.location = '%s'" % filters["location"]
	
	return conditions, filters



