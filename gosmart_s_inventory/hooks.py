app_name = "gosmart_s_inventory"
app_title = "Gosmart S Inventory"
app_publisher = "Gharieb Khalifa"
app_description = "A Simple Inventory Manager App"
app_email = "blacksnow.soon@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []
fixtures = [
    "Translation",
    "Website Settings",
    "Navbar Settings",
    "Print Settings",
    "Navbar Settings",
    {
        "dt": "Email Account", "filters": {
            "name": ["=", "Go Smart Inventory Management"]
        }
    },
    {
        "dt":"Role", "filters" : { 
            "name":["in", [
                "Inventory Viewer",
                "Inventory User",
                "Inventory Manager",
                
            ]]
        }
    },
    {
        "dt": "Custom DocPerm", "filters": {
            "role": ["in", [
                "Inventory Viewer",
                "Inventory User",
                "Inventory Manager",
            ]]  
        }
    }
]
# Each item in the list will be shown as an app in the apps page
add_to_apps_screen = [
	{
		"name": "gosmart_s_inventory",
		"logo": "/assets/gosmart_s_inventory/favicon-32x32.png",
		"title": "Gosmart Simple Inventory Manager",
		"route": "/",
# 		"has_permission": "gosmart_s_inventory.api.permission.has_app_permission"
	}
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = ["/assets/gosmart_s_inventory/css/gosmart_s_inventory.css"]
app_include_js = ["/assets/gosmart_s_inventory/js/gosmart_s_inventory.js"]

# include js, css files in header of web template
# web_include_css = "/assets/gosmart_s_inventory/css/gosmart_s_inventory.css"
# web_include_js = "/assets/gosmart_s_inventory/js/gosmart_s_inventory.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "gosmart_s_inventory/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "gosmart_s_inventory/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"
home_page = "/home_page/"
# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "gosmart_s_inventory.utils.jinja_methods",
# 	"filters": "gosmart_s_inventory.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "gosmart_s_inventory.install.before_install"
# after_install = "gosmart_s_inventory.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "gosmart_s_inventory.uninstall.before_uninstall"
# after_uninstall = "gosmart_s_inventory.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "gosmart_s_inventory.utils.before_app_install"
# after_app_install = "gosmart_s_inventory.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "gosmart_s_inventory.utils.before_app_uninstall"
# after_app_uninstall = "gosmart_s_inventory.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "gosmart_s_inventory.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"gosmart_s_inventory.tasks.all"
# 	],
# 	"daily": [
# 		"gosmart_s_inventory.tasks.daily"
# 	],
# 	"hourly": [
# 		"gosmart_s_inventory.tasks.hourly"
# 	],
# 	"weekly": [
# 		"gosmart_s_inventory.tasks.weekly"
# 	],
# 	"monthly": [
# 		"gosmart_s_inventory.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "gosmart_s_inventory.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "gosmart_s_inventory.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "gosmart_s_inventory.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["gosmart_s_inventory.utils.before_request"]
# after_request = ["gosmart_s_inventory.utils.after_request"]

# Job Events
# ----------
# before_job = ["gosmart_s_inventory.utils.before_job"]
# after_job = ["gosmart_s_inventory.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"gosmart_s_inventory.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

