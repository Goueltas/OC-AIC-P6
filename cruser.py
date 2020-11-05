#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Création d'utilisateur
Usage:
creerUser.py fichierUtilisateurs
creerUser.py username
creerUser.py username groupname
creerUser.py username groupname mot_de_passe

Syntaxe de fichierUtilisateur: une ligne par utilisateur,
Syntaxe de chaque ligne: username groupname password
"""

import crypt
import getpass
import grp
import os
import subprocess
import sys

def creer_user(username, groupname, password):
    """
    Crée l'utilisateur correspondant
    aux arguments fournis.
    """

    home = "/home/{}".format(username)
    #Teste si groupe existe, sinon le crée
    try:
        grp.getgrnam(groupname)
    except:
        subprocess.run(['addgroup', groupname])

    # Cree utilisateur avec home standard, groupe, shell bash
    subprocess.run(['useradd', '--home', home, '--gid', groupname, '--create-home', '--password', password, '--shell', '/bin/bash', username]) #ou /home/$NEWGROUP/$NEW_USER ?

    print("L'utilisateur {} a été créé avec les caractéristiques suivantes :".format(username))
    with open('/etc/passwd', "r") as p:
        users = p.readlines()
        for line in users:
            if line.split(":")[0] == username:
                print(line)
    return

def prepare_user(username, groupname=False):
    """
    Prépare les arguments 'utilisateur', 'groupe' et 'mot de passe'
    puis appelle la fonction creer_user avec ces 3 arguments
    """

    # Teste si utilisateur existe déjà
    if user_exists(username):
        print("L'utilisateur {} existe déjà.".format(username))
        exit()
    # Sinon, le crée
    else:
        # Crée le groupe s'il n'a pas été fourni en argument du script
        if not groupname:
            groupname = groupe(username)
        # Crée le mot de passe
        password = creer_mot_de_passe(username)
        # Crée l'utilisateur
        creer_user(username, groupname, password)

def prepare_users(fichier):
    """
    Extrait noms d'utilisateurs, noms de groupes et mots de passe du fichier
    puis appelle la fonction creer_user avec ces 3 arguments pour chaque utilisateur.
    Syntaxe du fichier: un utilisateur par ligne.
    Syntaxe de chaque ligne: utilisateur groupe mot_de_passe
    """

    with open(fichier, "r") as f:
        users = f.readlines()
        # Pour chaque utilisateur à créer
        for ligne in users:
            ligne = ligne.split()
            # Si l'utilisateur n'existe pas
            if not user_exists(ligne[0]):
                # Encode le mot de passe
                sel = crypt.mksalt()
                pw = crypt.crypt(ligne[2], sel)
                # Crée l'utilisateur
                creer_user(ligne[0], ligne[1], pw)		

def user_exists(username):
    """
    Teste si l'utilisateur existe.
    Retourne un booléen.
    """

    with open('/etc/passwd', "r") as p:
        existing_users = p.readlines()
        for line in existing_users:
            existing_user = line.split(':', 1)[0]
            if existing_user == username:
                return True
    return False

def groupe(username):
    """
    Affecte le nom du groupe de l'utilisateur.
    Par défaut, utilise le nom de l'utilisateur comme nom de groupe.
    Retourne groupname.
    """

    groupname = input("Entrez le nom du groupe principal de l'utilisateur (Entrée pour nom par défaut) :")
    if groupname == "":
        groupname = str(username)
        print("Le groupe aura le nom de l\'utilisateur : {}.".format(username))
    return groupname

def creer_mot_de_passe(username):
    """
    Demande et encode le mot de passe de l'utilisateur fourni en argument.
    Retourne le mot de passe encodé.
    """

    password = 'a'
    password1 = 'b'
    while password != password1:
        password = getpass.getpass("Indiquez le mot de passe de {}:".format(username))
        password1 = getpass.getpass("Confirmez le mot de passe :")
    return password

###################
#### PRINCIPAL ####
###################

if __name__ == "__main__":

    # Teste root user
    if os.geteuid() != 0:
        print("Sorry, you must be root.")
        exit(1)

    # Test nombre d'arguments (le nom du script EST un argument)
    # et crée le (les) utilisateur(s)
    if len(sys.argv) == 1:
        print("Vous devez fournir au moins 1 argument.")
    elif len(sys.argv) == 2:
        # Si l'argument est un fichier, créer les utilisateurs
        try:
            with open(sys.argv[1]): pass
            prepare_users(sys.argv[1])
        # Si l'argument n'est pas un fichier, créer l'utilisateur "argument"
        except IOError:
            prepare_user(sys.argv[1])
    # Si deux arguments (utilisateur et groupe)
    elif len(sys.argv) == 3:
        prepare_user(sys.argv[1], sys.argv[2])
    # Si trois arguments (utilisateur, groupe et mot de passe)
    elif len(sys.argv) == 4:
        prepare_user(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Too many arguments.")
        exit()

    exit()