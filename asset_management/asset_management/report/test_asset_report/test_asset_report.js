// Copyright (c) 2022, Lithe-Tech Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Test Asset Report"] = {
	"filters": [
        {
			"fieldname":"asset_category",
			"label": __("Asset Category"),
			"options": "Asset Category",
			"fieldtype": "Link",
			"reqd": 0,
			"width": "100px"
		},
		{
			"fieldname":"location",
			"label": __("Location"),
			"options": "Location",
			"fieldtype": "Link",
			"reqd": 0,
			"width": "100px"
		},
	]
};
