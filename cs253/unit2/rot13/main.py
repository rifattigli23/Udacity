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
import webapp2
from inputValidation import valid_day, valid_month, valid_year
from html_util import escape_html
import string

header="""
<!DOCTYPE html>
<html>
  <head>
    <title>Unit 2 Rot 13</title>
  </head>
  <body>
    <h2>Enter some text to ROT13:</h2>
"""

form="""
<form method="post">
    <textarea name="text" 
              style="height: 100px; width: 400px;">%(text)s</textarea>
    <br>
    <input type="submit">
</form>
"""

footer="""
  </body>
</html>
"""

class MainHandler(webapp2.RequestHandler):
    def rot13(self, text):
        upper="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lower="abcdefghijklmnopqrstuvwxyz"
        text = list(text)
        for idx, val in enumerate(text):
            lowerIndex = lower.find(val)
            upperIndex = upper.find(val)
            if lowerIndex <> -1:
                text[idx] = lower[(lowerIndex+13)%26]
            elif upperIndex <> -1:
                text[idx] = upper[(upperIndex+13)%26]
                     
        return "".join(text)
        
    def write_form(self, text=""):
        self.response.out.write(header)
        self.response.out.write(form % {"text": escape_html(text)})
        self.response.out.write(footer)
    
    def get(self):
        self.write_form()
    
    def post(self):        
        text = self.request.get('text')
        text = self.rot13(text)
        self.write_form(text)
        
app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)
