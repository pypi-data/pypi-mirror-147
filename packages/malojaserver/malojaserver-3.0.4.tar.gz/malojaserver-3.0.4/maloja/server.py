# technical
import sys
import os
from threading import Thread
import setproctitle
from importlib import resources
from css_html_js_minify import html_minify, css_minify
import datauri
import time


# server stuff
from bottle import Bottle, static_file, request, response, FormsDict, redirect, BaseRequest, abort
import waitress

# doreah toolkit
from doreah.logging import log
from doreah import auth

# rest of the project
from . import database
from .database.jinjaview import JinjaDBConnection
from .images import resolve_track_image, resolve_artist_image
from .malojauri import uri_to_internal, remove_identical
from .globalconf import malojaconfig, data_dir
from .jinjaenv.context import jinja_environment
from .apis import init_apis, apikeystore


from .proccontrol.profiler import profile


######
### TECHNICAL SETTINGS
#####

PORT = malojaconfig["PORT"]
HOST = malojaconfig["HOST"]
THREADS = 16
BaseRequest.MEMFILE_MAX = 15 * 1024 * 1024

#STATICFOLDER = importlib.resources.path(__name__,"web/static")

webserver = Bottle()

#rename process, this is now required for the daemon manager to work
setproctitle.setproctitle("Maloja")


######
### CSS
#####


def generate_css():
	cssstr = ""
	with resources.files('maloja') / 'web' / 'static' as staticfolder:

		for file in os.listdir(os.path.join(staticfolder,"css")):
			if file.endswith(".css"):
				with open(os.path.join(staticfolder,"css",file),"r") as filed:
					cssstr += filed.read()

	for file in os.listdir(data_dir['css']()):
		if file.endswith(".css"):
			with open(os.path.join(data_dir['css'](file)),"r") as filed:
				cssstr += filed.read()

	cssstr = css_minify(cssstr)
	return cssstr

css = generate_css()



######
### MINIFY
#####

def clean_html(inp):
	return inp

	#if malojaconfig["DEV_MODE"]: return inp
	#else: return html_minify(inp)






######
### ERRORS
#####


@webserver.error(400)
@webserver.error(403)
@webserver.error(404)
@webserver.error(405)
@webserver.error(408)
@webserver.error(500)
@webserver.error(503)
@webserver.error(505)
def customerror(error):
	error_code = error.status_code
	error_desc = error.status
	traceback = error.traceback
	body = error.body or ""
	traceback = traceback.strip() if traceback is not None else "No Traceback"
	adminmode = request.cookies.get("adminmode") == "true" and auth.check(request)

	template = jinja_environment.get_template('error.jinja')
	return template.render(
		error_code=error_code,
		error_desc=error_desc,
		traceback=traceback,
		error_full_desc=body,
		adminmode=adminmode,
	)










######
### REGISTERING ENDPOINTS
#####

aliases = {
	"admin": "admin_overview",
	"manual": "admin_manual",
	"setup": "admin_setup",
	"issues": "admin_issues"
}


### API

auth.authapi.mount(server=webserver)
init_apis(webserver)

# redirects for backwards compatibility
@webserver.get("/api/s/<pth:path>")
@webserver.post("/api/s/<pth:path>")
def deprecated_api_s(pth):
	redirect("/apis/" + pth + "?" + request.query_string,308)

@webserver.get("/api/<pth:path>")
@webserver.post("/api/<pth:path>")
def deprecated_api(pth):
	redirect("/apis/mlj_1/" + pth + "?" + request.query_string,308)




### STATIC

@webserver.route("/image")
def dynamic_image():
	keys = FormsDict.decode(request.query)
	if keys['type'] == 'track':
		result = resolve_track_image(keys['id'])
	elif keys['type'] == 'artist':
		result = resolve_artist_image(keys['id'])

	if result is None or result['value'] in [None,'']:
		return ""
	if result['type'] == 'raw':
		# data uris are directly served as image because a redirect to a data uri
		# doesnt work
		duri = datauri.DataURI(result['value'])
		response.content_type = duri.mimetype
		return duri.data
	if result['type'] == 'url':
		redirect(result['value'],307)

