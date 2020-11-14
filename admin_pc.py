#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import sys
import chname
import cruser
import effuser

def menu():
    """
    Affiche le menu et demande le choix de l'utilisateur.
    """

    choix = ""
    while choix not in ["1", "2", "3", "4", "q", "Q"]:
        print("Menu :")
        print("1 : Changer le hostname de ce PC")
        print("2 : Créer un(des) utilisateur(s)")
        print("3 : Supprimer un(des) utilisateur(s)")
        print("4 : Configurer le serveur ssh")
        print("Q : Quitter\n")
        choix = input("Votre choix :")
    return choix
    
def action(choix):
    """
    Appelle le module correspondant au choix
    fourni en argument.
    """

    if choix == "1":
        nom_pc = input("Indiquez le nouveau nom de ce PC :")
        chname.change_hostname(nom_pc)
    elif choix == "2":
        new_user = input("Indiquez le nom de l'utilisateur ou du fichier des utilisateurs à créer :")
        # Si l'argument est un fichier, créer les utilisateurs
        try:
            with open(new_user): pass
            cruser.prepare_users(new_user)
        # Si l'argument n'est pas un fichier, créer l'utilisateur "argument"
        except FileNotFoundError:
            cruser.prepare_user(new_user)
    elif choix == "3":
        old_user = input("Indiquez le nom de l'utilisateur ou du fichier des utilisateurs à supprimer :")
        # Si l'argument est un fichier, supprime les utilisateurs
        # et confirme si tout s'est bien passé (None)
        try:
            with open(old_user): pass
            if effuser.supprime_users(old_user) == None:
                print("Les utilisateurs ont bien été supprimés.")
        # Si l'argument n'est pas un fichier,
        # supprime l'utilisateur old-user
        # et confirme si tout s'est bien passé (None)
        except FileNotFoundError:
            if effuser.supprime_user(old_user) == None:
                print("L\'utilisateur {} a bien été supprimé.".format(old_user))
    elif choix == "4":
        sshd_config
    elif choix.upper() == "Q":
        exit()

def continuer():
    """
    Retourne False par défaut.
    """
    reponse = input("Voulez-vous effectuer une autre opération ? [o/N]")
    if reponse.upper() == "O":
        return True
    else:
        return False

#################
### PRINCIPAL ###
#################

if __name__ == "__main__":

    # Teste root user
    if os.geteuid() != 0:
        print(os.geteuid())
        print("Sorry, you must be root.")
        exit(1)
    
    # Adaptation à la version de python    
    #if sys.version[0] == "3":
    #    raw_input = input

    # BOUCLE PRINCIPALE
    # -----------------
    autre_action = True
    while autre_action:
        choix = menu()
        action(choix)
        autre_action = continuer()

    exit(0)
