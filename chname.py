#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import shutil
import subprocess
import sys

def change_hostname(new_hostname):
    """Comme son nom l'indique."""

    print("Sauvegarde des fichiers  \"hosts\" et \"hostname\" avec l'extension \".bak\".")
    shutil.copy("/etc/hostname", "/etc/hostname.bak")
    shutil.copy("/etc/hosts", "/etc/hosts.bak")

    # Extrait le nom d'hôte courant
    # Sous Windows, utiliser platform.uname()
    cur_hostname = os.uname()[1]
    # Affiche le nom d'hôte courant
    print("The current hostname is {}.".format(os.uname()[1]))

    # Modifie hostname in /etc/hosts
    hsts = open("/etc/hosts", "r")
    contenu = hsts.read()
    hsts.close()
    contenu = contenu.replace(cur_hostname, new_hostname)
    hsts = open("/etc/hosts", "w")
    hsts.write(contenu)
    hsts.close()


    # Affiche les fichiers hosts.bak et hosts pour vérification
    print("Ancien fichier hosts :")
    with open("/etc/hosts.bak", "r") as hstsbk:
        print(hstsbk.read())

    print("Nouveau fichier hosts :")
    with open("/etc/hosts", "r") as hsts:
        print(hsts.read())

    # Change le nom d'hôte
    subprocess.run(['hostnamectl', 'set-hostname', new_hostname])

    # Affiche le nouveau nom d'hôte
    print("The new hostname is {}.".format(os.uname()[1]))

    print("Le système doit être redémarré pour la prise en compte des modifications.")
    redemarrer = input("Redémarrer maintenant ? [O/n]")
    if redemarrer.upper() != "N":
        subprocess.run(["shutdown", "-r", "+0"])

if __name__ == "__main__":
    # Teste root user
    if os.geteuid() != 0:
        print("Sorry, you must be root.")
        exit(1)

    # Affecte la variable new_hostname
    if len(sys.argv) == 1:
        new_hostname = input("Indiquer le nouveau nom de la machine :")
    elif len(sys.argv) == 2:
        new_hostname = sys.argv[1]
    else:
        print("Too many arguments.")
        exit()

    change_hostname(new_hostname)
    exit()