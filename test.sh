#!/bin/bash


virtenv=""
chemabs="^/*"

while [[ "$virtenv" != /* ]] ; do
    echo "Indiquez le nom de l'environnement virtuel à créer"
    read -p "(chemin absolu): " virtenv
done


echo $virtenv

exit 0