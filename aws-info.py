#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgi
import os
import subprocess
import json

# Enable debugging
import cgitb
cgitb.enable()

# Set the command to use for obtaining AWS information
aws_script='./aws_info.sh'

#
# Function to traverse JSON object and produce an HTML table representation
#  Argument: A valid JSON python object
#  Returns: A string containing an HTML table representation of the argument
#
# Code in this function is a simplified adaptation of json2html located at:
#  https://pypi.python.org/pypi/json2html/0.3
#
def jsonToHTMLTable( json_obj ):
	# Special case to handle a value of "null" appearing in json
	if json_obj == None:
		return "Null"
	
	if (isinstance(json_obj,unicode)):
		return unicode(json_obj)

	if (isinstance(json_obj,int) or isinstance(json_obj,float)):
		return str(json_obj)

	# Special case to handle empty lists
	if (isinstance(json_obj,list)==True) and len(json_obj) == 0:
		return 'None'

	if (isinstance(json_obj,list)==True):
		return '<ul><li>' + '</li><li>'.join([jsonToHTMLTable(child) for child in json_obj]) + '</li></ul>'


	if (isinstance(json_obj,dict)==True):
		table = '<table border="1">'

		for k,v in json_obj.iteritems():
			table = table + '<tr>'
			table = table + '<th>' + str(k) + '</th>'

			# In json, values can be numbers, strings, lists, or
			#  dictionaries. Therefore we will treat each value
			#  as a separate json object.
			table = table + '<td>' + jsonToHTMLTable(v) + '</td>'
			table = table + '</tr>'

		table = table + '</table>'

	return table


# Get the script arguments from the URI used in the request that called this
#  script.
arguments = cgi.FieldStorage()

# Get the hostname and URI for generating links to this script with additonal
#  arguments.
url = os.environ["HTTP_HOST"]
uri = os.environ["REQUEST_URI"]

# Get the referrer so that we can generate a "Back" link
referer = os.environ.get("HTTP_REFERER", "<not present>")

# Generate HTML header
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>AWS Information</title>"
print "</head>"
print "<body>"

# Build the base of all of our links. All of our links are to the current
#  script plus an additional argument with a key of 'service'.
if "service" not in arguments.keys():        
	print "<h2>Please select an AWS service from the list below.</h2>"

        if "?" in uri:
            if arguments.keys():
                link_url_base = '<a href="http://' + url + uri + '&'
            else:
                # Note that this case does not work correctly if the URI is of
                #  the form "aws-info.py?key". Note that this URI has an
                #  invalid argument that consists of a key with no value. For
                #  this reason we will ignore this invalid case for now.
                link_url_base = '<a href="http://' + url + uri
        else:
                link_url_base = '<a href="http://' + url + uri + '?'
                

	# Generate the link table
        print link_url_base + 'service=EC2">EC2 Instances</a><br>'
	print link_url_base + 'service=RDS">RDS DB Instances</a><br>'
        print link_url_base + 'service=ELB">ELB Load Balancers</a><br>'
	print link_url_base + 'service=ECache">ElastiCache Cache Clusters</a><br>'
	print link_url_base + 'service=CF">CloudFormation Stacks</a><br>'

else:
	print "<h2>"

	service = arguments["service"].value

	# Generate the page header
	if service == "EC2":
		print "EC2 Instances"
	elif service == "RDS":
		print "RDS DB Instances"
	elif service == "ELB":
		print "ELB Load Balancers"
	elif service == "ECache":
		print "ElastiCache Cache Clusters"
	elif service == "CF":
		print "CloudFormation Stacks"
	else:
		print "Unknown Service!"
		
	print "</h2>"

	# Generate a "back" link
	print '<a href="' + referer + '">&larr; Back</a><br><br>'

	#
	# Parse json to html
	#
	info = subprocess.check_output(['./aws_info.sh', service])

	if info:
	     json_info = json.loads(info)
	
	     print jsonToHTMLTable(json_info)

	# The following line will add a basic text representation of the json
	#  object to the page. It is left in purely for debugging and sanity
	#  checking of the parsed HTML output.
	#print '<script type="text/javascript">document.write(JSON.stringify(' + info + ', null, "<br>"))</script>'

	#Generate a "back" link
	print '<br><a href="' + referer + '">&larr; Back</a><br>'
	
# Generate HTML footer
print "</body>"
print "</html>"
