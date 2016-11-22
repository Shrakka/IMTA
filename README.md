***************************************************************
---------------------------------------------------------------
Projet de site web pour la gestion administrative de l’Institut Mines-Télécom Atlantique Bretagne-Pays de la Loire
---------------------------------------------------------------
***************************************************************

Réalisateurs :
- HERVIEU Antoine
- TESTA Enzo

--------------------------------
Comment exécuter l'application ? 
--------------------------------

* Ouvrir une fenetre Terminal/invite de commande/shell. 
* Se placer dans le dossier en IMTA_HERVIEU_TESTA à l'aide de la commande cd <folder>
* Ouvrir son navigateur par defaut (Firefox de préférence)
* Exécuter la commande suivante dans le Terminal : 

- SOUS MAC : export FLASK_APP=main.py & flask run
- SOUS LINUX : export FLASK_APP=main.py & flask run
- SOUS WINDOWS : set FLASK_APP=main.py & flask run

(Eventuellement séparer les deux commandes en ne les tapant pas sur une seule ligne)

* La page Firefox s'ouvre alors automatiquement. 
* Si l'URL est différent de celui spécifié, entrer l'URL proposé par le Terminal dans la barre d'URL de Firefox et commenter la derniere ligne de code du fichier main.py 
* ENJOY ! Pour un meilleur affichage, n'hesitez pas à naviger en mode plein écran sous Firefox ! 

----------------------------------------------
QUELS IDENTIFIANTS POUR ACCEDER AUX METHODES ? 
----------------------------------------------

login : admin
password : default

------------------------------------------------
QUEL EST L'ARCHITECTURE DU PROGRAMME ? (3 tiers)
------------------------------------------------

L’architecture de notre projet est la suivante : 
- Notre main.py agit comme un contrôleur, il encadre le trafic des adresses. I joue également le rôle de modèle car les fonctions agissant sur les bases de données y sont stockées.
- La vue est principalement gérée par les fichiers contenus dans template et dans static. 
- Un fichier bdd.db comprend la base de donnée SQL des élèves.
==> Le détail des couches est spécifié ci-dessous.

*******************************
COUCHE 1 - Présentation (Vue) : 
*******************************
    - Dossiers concernés : static/templates
    - Comprend les fichiers HTML et les feuilles de style exécutés par le navigateur web. 
    - Contenus : 
        * static contient le fichier "style.css" et "boostrap.min.css" qui sont les feuilles de style de l'application
        * templates comprend les pages HTML statiques :
            - layout : page dont hérite toutes les autres page html. Comprend le titre, le logo, les boutons bleus d'accès aux pages et méthodes de l'application.
            - index : l'URL root ('/') redirige automatiquement vers la page index.
            - login : page pour s'indentifier.
            - login : page pour s'indentifier.
            - ajouter_eleve : pour ajouter un élève
            - consulter_eleve : choix de l'élève dont on souhaite consulter la fiche
            - consulter : page-template de la fiche d'un eleve
            - mail : choix de l'élève dont on souhaite obtenir le mail
            - modification : choix des notes à modifier.
            - notes : présente les notes de tous les élèves et peut rediriger vers modification.html
            - show_entries : affiche tous les élèves inscrits sous forme d'un tableau (option de tri disponible)


*********************************
COUCHE 2 - Métier (Application) : 
*********************************

    - Dossiers et fichiers concernés : main.py et templates
    - Contenus :
        * main.py : fichier python exécutable par Python-FLASK qui joue le rôle de controleur et gère les différents accès aux pages ainsi que les variables qui doivent y être envoyées (en POST ou en GET).
        * templates : contient les pages html où les variables envoyées depuis main.py sont interprétées pour l'affichage.

        - Documentation des fonctions : 
            * La plupart des fonctions suivantes vérifient si l’on est connecté avant de poursuivre.
            * show_entries() : Affiche la page show_entries.html en envoyant le contenu de nom, prenom, date_naissance, telephone, option, ecole_origine de la table eleves.
            * add_entry() : Ajoute nom, prenom, date_naissance, telephone, option, ecole_origine entré dans la base de données.
            * ajouter_eleve() : Renvoie la page ajouter_eleves.html
            * delete_entry(): Efface l’élève dont le nom et le prénom correspondent de la base de données (depuis page supprimer_eleve.html).
            * delete_eleve(nom,prenom) : Efface l’élève de nom nom et de prénom prenom dans la base de donnees depuis la page show_entries.html. Elle correspond au clic sur le bouton "Supprimer".
            * supprimer_eleve() : Renvoie la page supprimer_eleve.html
            * login() : Permet de se connecter.
            * logout() : Permet de se déconnecter.
            * notes() : Renvoie la page notes.html avec les prénoms, noms et notes des élèves en mémoire.
            * modificationnoteseleves(nom,prenom): Renvoie la page modification.html avec un tableau de type [nom,prenom].
            * mail_entry(): Construit et affiche un mail à partir d’un prénom et d’un nom.
            * mail() : Renvoie la page mail.html.


***************************
COUCHE 3 - Base de donnée :  
***************************

    - Fichier concerné : bdd.db et BDD.sql
    - Contenus :
        * Le fichier BDD.sql permet de créer la base de donnée bdd.db à l'aide de la commande init_bd() exécuté par le main python. Cette action est réalisée une fois et ne doit plus être réalisée à nouveau (sauf si la base de donnée doit être écrasée puis recrée).

        * Le fichier bdd.db est la base de donnée. Elle comporte une seule table (eleves) et contient les attributs suivants : id (clef primaire), nom, prenom, date_naissance, telephone, option, ecole_origine, mathematiques et informatique.

    - Nous aurions pu faire le choix de créer une base de donnée spécifique aux matières et aux notes pour pouvoir ajouter/modifier plus facilement celles-ci, mais cela complique le code.



-----------------------
QU'AVONS NOUS REALISE ? 
-----------------------

Nous avons entièrement réalisé les méthodes de l'application, à l'exception de celles proposées dans le tuto flask fournie par le corps enseignant, à savoir : 

- login()
- logout()
- show_entries() : que vous avons adapté.
- les méthodes de base de la construction de la base de donnée : init_db() ; connect_db() ; get_db() ; initdb_command() ; close_db()

