from flask import Flask, render_template, request, make_response, redirect, url_for, session
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
import authomatic
import dbfunc

# Instantiate Authomatic.
# authomatic = Authomatic(CONFIG, 'your secret string', report_errors=False)

app = Flask(__name__, template_folder='.')
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/koffiepunten', methods=['GET', 'POST'] )
def koffiepunten():
    message = ''
    goednieuws = ''
    punten = 0
    if request.method == 'POST':
        paknummer = request.form.get('paknummer')
        if paknummer != "":
            statuscode, status_tekst = dbfunc.db_ClaimPunten(session['id'], session['oauth_provider'], int(paknummer))
            if statuscode == 1:
                message = status_tekst
            else:
                goednieuws = "er zijn " + str( status_tekst) + " toegevoegd"
    punten = dbfunc.db_GetPunten(session['id'], session['oauth_provider'])
    return render_template('koffiepunten.html', message=message, punten=punten, goednieuws=goednieuws)

@app.route('/login', methods=['GET', 'POST'])
def login():
    mislukt = ""
    if request.method == 'POST':
        Username = request.form.get('Username')
        Password = request.form.get('Password')
        
        #login Gijs
        if Username == "Gijs" and Password == "Mijn kamer is een troep!":
            id = 1
            Firstname = "Gijs"
            Lastname = "Schouten"
            Email = "gaatjeniksaan@anoniem.com"
            Provider = "Static"

            session['id'] = id
            session['name'] = Username
            session['first_name'] = Firstname
            session['last_name'] = Lastname
            session['email'] = Email
            session['oauth_provider'] = provider
            exists = dbfunc.db_UserExist(id, provider)
            if exists == 1:
                dbfunc.db_makeUser(Username, Firstname, Lastname, Email, id, provider)
            return redirect(url_for('index'))
        
        #login Joerie
        if Username == "Joerie" and Password == "Mijn kamer is opgeruimt!":
            id = 2
            Firstname = "Joerie"
            Lastname = "van der Meer"
            Email = "gaatjeniksaan@anoniem.com"
            Provider = "Static"

            session['id'] = id
            session['name'] = Username
            session['first_name'] = Firstname
            session['last_name'] = Lastname
            session['email'] = Email
            session['oauth_provider'] = provider
            exists = dbfunc.db_UserExist(id, provider)
            if exists == 1:
                dbfunc.db_makeUser(Username, Firstname, Lastname, Email, id, provider)
            return redirect(url_for('index'))
        
        else:
            mislukt = True
    return render_template('login.html', mislukt=mislukt)

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/logout')
def lougout():
    session.clear()
    return redirect(url_for('index'))

# Run the app on port 5000 on all interfaces, accepting only HTTPS connections
if __name__ == '__main__':
    dbfunc.db_connection('127.0.0.1', 27017)
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, ssl_context='adhoc', host='0.0.0.0', port=443)
