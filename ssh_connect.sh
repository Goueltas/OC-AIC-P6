#!/bin/bash

# Paramètre la connectivité entre le gestionnaire et les noeuds distants.
# Crée l'environnemt virtuel avec les dernières version de python et ansible
# disponibles dans les dépôts.
# Lance le playbook centos_postinstall.yml (epel, git, fail2ban,
# apache, php, mariadb + Mises à Jour)
#
# Usage:
# ssh_connect.sh utilisateur_local utilisateur_distant
# Les arguments sont facultatifs.
# Ils seront demandés s'ils ne sont pas fournis.
# Les utilisateurs doivent avoir été créés au préalable.

#################
### PRINCIPAL ###
#################

# Teste root user
if [ $EUID != 0 ] ; then
	echo "Sorry, you must be root."
	exit 0
fi

# Déclaration des variables
virtenv=""
venvuser=""
distuser=""

# Attribution des variables
if [ $# = 2 ] ; then
    venvuser=$1
    distuser=$2
elif [ $# = 1 ] ; then
    venvuser=$1
    while [[ $distuser == "" ]] ; do
        read -p "Indiquez le nom de l'utilisateur distant: " distuser
    done
elif [ $# = 0 ] ; then
    while [[ $venvuser == "" ]] ; do
        read -p "Indiquez le nom de l'utilisateur du virtual env.: " venvuser
    done
    while [[ $distuser == "" ]] ; do
        read -p "Indiquez le nom de l'utilisateur distant: " distuser
    done
fi

while [[ $virtenv != /* ]] ; do
    echo "Indiquez le nom de l'environnement virtuel à créer"
    read -p "(chemin absolu): " virtenv
done

# Mise à jour du système et installation des paquets
# requis pour la création d'un environnement virtuel python3
apt update -y
apt upgrade -y
apt install python3 python3-venv sshpass

# Création de l'environnement virtuel
# et copie du playbook
sudo -u $venvuser python3 -m venv $virtenv
cp centos_postinstall.yml $virtenv
chown $venvuser:$venvuser $virtenv

cd $virtenv

# Création des clés ssh
sudo -u $venvuser ssh-keygen -t ecdsa

sudo -u $venvuser bash << EXITUSER
source $virtenv/bin/activate
pip3 install ansible
ansible --version
deactivate

#echo "192.168.122.11 http1" >> /etc/hosts
#echo "192.168.122.12 bdd1" >> /etc/hosts

echo "[srvweb]" > $virtenv/inventaire.ini
echo "http1" >> $virtenv/inventaire.ini
#echo "centos-8" >> $virtenv/inventaire.ini
echo "[bdd]" >> $virtenv/inventaire.ini
echo "bdd1" >> $virtenv/inventaire.ini


ssh-copy-id -i /home/$venvuser/.ssh/id_ecdsa.pub $distuser@http1
ssh-copy-id -i /home/$venvuser/.ssh/id_ecdsa.pub $distuser@bdd1

source $virtenv/bin/activate
ansible-playbook -i inventaire.ini --ask-become-pass centos_postinstall.yml
deactivate
EXITUSER

exit 0