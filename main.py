import webapp2
import os
import re

page_header = """
<!DOCTYPE html>
<html>
    <head>
        <style>
            .error {
                color:red;
            }
        </style>
    </head>
    <body>
        <h1>User Sign-up:</h1>
"""

page_footer = """
    </body>
</html>
"""


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)


class Signup(webapp2.RequestHandler):
    def get(self):

        error1 = self.request.get("error1")
        error2 = self.request.get("error2")
        error3 = self.request.get("error3")
        error4 = self.request.get("error4")

        signup_form = """
        <form method="post">
            <table>
                <tr>
                    <td class="label">
                        Username
                    </td>
                    <td>
                        <input type="text" name="user-name" value="" required>
                    </td>
                    <td class="error">
                        {user_name_error}
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        Password
                    </td>
                    <td>
                        <input type="password" name="pass-word" value="" required>
                    </td>
                    <td class="error">
                        {pass_word_error}
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        Verify Password
                    </td>
                    <td>
                        <input type="password" name="verify-pw" required>
                    </td>
                    <td class="error">
                        {pass_word_match}
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        Email (optional)
                    </td>
                    <td>
                        <input type="email" name="e-mail" value="">
                    </td>
                    <td class="error">
                        {email_error}
                    </td>
                </tr>
            </table>
            <input type="submit"/>
        </form>
        """.format(user_name_error = error1, pass_word_error = error2, pass_word_match = error3, email_error = error4)

        content = page_header + signup_form + page_footer
        self.response.write(content)

    def post(self):
        error1 = ""
        error2 = ""
        error3 = ""
        error4 = ""
        hasError=False
        username = self.request.get("user-name")
        password = self.request.get("pass-word")
        verify = self.request.get("verify-pw")
        email = self.request.get("e-mail")

        if not valid_username(username):
            error1 = "That's not a valid username."
            hasError=True

        if not valid_password(password):
            error2 = "Invalid password."
            hasError=True

        elif password != verify:
            error3 = "Your passwords didn't match."
            hasError=True

        if not valid_email(email):
            error4 = "That's not a valid email address."
            hasError=True

        error = "/?error1=" + error1 + "&error2=" + error2 + "&error3=" + error3 + "&error4=" + error4
        if hasError:
            self.redirect(error)
        else:
            self.redirect("/welcome?username=" + username)


class Welcome(webapp2.RequestHandler):
    def get(self):
        new_user_name = self.request.get("username")
        content = "<h1>" + "Welcome, " + new_user_name + "!" + "</h1>"
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', Signup),
    ('/welcome', Welcome)
], debug=True)
