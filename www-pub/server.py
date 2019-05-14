from flask import Flask, render_template, request, abort
from collections import OrderedDict
import data
app = Flask(__name__)

@app.route('/')
def index():
	""" Renders index.html with the latest project """
	#Call load() in the data layer to load the database and store it's contents in the variable db
	db = data.load('data.json')
	#Call search() in the data layer to get a list sorted by end_date in descending order, and pick the first project to get the latest project
	project_lst = data.search(db, sort_by='end_date')
	latest_project = project_lst[0]
	#Render index.html with:
		#latest_project --> used to display information about the latest project
	return render_template('index.html', latest_project=latest_project)

@app.route('/list/')
def list():
	""" Renders list.html based on a set of GET-arguments """
	#Call load() in the data layer to load the database and store it's contents in the variable db
	db = data.load('data.json')
	#If there are GET-arguments:
		#Call search() in the data layer with the arguments and store the results in the variable project_lst
	if request.args:	
		sort_by = request.args.get('sort_by', 'project_id')
		sort_order = request.args.get('sort_order', 'desc')
		techniques = request.args.getlist('techniques')
		if not techniques:
			techniques = None
		search = request.args.get('search', None)
		search_fields = request.args.getlist('search_fields')
		if not search_fields:
			search_fields = None
		project_lst = data.search(db, sort_by=sort_by, sort_order=sort_order, techniques=techniques, search=search, search_fields=search_fields)
	#Else:
		#Store all data in the database, i.e. all projects, in the variable project_lst,
	else:
		project_lst = db
	#Call get_techniques() in the datalayer and store the results in the variable technique_lst
	technique_lst = data.get_techniques(db)
	#Render list.html with:
		#project_lst --> used to display a list of projects
		#technique_lst --> used to display techniques available to filter by in the search-form on the webpage
	return render_template('list.html', project_lst=project_lst, technique_lst=technique_lst)

@app.route('/project/<id>')
def project(id):
	""" Renders project.html based on the <id>-variable """
	#Call load() in the data layer to load the database and store it's contents in the variable db
	db = data.load('data.json')
	#Call get_project() in the data layer and store the project in the variable project
	project = data.get_project(db, id)
	#If None was returned by get_project():
		#No project with the specified ID exists, ergo a nonexistent page has been visited, ergo abort with a 404
	if project is None:
		abort(404)
	else:
		#adding a counter to the project-page.
		counter = open("doc/counter.log", "r+")					#opens counter.log
		count = 1
		pid = str("project ")+str(project['project_id'])+"\n"
		for line in counter:
			if pid in line:
				count += 1
		project['counter'] = count
		counter.write(pid)
		counter.close()
		#Render project.html with:
			#project --> used to display information about the project
		return render_template('project.html', project=project)

@app.route('/techniques/')
def techniques():
	""" Renders techniques.html with all techniques and projects using those techniques """
	#Call load() in the data layer to load the database and store it's contents in the variable db
	db = data.load('data.json')
	#Call data.get_technique_stats() in the data layer, and use OrderedDict(sorted(...)) to get it sorted alphabetically
	tech_stat_dict = data.get_technique_stats(db)
	tech_stat_dict = OrderedDict(sorted(tech_stat_dict.items()))
	#Render techniques.html with:
		#tech_stat_dict --> used to display a list of all techniques, where each items contains another list of all projects using that technique
	return render_template('techniques.html', tech_stat_dict=tech_stat_dict)

@app.errorhandler(404)
def page_not_found(e):
	""" Renders a custom 404 page (error.html) """
	error_msg = "The page you requested does not exist"
	return render_template('error.html', error_num=404, error_msg=error_msg), 404

@app.errorhandler(500)
def server_error(e):
	""" Renders a custom 500 page (error.html) """
	error_msg = "An internal server error occured. Sorry!"
	return render_template('error.html', error_num=500, error_msg=error_msg), 500

#Perform logging to file if application is not in debug mode
if not app.debug:
	import logging
	logging.basicConfig(filename='doc/flask.log',level=logging.INFO)

#Run the application if run as main
if __name__ == "__main__":
	app.run()
