app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

#app.secret_key = 'Yuelin'

##Authenicate
# oAuth 2.0 Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id="122252126585-ibobp8jrclfnm15ie3tsfj3ac23cuv69.apps.googleusercontent.com",
    client_secret="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",
    jwks_uri= "https://www.googleapis.com/oauth2/v3/certs",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v2/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)


@app.route('/')
#@login_required
def loginFunction():
    email = dict(session).get('email',None)
    
    return f'Hello, you are logge in as {email}!'


@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['profile'] = user_info
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


    #backup file

    #SQLALchemy Database
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False,unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #Create A String
    def __repr__(self):
        return '<Name %r>' % self.name

class UserForm(FlaskForm):
    from flask_wtf import FlaskForm
    name = StringField("Please input Your name",validators=[DataRequired()])
    email = StringField("Email",validators=[DataRequired()])
    submit = SubmitField("Submit")


class NamerForm(FlaskForm):
    name = StringField("Please input Your name",validators=[DataRequired()])
    #email = StringField("Email",validators=[DataRequired()])
    submit = SubmitField("Submit")
@app.route('/name', methods=['GET','POST'])
def name():
    from flask_wtf import FlaskForm
    name = None
    form = NamerForm()
    
    #validate form
    #if form.validate_on_sumbit():
        #name = form.name.data
        #form.name.data =''
    return render_template("name.html",name =name, form = form)

@app.route('/user/add', methods=['GET','POST'])
def add_user():
    return render_template("add_user.html")
