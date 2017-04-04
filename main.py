import os
import jinja2
import webapp2
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
print template_dir
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape= True)


class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
		
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))


class MainPage(Handler):
	def get(self):
		self.render("home.html")
	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')
		verify_password = self.request.get('verify')
		email = self.request.get('email')
		usernameV = valid_username(username)
		passwordV = vaild_password(password)
		verifyV = valid_verify(password,verify_password)
		emailV = vaild_email(email)

		error_data = False
		params = dict(username = username, email = email)
		
		if not(usernameV):
			params['errorUsername'] = "That's not a valid username."
			error_data = True
		if not(passwordV):
			params['errorPassword'] = "That wasn't a valid password."
			error_data = True
		else:
			if password != verify_password:
				params['errorVerify'] = "Your passwords didn't match."
				error_data = True
		if not(emailV):
			params['errorEmail'] = "That's not a valid email."
			error_data = True

		if error_data:
			self.render("home.html", **params)
		else:
			self.redirect('/welcome?username=' + username)
			

class WelcomeHandler(Handler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/')
app = webapp2.WSGIApplication([('/', MainPage), ('/welcome', WelcomeHandler)], debug = True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return USER_RE.match(username)

PAS_RE = re.compile(r"^.{3,20}$")
def vaild_password(password):
	return PAS_RE.match(password)
def valid_verify(password, verify):
	if vaild_password(password):
		return True
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def vaild_email(email):
	if len(email) == 0:
		return True
	else:
		return EMAIL_RE.match(email)