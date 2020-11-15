# OC-AIC-P6

Ce dossier contient le script admin.py qui est un menu d'appel des autres scripts python.

Chaque script peut être utilisé seul.

fileUsers :
Fichier texte destiné à servir d'exemple et de test
pour la création/suppression d'utilisateurs multiples.

sshd.local, sshd_config_base.txt, issue.txt :
Ces fichiers doivent être édités et modifiés en fonction
des besoins avant l'utilisation du script sshd_config.py.

ssh_connect.sh :
Paramètre la connectivité entre le gestionnaire et les noeuds distants.
Crée l'environnemt virtuel avec les dernières version de python et ansible
disponibles dans les dépôts.
Lance le playbook centos_postinstall.yml

centos_postinstall.yml :
Playbook ansible basique qui installe epel, git, fail2ban,
apache, php, mariadb et procède aux mises à jour d'une RHEL.
