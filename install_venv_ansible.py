#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import cruser
import os
import subprocess

def dedicated_user():
    """
    Renvoie l\'utilisateur dédié à ansible
    après l'avoir créé si nécessaire.
    """

    new_user = input("Voulez-vous créer un utilisateur dédié ? [O/n] ")
    if new_user == "" or new_user.upper() == "O":
        ansible_user = ""
        confirmation = ""
        while ansible_user == "" or confirmation.upper != "O":
            ansible_user = input("Indiquez le nom  de l\'utilisateur à créer: ")
            confirmation = input("Confirmez-vous la création de l\'utilisateur {}? [o/N] ".format(ansible_user))
        cruser.prepare_user(ansible_user)
    else:
        ansible_user = input("Quel utilisateur voulez-vous dédier à ansible? ")
    return ansible_user

def opsys():
    """
    Extrait le nom du système d'exploitation
    et retourne la commande d'installation à utiliser (apt ou dnf).
    Fonctionne pour RedHat (Centos), Debian, Ubuntu.
    """

    try:
        with open("/etc/redhat-release"): pass
        return "dnf"
    except FileNotFoundError:
        pass
    with open("/etc/issue") as f:
        if f.read().split()[0] == "Debian" \
        or f.read().split()[0] == "Ubuntu":
            return "apt"

def virtenv(evt_name, ansible_user):
    """
    Installe les paquets nécessaires
    puis crée l'environnement virtuel
    et installe ansible
    """


    subprocess.run([installer, "install", "python3-venv", "sshpass"])
    #subprocess.run(["su", "-", ansible_user])
    subprocess.run(["python3", "-m", "venv", evt_name])
    subprocess.run(["source", "{}/bin/activate".format(evt_name)])
    subprocess.run(["pip3", "install", "ansible"])
    subprocess.run("deactivate")
    subprocess.run("exit")


        

#####################
# BOUCLE PRINCIPALE #
#####################

if __name__ == "__main__":

    # Teste root user
    if os.geteuid() != 0:
        print(os.geteuid())
        print("Sorry, you must be root.")
        exit(1)

    ansible_user = dedicated_user()
    installer = opsys()
    evt_name = input("Indiquez le chemin absolu de l'environnement virtuel à créer: ")
    virtenv(evt_name, ansible_user)