@webserver.route("/images/<pth:re:.*\\.jpeg>")
@webserver.route("/images/<pth:re:.*\\.jpg>")
@webserver.route("/images/<pth:re:.*\\.png>")
@webserver.route("/images/<pth:re:.*\\.gif>")
def static_image(pth):

	ext = pth.split(".")[-1]
	small_pth = pth + "-small"
	if os.path.exists(data_dir['images'](small_pth)):
		resp = static_file(small_pth,root=data_dir['images']())
	else:
		try:
			from pyvips import Image
			thumb = Image.thumbnail(data_dir['images'](pth),300)
			thumb.webpsave(data_dir['images'](small_pth))
			resp = static_file(small_pth,root=data_dir['images']())
		except Exception:
			resp = static_file(pth,root=data_dir['images']())

	#response = static_file("images/" + pth,root="")
	resp.set_header("Cache-Control", "public, max-age=86400")
	resp.set_header("Content-Type", "image/" + ext)
	return resp


@webserver.route("/style.css")
def get_css():
	response.content_type = 'text/css'
	if malojaconfig["DEV_MODE"]: return generate_css()
	else: return css


@webserver.route("/login")
def login():
	return auth.get_login_page()

# old
@webserver.route("/<name>.<ext>")
@webserver.route("/media/<name>.<ext>")
def static(name,ext):
	assert ext in ["txt","ico","jpeg","jpg","png","less","js","ttf"]
	with resources.files('maloja') / 'web' / 'static' as staticfolder:
		response = static_file(ext + "/" + name + "." + ext,root=staticfolder)
	response.set_header("Cache-Control", "public, max-age=3600")
	return response

# new, direct reference
@webserver.route("/static/<path:path>")
def static(path):
	with resources.files('maloja') / 'web' / 'static' as staticfolder:
		response = static_file(path,root=staticfolder)
	response.set_header("Cache-Control", "public, max-age=3600")
	return response



### DYNAMIC

@profile
def jinja_page(name):
	if name in aliases: redirect(aliases[name])
	keys = remove_identical(FormsDict.decode(request.query))

	adminmode = request.cookies.get("adminmode") == "true" and auth.check(request)

	with JinjaDBConnection() as conn:

		loc_context = {
			"dbc":conn,
			"adminmode":adminmode,
			"apikey":request.cookies.get("apikey") if adminmode else None,
			"apikeys":apikeystore,
			"_urikeys":keys, #temporary!
		}
		loc_context["filterkeys"], loc_context["limitkeys"], loc_context["delimitkeys"], loc_context["amountkeys"], loc_context["specialkeys"] = uri_to_internal(keys)

		template = jinja_environment.get_template(name + '.jinja')
		try:
			res = template.render(**loc_context)
		except (ValueError, IndexError):
			abort(404,"This Artist or Track does not exist")

	if malojaconfig["DEV_MODE"]: jinja_environment.cache.clear()

	return clean_html(res)

@webserver.route("/<name:re:admin.*>")
@auth.authenticated
def jinja_page_private(name):
	return jinja_page(name)

@webserver.route("/<name>")
def jinja_page_public(name):
	return jinja_page(name)

@webserver.route("")
@webserver.route("/")
def mainpage():
	return jinja_page("start")


# Shortlinks

@webserver.get("/artist/<artist>")
def redirect_artist(artist):
	redirect("/artist?artist=" + artist)
@webserver.get("/track/<artists:path>/<title>")
def redirect_track(artists,title):
	redirect("/track?title=" + title + "&" + "&".join("artist=" + artist for artist in artists.split("/")))




######
### RUNNING THE SERVER
#####


# warning interception
import logging

class WaitressLogHandler():
	def __init__(self):
		self.lastwarned = 0
		self.barrier = 5
		self.level = 20
		self.filters = []
	def handle(self,record):
		if record.name == 'waitress.queue':
			now = time.time()
			depth = record.args[0]

			if depth > self.barrier:
				log(f"Waitress Task Queue Depth at {depth}")
				self.lastwarned = now
				self.barrier = max(depth,self.barrier+5)
			elif now - self.lastwarned > 5:
				self.barrier = max(5,self.barrier-5)
		else:
			log(f"Waitress: {record.msg % record.args}")
logging.getLogger().addHandler(WaitressLogHandler())


def run_server():
	log("Starting up Maloja server...")

	## start database
	Thread(target=database.start_db).start()



	try:
		#run(webserver, host=HOST, port=MAIN_PORT, server='waitress')
		listen = f"{HOST}:{PORT}"
		log(f"Listening on {listen}")
		waitress.serve(webserver, listen=listen, threads=THREADS)
	except OSError:
		log("Error. Is another Maloja process already running?")
		raise
