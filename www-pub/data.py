import json

def load(filename):
	""" Opens and returns a JSON-formatted file decoded as a python-structure or None if it fails. """
	try:
		with open(filename, encoding="utf-8") as db_file:
			db = json.load(db_file)
			db.sort(key=lambda project: project['project_id'])
		return db
	except:
		return None

def get_project_count(db):
	""" Returns number of projects in db """
	return len(db)

def get_project(db, id):
	""" Returns a project with a specified project_id from db """
	for project in db:
		if str(project['project_id']) == str(id):
			return project
	return None

def search(db, sort_by='start_date', sort_order='desc', techniques=None, search=None, search_fields=None):
	""" Searches the db for a string in all search fields or the specified search fields and returns all
		results that matches the string aswell as, if supplied, required techniques, sorted by the specified
		field in the specified order. """ 
	#initate a empty list to store results in
	results = []
	#if <search> is none, set <search> to an empty string to match all projects
	if search is None:
		search = ''
	#iterate over all projects in the database
	for project in db:
		#if the <techniques> variable is not None:
			#iterate over all the techniques in <techniques> and if one of the techniques
			#does not exist in the currently iterated project, continue to the next project iteration
		if techniques is not None:
			ok = True
			for tech in techniques:
				if tech not in project['techniques_used']:
					ok = False
					break
			if not ok:
				continue
		#if <search_fields> is None, set <search_fields> to all fields (keys) in the currently iterated project
		if search_fields is None:
			search_fields = [field for field in project]
		#iterate over all search fields
		for field in search_fields:
			#if the search_field exists in the project
			#compare its contents to the <search>-variable, and append it to <results> if it matches
			try:
				if type(project[field]) is list:
					for item in project[field]:
						if search.lower() in str(item).lower():
							results.append(project)
							break
					else: continue #else = if not breaked, continue to next field in project.
					break # if breaked, stop searching in this project to avoid duplicates.
				elif search.lower() in str(project[field]).lower():
					results.append(project)
					break #stop searching in this project to avoid duplicates
			#if the search field did not exist in the project, do nothing
			except KeyError:
				pass
	try:
		#sort the list according to the specified sorting parameters
		reverse = True if sort_order=='desc' else False
		results.sort(key=lambda project: project[sort_by], reverse=reverse)
	except KeyError:
		pass #dont sort if sort_by is invalid
	return results

def get_techniques(db):
	""" Returns all techniques ever used by the projects in db sorted by name """
	tech_list = []
	for project in db:
		for tech in project['techniques_used']:
			if tech not in tech_list:
				tech_list.append(tech)
	tech_list.sort(key=lambda tech: tech.lower()) #sort on lower because 'aBb', is more natural than 'Bab'
	return tech_list

def get_technique_stats(db):
	""" Returns all techniques used by the projects in db with the id and name of the projects that utilizes the technique """
	tech_stat_dict = {}
	for project in db:
		for tech in project['techniques_used']:
			if tech not in tech_stat_dict:
				tech_stat_dict[tech] = []
			tech_stat_dict[tech].append({'id': project['project_id'], 'name': project['project_name']})
	return tech_stat_dict
