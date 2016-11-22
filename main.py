# -*- coding: utf-8 -*-
# ----------------------- IMPORTATION DES BIBLIOTHEQUES -------------------
import os
import sqlite3
import webbrowser
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


# ----------------------- CREATION DE L APPLICATION -------------------
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
        DATABASE=os.path.join(app.root_path,'bdd.db'),
        SECRET_KEY='development key',
        USERNAME='admin',
        PASSWORD='default'
    ))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


# ----------------------- METHODE GENERIQUE POUR LA CREATION DE LA BDD  -------------------
def init_db():
    db = get_db()
    with app.open_resource('BDD.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


# ----------------------- INITIALISATION DE LA BDD  -------------------
@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the resquest."""
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()



# ----------------------- PAGE INDEX  -------------------
@app.route('/')
def home():
    """ redirige le root vers la page index """
    return redirect(url_for('index'))

@app.route('/index')
def index():
    """ page index """
    return render_template('index.html')


# ----------------------- PAGE CONSULTATION DES ELEVES  -------------------
@app.route('/show_entries')
def show_entries():
    """ Affiche les valeurs de la table eleves et les retourne a travers le template show_entries.html """
    db = get_db()
    cur = db.execute('select nom, prenom, date_naissance, telephone, option, ecole_origine from eleves order by nom asc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

@app.route('/show_entries_triees', methods=['POST'])
def show_entries_triees():
    """ Selectionner les etudiants de la base de donnee selon leur campus et les affiches sur la page template show_entries.html """
    db = get_db()
    cur = db.execute('select nom, prenom, date_naissance, telephone, option, ecole_origine from eleves where ecole_origine = ? order by nom asc',[request.form['campus']])
    entries = cur.fetchall()
    if entries:
        return render_template('show_entries.html', entries=entries)
    else:
        flash(u'Pas d\'élève sur le campus selectionné | Retour à l\'option "---"')
        return redirect(url_for('show_entries'))

# ----------------------- PAGE CONSULTATION DE LA FICHE DE 1 ELEVE  -------------------
@app.route('/consulter_eleve', methods=['GET','POST'])
def consulter_eleve():
    """ Retourne la page consulter_eleve.html """
    return render_template('consulter_eleve.html')

@app.route('/consulter', methods=['POST'])
def consulter():
    """ Retourne la page template consulter.html correspondant a la fiche de l eleve de la requete prevenant de la page consulter_eleve.html """
    db = get_db()
    cur = db.execute('select nom, prenom, date_naissance, telephone, option, ecole_origine, mathematiques, informatique from eleves where nom = ? and prenom = ?',[request.form['nom_eleve'].upper(), request.form['prenom_eleve'].title()])
    entries = cur.fetchall()
    if entries:
        return render_template('consulter.html', entries=entries)
    else:
        flash(u'L\'élève indiqué n\'existe pas dans la base de donnée.')
        print("No such student in the database. Return to consulter_eleve")
        return redirect(url_for('consulter_eleve'))


# ----------------------- AJOUTER ELEVE -------------------
@app.route('/add', methods=['POST'])
def add_entry():
    """ Ajoute une valeur eleve dans la BDD selon la requete envoyee de la page ajouter_eleve.html """
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    ddn = request.form['dob_day']+'/'+request.form['dob_month']+'/'+request.form['dob_year']
    print(ddn)
    db.execute('insert into eleves (nom, prenom, date_naissance, telephone, option, ecole_origine) values (?,?,?,?,?,?)',
                 [request.form['nom'].upper(), request.form['prenom'].title(),ddn,request.form['telephone'],request.form['option'],request.form['ecole_origine']])
    db.commit()
    flash(u'L\'élève a bien été ajouté à la base de donnée.')
    print("A new value was successfully added to the database.")
    return redirect(url_for('show_entries'))

@app.route('/ajouter_eleve')
def ajouter_eleve():
    return render_template('ajouter_eleve.html')


# ----------------------- SUPPRIMER ELEVE VIA LA PAGE SUPPRIMER ELEVE -------------------
@app.route('/delete', methods=['POST'])
def delete_entry():
    """ Supprime un eleve de la base de donnee selon la requete envoyee de la page supprimer_eleve.html """
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    #tester si l'eleve existe
    cur = db.execute('select * from eleves where nom=? and prenom=?',[request.form['nom'].upper(), request.form['prenom'].title()])
    eleve = cur.fetchall()
    if eleve:
        db.execute('delete from eleves where nom=? and prenom=?',[request.form['nom'].upper(), request.form['prenom'].title()])
        db.commit()
        flash(u'L\'élève a été supprimé.')
        print("The lign was deleted from the database.")
    else:
        flash(u'Cet élève n\'existe pas.')
        print("No such student in the database.")
    return redirect(url_for('show_entries'))

@app.route('/supprimer_eleve')
def supprimer_eleve():
    return render_template('supprimer_eleve.html')

# ----------------------- SUPPRIMER ELEVE VIA LE TABLEAU DE LA PAGE SHOW_ENTRIES -------------------
@app.route('/delete_eleve/<nom>,<prenom>', methods=['POST'])
def delete_eleve(nom,prenom):
    """ supprime un eleve de la base de donnee par clic sur la croix a cote de son nom dans la page show_entries.html """
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('delete from eleves where nom=? and prenom=?',[nom,prenom])
    db.commit()
    flash(u'L\'élève a bien été supprimé.')
    print("The value has been successfully deleted from the database.")
    return redirect(url_for('show_entries'))


# ----------------------- LOGGIN/LOGOUT -------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash(u'Vous êtes connecté !')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash(u'Vous êtes déconnecté.')
    return redirect(url_for('index'))

# ----------------------- VOIR LES NOTES DES ELEVES ----------------------------
@app.route('/notes')
def notes():
    """ Affiche les notes de tous les eleves sur la page notes.html """
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    cur=db.execute('select nom, prenom, mathematiques, informatique from eleves')
    entriesnotes = cur.fetchall()
    return render_template('notes.html', entriesnotes=entriesnotes)


# ----------------------- MODIFIER LES NOTES DES ELEVES -------------------------
@app.route('/modificationnoteseleves/<nom>,<prenom>', methods=['POST'])
def modificationnoteseleves(nom,prenom):
    """ Modifie la valeur des attributs mathematique et informatique de l eleve a partir de la requete envoyee depuis la page modification.html """
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('update eleves set mathematiques= ?, informatique= ? WHERE nom=? and prenom = ?',[request.form['math'],request.form['info'],nom,prenom])
    db.commit() 
    
    flash(u'Les notes de l\'élève ont été correctement modifiées.')
    print("The entry was successfully updated.")
    return redirect(url_for('notes'))

@app.route('/modification/<nom>,<prenom>', methods=['GET'])
def modification(nom,prenom):
    if not session.get('logged_in'):
        abort(401)
    return render_template('modification.html', entriesnotes=[prenom,nom])

# ----------------------- DEMANDER L ADRESSE MAIL D UN ELEVE -------------------------
@app.route('/mailentry', methods=['POST'])
def mail_entry():
    """ Verifie si l eleve est present dans la base de donnee et si c est le cas retourne son mail sous forme de flash sur la page courante """
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    cur = db.execute('select * from eleves where nom=? and prenom=?',[request.form['nom'].upper(), request.form['prenom'].title()])
    eleve = cur.fetchall()
    if eleve:
        a=request.form['prenom']
        b=request.form['nom']
        flash(a.lower()+'.'+b.lower()+'@etudiant.mines-nantes.fr')
    else:
        flash(u'Désolé, l\'étudiant indiqué n\'existe pas dans la base de donnée !')
        print("No such entry in the database.")
    return redirect(url_for('mail'))

@app.route('/mail')
def mail():
    if not session.get('logged_in'):
        abort(401)
    return render_template('mail.html')


# ----------------------- OUVRE L APPLICATION DANS LE NAVIGATEUR PAR DEFAUT -------------------------
webbrowser.open('http://127.0.0.1:5000/')
# Methode a commenter si probleme d URL
