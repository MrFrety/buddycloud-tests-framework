import os, sys, json
from flask import Flask, render_template, redirect, url_for, request, make_response

sys.path.append("installation")
sys.path.append("integration")

from installation_tests import test_entries as installation_test_entries
from integration_tests import test_entries as integration_test_entries


test_entries = installation_test_entries + integration_test_entries

test_names = {}
for i in range(len(test_entries)):
	print str(test_entries[i])
	test_names[test_entries[i]['name']] = i


app = Flask(__name__)

@app.route('/')
def index():
	
	return render_template("index.html", domain_url=None)


@app.route('/test_names', methods=['GET'])
def get_test_names():
	
	entries = []
	for entry in test_entries:
		entries.append({
			'name' : entry['name'],
			'continue_if_fail' : entry['continue_if_fail'],
			'source' : entry['source']
		})
	return json.dumps(entries)

@app.route('/perform_test/<test_name>/<path:domain_url>')
def perform_test(test_name=None, domain_url=None):

	json_return = { 'name' : test_name }

	error_msg = None

	if test_name == None or test_name.strip() == "":

		error_msg = "Invalid test name. It cannot be null."
		
	elif test_name not in test_names:

		error_msg = "Invalid test name. There is no such test called "+test_name+"."

	if error_msg != None:

		(exit_status, briefing, message, results) = 2, "Invalid test name!", error_msg
		json_return['exit_status'] = exit_status
		json_return['briefing'] = briefing
		json_return['message'] = message

	else:
	
		(exit_status, briefing, message, results) = test_entries[test_names[test_name]]['test'](domain_url)
		json_return['exit_status'] = exit_status
		json_return['briefing'] = briefing
		json_return['message'] = message


	return json.dumps(json_return)

@app.route('/<path:domain_url>')
def start_tests_launcher(domain_url=None):

	resp = make_response(render_template("index.html", domain_url=domain_url))
	resp.headers['content-type'] = "text/html"
	resp.mimetype = 'text/html'
	return resp

if __name__ == "__main__":
	
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, debug=True)
