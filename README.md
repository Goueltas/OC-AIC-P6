# OC-AIC-P6

!!! AVERTISSEMENT !!!
LE SCRIPT f2bssh.py (CHOIX 4 DU SCRIPT admin_pc.py) MODIFIE LA CONFIGURATION DU SERVEUR SSH SUR LA MACHINE SUR LAQUELLE IL EST LANCÉ. IL INTERDIT LA CONNEXION EN ROOT ET L'AUTHENTIFICATION PAR MOT DE PASSE. IL EST NÉCESSAIRE DE DISPOSER D'UN UTILISATEUR SUDOER ET D'AVOIR PARAMETRÉ ET TESTÉ L'AUTHENTIFICATION PAR CLÉ AVANT DE LE LANCER SUR UNE MACHINE DISTANTE !

Ces scripts ont été réalisés dans le cadre d'une formation. Ils ont été testés sur des machines distantes sous CentOS 8 depuis une machine locale sous Debian 10 (Buster).

Je vous encourage vivement à lire les commentaires et doc_strings présent dans les scripts AVANT de les utiliser !


scripts_py: Ce dossier contient le script admin.py qui est un menu d'appel des autres scripts python.

Chaque script peut être utilisé seul.

fileUsers : Fichier texte destiné à servir d'exemple et de test pour la création/suppression d'utilisateurs multiples.
    
sshd.local, sshd_config_base.txt, issue.txt: Ces fichiers doivent être édités et modifiés en fonction des besoins AVANT l'utilisation du script f2bssh.py.


ssh_connect.sh :

Ce script agit à distance sur des machine dont le nom est codé en dur dans le script ("http1" et "bdd1"). Vous devez modifier ces noms en fonction de vos machines distantes, voire copier/coller les lignes y faisant référence si vous souhaitez ajouter des machines.

Actions du script:

Paramètre l'authentification par clé pour la connexion ssh entre le machine locale et les machines distantes.

Crée l'environnement virtuel sur lmachine locale avec les dernières version de python et ansible disponibles dans les dépôts.

Lance le playbook centos_postinstall.yml


centos_postinstall.yml :

Playbook ansible basique qui installe epel, git, fail2ban, apache, php, mariadb, ouvre le port 80 du serveur apache et procède aux mises à jour des machines distantes.


Exemple d'utilisation :

Les machines distantes doivent avoir un serveur ssh activé et enabled.

Copier le dossier scripts_py sur la(les) machine(s) distante(s) (scp).

Se connecter à la machine distante (ssh).

Installer Python 3.

Créer un utilisateur au moyen du script cruser.py (ou admin_pc.py, choix 2).

Rendre cet utilisateur sudoer (groupe wheel).

Se déconnecter de la machine distante.

Lancer le script ssh_connect.sh sur la machine locale.

Répondre aux questions: utilisateur local, utilisateur distant, environnement virtuel.

Répondre aux questions et demandes de mot de passe relatives à la création des clés et au lancement du playbook ansible.

Attendre la fin des opérations.

Vérifier le bon fonctionnement de l'authentification par clé pour l'utilisateur distant (utilisateur_local ~$ ssh utilisateur_distant@machine_distante).

SI ET SEULEMENT SI la connexion avec authentification par clé a réussi:

Lancer le script f2bssh.py (ou admin_pc.py, choix 4).
