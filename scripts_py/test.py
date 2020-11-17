#!/usr/bin/env python3
#-*- coding: utf-8 -*-

chaine = "name"
new_chaine = "new_name"
IP = "127.0.1.1"
hsts = open("test.txt", "r")
contenu = hsts.read()
hsts.close()
if chaine in contenu:
    contenu = contenu.replace(chaine, new_chaine)
else:
    print(contenu)
    print()
    for ligne in contenu.split("\n"):
        print(ligne)
        print()
        if IP in ligne:
            ligne += "\n127.0.1.1   {}".format(new_chaine)
            print(ligne)
hsts = open("test.txt", "w")
hsts.write(contenu)
hsts.close()