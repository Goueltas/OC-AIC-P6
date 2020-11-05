#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Suppression d'utilisateur
Usage:
effUser.py fichierUtilisateurs
effUser.py username
effUser.py username groupname

Syntaxe de fichierUtilisateur: une ligne par utilisateur,
Syntaxe de chaque ligne: username groupname.
Note: Il est possible de réutiliser le fichier ayant servi à créer les utilisateurs
et comportant des lignes de la forme "username groupname mot_de_passe".
Dans ce cas, le mot de passe ne sera pas pris en compte.
"""

import os
import subprocess
import sys

def supprime_user(username, groupname=False):
    """
    Supprime l'utilisateur.
    Supprime le groupe, s'il est vide.
    """

    # Affecte le nom du groupe
    if not groupname:
        groupname = groupe(username)
    # Teste si utilisateur existe
    if user_exists(username):
        # Supprime utilisateur et sauvegarde données (/home/userHome dans ./utilisateur.bak
        subprocess.run(['deluser', '--remove-home', '--backup', username])

        # Supprime groupe s'il existe et est vide
        with open('/etc/group', "r") as groupes:
            for ligne in groupes:
                group = ligne.split(':', 1)[0]
                if group == groupname:
                    subprocess.run(['delgroup', '--only-if-empty', groupname])
        print("L'utilisateur {} a été supprimé...".format(username))
        print("Son dossier personnel a été sauvegardé dans le dossier courant")
        print("sous le nom {}.tar.bz2".format(username))
    return


def supprime_users(fichier):
    """
    Supprime les utilisateur listés dans le fichier indiqué en argument.
    Syntaxe de fichier: une ligne par utilisateur,
    Syntaxe de chaque ligne: username groupname.
    Note: Il est possible de réutiliser le fichier ayant servi à créer les utilisateurs
    et comportant des lignes de la forme "username groupname mot_de_passe".
    Dans ce cas, le mot de passe ne sera pas pris en compte.
    """

    # Extrait noms d'utilisateurs et noms de groupes du fichier
    with open(fichier, "r") as f:
        old_users = f.readlines()
        for line in old_users:
            supprime_user(line.split()[0], line.split()[1])
    return

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

#################
### PRINCIPAL ###
#################

if __name__ == "__main__":

    # Teste root user
    if os.geteuid() != 0:
        print("Sorry, you must be root.")
        exit(1)

    # Test nombre d'arguments (le nom du script EST un argument)
    # et supprime le (les) utilisateur(s)
    if len(sys.argv) == 1:
        print("Vous devez fournir au moins 1 argument.")
        print("Usage :")
        print("effUser.py userFile")
        print("effUser.py userName [userGroup]")
    elif len(sys.argv) == 2:
        # Si l'argument est un fichier, supprime les utilisateurs
        # et confirme si tout s'est bien passé (None)
        try:
            with open(sys.argv[1]): pass
            if supprime_users(sys.argv[1]) == None:
                print("Les utilisateurs ont bien été supprimés.")
        # Si l'argument n'est pas un fichier,
        # demande le nom du groupe à supprimer (si vide),
        # supprime l'utilisateur "argument"
        # et confirme si tout s'est bien passé (None)
        except IOError:
            old_group = input("Indiquez le nom du groupe principal de l'utilisateur (Entrée pour nom par défaut) :")
            if old_group == "":
                print("Le programme supprimera le groupe ayant le nom de l'utilisateur ({}).".format(sys.argv[1]))
                old_group = str(sys.argv[1])
            if supprime_user(sys.argv[1], old_group) == None:
                print("L'utilisateur {} a bien été supprimé.".format(sys.argv[1]))
    # Si deux arguments (utilisateur et groupe)
    elif len(sys.argv) == 3:
        supprime_user(sys.argv[1], sys.argv[2])
    else:
        print("Too many arguments.")
        exit()

    exit()