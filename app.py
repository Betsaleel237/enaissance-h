
from flask import Flask,render_template,request,redirect,url_for,session,jsonify,Response,session
from flask import Flask,render_template, request
from flask_mysqldb import MySQL
import json
import datetime
import os
import time
import datetime
import winsound
from flask_session import Session
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
 

 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'enaissance' 
mysql = MySQL(app)




@app.route("/login",methods=["GET","POST"])
def login():
    name=request.args.get('name')
    password=request.args.get('password')
    return render_template("index1.html",name=name,password=password)

@app.route("/login_ver",methods=["POST","GET"])
def login_ver():
    if request.method == "POST":
        donnees=request.form
        name=request.form.get("name")
        password=request.form.get("password")
        session["name"]=name
        return redirect("/",name=name)
        
       
        return redirect(url_for("index"))    
    else:
        return redirect(url_for("login"))

@app.route("/")
def index():
    if not session.get('name'):
        return redirect("/login")
    name=request.args.get('name')
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM commune''')
    rv = cur.fetchall()
    compteur=0
    while compteur < len(rv):
        print(rv[compteur])
        compteur=compteur+1
    
    return render_template("index.html",liste_commune=rv,name=name)


@app.route("/register")
def register():
    return render_template("sign-up.html")



@app.route("/register_ver", methods=["POST"])
def register_ver():
    if request.method == "POST":
        email=request.form.get("email")
        name=request.form.get("name")
        password=request.form.get("password")
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO admin VALUES(" ",%s,%s,%s)''',(name,email,password))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('login',name=name,password=password))
    else:
        return redirect(url_for('register'))
 
@app.route("/select_commune", methods=["POST"])
def select_commune():
    if request.method == "POST":
        id_commune=request.form.get("id_commune")
        nom_commune=request.form.get("nom_commune")
        arrondissement=request.form.get("arrondissment")
        departement=request.form.get("departement")
        region=request.form.get("region")
        return render_template("declarer.html", id_commune=id_commune ,nom_commune=nom_commune,arrondissement=arrondissement,departement=departement,region=region)
    
@app.route("/declaration_reg", methods=["POST"])
def declaration_reg():
    if request.method == "POST":
        nom_enfant=request.form.get("nom_enfant")
        prenom_enfant=request.form.get("prenom_enfant")
        sexe_enfant=request.form.get("sexe_enfant")
        date_naissance=request.form.get("date_naissance")
        lieu_naissance=request.form.get("lieu_naissance")
        type_naissance=request.form.get("type_naissance")
        rang_naissance=request.form.get("rang_naissance")
        poids_enfant=request.form.get("poids_enfant")
        taille_enfant=request.form.get("taille_enfant")
        nom_mere=request.form.get("nom_mere")
        date_mere=request.form.get("date_mere")
        lieu_mere=request.form.get("lieu_mere")
        profession_mere=request.form.get("profession_mere")
        nationalite_mere=request.form.get("nom_enfant")
        nom_pere=request.form.get("nom_pere")
        date_pere=request.form.get("date_pere")
        lieu_pere=request.form.get("lieu_pere")
        id_commune=request.form.get("id_commune")
        id_hopital=request.form.get("id_hopital")
        print(nom_enfant)
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO declaration VALUES(" ",%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(nom_enfant,prenom_enfant,sexe_enfant,date_naissance,lieu_naissance,type_naissance,rang_naissance,poids_enfant,taille_enfant,nom_mere,date_mere,lieu_mere,profession_mere,nationalite_mere,nom_pere,date_pere,lieu_pere,id_commune,id_hopital))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('naissanceh'))
   


@app.route("/naissanceh")
def naissanceh():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM declaration''')
    rv = cur.fetchall()
    compteur=0
    while compteur < len(rv):
        print(rv[compteur])
        compteur=compteur+1
    return render_template("naissanceh.html",liste_declaration=rv)

@app.route("/rechercher", methods=['POST'])
def rechercher():
    if request.method == "POST":
        nom_enfant=request.form.get("nom_enfant")
        nom_pere=request.form.get("nom_pere")
        nom_mere=request.form.get("nom_mere")
        date_naissance=request.form.get("date_naissance")
        sexe=request.form.get("sexe")
        nom_commune=request.form.get("nom_commune")
    nom_enfant="%"+nom_enfant+"%"    
    nom_pere="%"+nom_pere+"%"    
    nom_mere="%"+nom_mere+"%"    
    date_naissance="%"+date_naissance+"%"    
    sexe=sexe+"%"  
    nom_commune="%"+nom_commune+"%"    
    cur = mysql.connection.cursor()
    query_string = " SELECT * FROM declaration, commune WHERE declaration.id_commune=commune.id_commune and nom_enfant LIKE %s and nom_pere LIKE %s and nom_mere LIKE %s and date_naissance LIKE %s and sexe_enfant LIKE %s and titre_commune LIKE %s "
    #cur.execute(query_string, (nom_enfant,nom_pere,nom_mere,date_naissance,sexe, nom_commune))
    cur.execute(query_string, [nom_enfant,nom_pere,nom_mere,date_naissance,sexe,nom_commune])
    
    rv = cur.fetchall()
    compteur=0
    while compteur < len(rv):
        print(rv[compteur])
        compteur=compteur+1
    return render_template("naissanceh.html",liste_declaration=rv)


@app.route("/declarer")
def declarer():
    return render_template("declarer.html")

@app.route("/create_commune")
def create_commune():
    return render_template("create_commune.html")

@app.route("/commune_reg",methods=["POST"])
def commune_reg():
    if request.method == "POST":
        departement=request.form.get("departement")
        region=request.form.get("region")
        arrondissement=request.form.get("arrondissement")
        titre_commune=request.form.get("titre_commune")
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO commune VALUES(" ",%s,%s,%s,%s)''',(titre_commune,arrondissement,departement,region))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('create_commune'))

@app.route("/subscription")
def subscription():
    return render_template("subscription.html")

@app.route("/create_exam")
def create_exam():
    return render_template("create-exam.html")

@app.route("/create_exam_reg",methods=["POST"])
def create_exam_reg():
    if request.method == "POST":
        exam_code=request.form.get("exam_code")
        subject=request.form.get("subject")
        classroom_name=request.form.get("classroom_name")
        exam_date=request.form.get("exam_date")
        date=exam_date.split('-')
        start_time=request.form.get("start_time")
        time=start_time.split(':')
        class_name=request.form.get("class_name")
        duration=request.form.get("duration")
        assignee=request.form.get("assignee")
        status="To be done"
        report="../reports/"
        print('start time {} exam date {} duration {}  '.format(start_time,exam_date,duration))
       
        return redirect(url_for('schedule_exam'))
   






if __name__=="__main__":
    app.run(debug=True)
   #app.run(host='localhost', port=5000)
