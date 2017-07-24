#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

env = jinja2.Environment(loader = jinja2.FileSystemLoader("templates"))

def getUserInfo(path):
    cur_user = users.get_current_user()
    log_url = ''
    if cur_user:
        log_url = users.create_logout_url(path)
        name = cur_user.nickname().split('@')[0]
    else:
        log_url = users.create_login_url(path)
        name = 'none'
    return {
        "log_url": log_url,
        "user": cur_user,
        "username": name
    }

class User(ndb.Model):
    name = ndb.StringProperty()



class MainHandler(webapp2.RequestHandler):
    def get(self):
        my_vars = getUserInfo('/')
        temp = env.get_template("homepage.html")
        self.response.out.write(temp.render(my_vars))

class DiscussionPage(webapp2.RequestHandler):
    def get(self):
        my_vars = getUserInfo('/discuss')
        temp = env.get_template("discussion.html")
        self.response.out.write(temp.render(my_vars))

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        my_vars = getUserInfo('/')
        temp = env.get_template("user_profile.html")
        self.response.out.write(temp.render(my_vars))

class EditProfile(webapp2.RequestHandler):
    def get(self):
        my_vars = getUserInfo('/')
        temp = env.get_template("edit_profile.html")
        self.response.out.write(temp.render(my_vars))

class MyProfile(webapp2.RequestHandler):
    def get(self):
        my_vars = getUserInfo('/profile')
        user = my_vars['user']
        if user:
            self.redirect('/profile')
        else:
            self.redirect('/')

class AllProfilesPage(webapp2.RequestHandler):
    def get(self):
        my_vars = getUserInfo('/all_profiles')
        temp = env.get_template("all_profiles.html")
        self.response.out.write(temp.render(my_vars))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/discuss', DiscussionPage),
    ('/profile', ProfileHandler),
    ('/profile/edit', EditProfile),
    ('/all_profiles', AllProfilesPage),

    ('/my_profile', MyProfile),
], debug=True)
