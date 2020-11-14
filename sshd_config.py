#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
Ce script utilise les fichiers 'sshd.local', 'sshd_config_base.txt'
et 'issue.txt' présents dans ce dossier.
Ces fichier doivent être édités et modifiés en fonction des besoins
avant l'utilisation du script.
Crée un fichier de paramètres applicables au serveur ssh par fail2ban.
Sauvegarde le fichier de configuration /etc/ssh/sshd_config en '.bak'.
Remplace sshd_config par le contenu du fichier sshd_config_base.txt.
Crée le fichier d'avertissement de connexion (Banner) /etc/issue.net.
"""

import shutils

def sshd_conf():
    print("Création du fichier /etc/fail2ban/jail.d/sshd.local")
    shutils.copyfile('sshd_f2b.txt', '/etc/fail2ban/jail.d/sshd.local')
    print("Sauvegarde du fichier de configuration /etc/ssh/sshd_config en \'.bak\'.")
    shutils.copyfile('/etc/ssh/sshd_config', '/etc/ssh/sshd_config.bak')
    print("Remplacement de sshd_config par le contenu du fichier sshd_config_base.txt")
    shutils.copyfile('sshd_config_base.txt', '/etc/ssh/sshd_config')
    print("Création du fichier d'avertissement de connexion ssh /etc/issue.net.")
    shutils.copyfile('issue.txt', '/etc/issue.net')

#################
### PRINCIPAL ###
#################

if __name__ == "__main__":

    # Teste root user
    if os.geteuid() != 0:
        print(os.geteuid())
        print("Sorry, you must be root.")
        exit(1)
    
    sshd_conf()
exit()