#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 22:29:53 2022
Modifie le 21 novembre 2023

@author: ajuton
"""

import tkinter #module gerant l'affichage
import os

#definition du chemin des images
current_path = os.path.dirname(__file__) # localisation du fichier .py
lapin_png = os.path.join(current_path, "lapin.png")
falaise_png = os.path.join(current_path, "falaise.png")
carotte_png = os.path.join(current_path, "carotte.png")

class fenetre_apprentissage :
    #fonctions associees aux boutons
    def demarrer(self):
        self.bouton_start = True
               
    def fonction_mode_manuel(self):
        print(self.mode_manuel)
        if self.mode_manuel == False :
            #on passe en mode manuel, les boutons passent en rouge
            self.mode_manuel = True
            self.bouton2.configure(bg="red")
            self.bouton2.configure(activebackground="salmon")
            self.bouton3.configure(bg="red")
            self.bouton3.configure(activebackground="salmon")
        else:
            #on repasse en mode auto, les boutons reprennent la couleur d'origine
            self.mode_manuel = False
            self.bouton2.configure(bg='#d9d9d9')
            self.bouton2.configure(activebackground='#ececec')
            self.bouton3.configure(bg='#d9d9d9')
            self.bouton3.configure(activebackground='#ececec')
            
    
    def mouvement_suivant(self) :
        self.pas_suivant = True
        
    def __init__(self):
        #Creation de la fenetre de parametres
        self.bouton_start = False
        self.mode_manuel = False
        self.pas_suivant = False
        self.grille_type = False
        self.fenetre = tkinter.Tk()
        self.fenetre.title("Cliff Walking")
        cadre =tkinter.LabelFrame(self.fenetre,bg ="gray85",border =3, relief =tkinter.GROOVE,text="Controles", width = 600)
        cadre.grid(row=0, column=0)
        self.bouton0 = tkinter.Button(cadre, text ="Quitter", command =self.fenetre.destroy)
        self.bouton0.pack(side =tkinter.LEFT)
        self.bouton1 = tkinter.Button(cadre, text ="Demarrer / Nouvel episode", command =self.demarrer)
        self.bouton1.pack(side =tkinter.LEFT)
        self.bouton2 = tkinter.Button(cadre, text ="Mode_manuel", command = self.fonction_mode_manuel)
        self.bouton2.pack(side =tkinter.LEFT)
        self.bouton3 = tkinter.Button(cadre, text ="Mouvement suivant", command = self.mouvement_suivant)
        self.bouton3.pack(side =tkinter.LEFT)

        cadre2 =tkinter.LabelFrame(self.fenetre,bg ="gray85",border =3, relief =tkinter.GROOVE,text="Hyper parametres",width = 600)
        cadre2.grid(row=0, column=1)
        invite3 =tkinter.Label(cadre2, text ='duree entre 2 test en s :', width =20, height =1, fg ="navy")
        invite3.pack()
        self.duree_entre_2_tests_recu=tkinter.DoubleVar()  # definition d'une variable-chaine pour recevoir la saisie d'un nombre
        self.duree_entre_2_tests_recu.set("0.1")  # facultatif: assigne une valeur a la variable
        saisie3 =tkinter.Entry(cadre2,textvariable =self.duree_entre_2_tests_recu, width =10)
        saisie3.pack()
        
        #Creation de l'espace d'affichage de la Qtable
        self.espace_qtable = tkinter.Canvas(self.fenetre, width = 600, height = 400)
        self.espace_qtable.grid(row = 1, column =0 )
        
        self.rectangle = []
        self.valeur_qtable=[]
        self.espace_qtable.create_text(200, 10, font=("Arial Black",14),text="valeurs de la qtable",justify = tkinter.LEFT)
        for j_ligne in range(0,4):
            for action in range(0,4):
                for i_col in range (0,6):
                    couleur_fond = '#%02x%02x%02x'% (128,128, 128)
                    self.rectangle.append(self.espace_qtable.create_rectangle(65+i_col*64,27+j_ligne*102.5+action*17,65+i_col*64+58,27+j_ligne*102.5+action*17+15,outline = couleur_fond,fill=couleur_fond))
            self.valeur_qtable.append(self.espace_qtable.create_text(260, 70+j_ligne*102.5, font=("Arial Black",9),text="",justify = tkinter.LEFT))
        self.espace_qtable.update()
        
    def affichage_de_la_qtable(self,Q,num_actions,nom_action) :
        for j_ligne in range(0,4):
            chaine_qtable = ""
            for action in range(num_actions):
                for i_col in range (0,6):
                    couleur_fond = '#%02x%02x%02x' % (max(min(128-int(Q[(j_ligne*6+i_col),action]*12.8),255),0), max(min(128+int(Q[(j_ligne*6+i_col),action]*12.8),255),0), max(min(128-abs(int(Q[(j_ligne*6+i_col),action]*12.8)),128),0))  
                    self.espace_qtable.itemconfigure(self.rectangle[j_ligne*24+action*6+i_col],outline=couleur_fond,fill=couleur_fond)
                    chaine_qtable += nom_action[action]+str(" %3.2f" % Q[(j_ligne*6+i_col),action])+"\t"
                chaine_qtable+="\n"
            self.espace_qtable.itemconfigure(self.valeur_qtable[j_ligne], text=chaine_qtable)
        self.espace_qtable.update()
        
        
    

class espace_de_jeu_apprentissage :
    def __init__(self,fenetre):
        #Creation de l'espace de jeu et des acteurs
        self.espace = tkinter.Canvas(fenetre.fenetre, width = 600, height = 400)
        self.espace.grid(row = 1, column =1)
        #self.espace.pack()
        self.espace.create_line(100,0,100,400, fill="gray")
        self.espace.create_line(200,0,200,400, fill="gray")
        self.espace.create_line(300,0,300,400, fill="gray")
        self.espace.create_line(400,0,400,400, fill="gray")
        self.espace.create_line(500,0,500,400, fill="gray")
        self.espace.create_line(00,100,600,100, fill="gray")
        self.espace.create_line(00,200,600,200, fill="gray")
        self.espace.create_line(00,300,600,300, fill="gray")
        
        
        self.image_lapin =tkinter.PhotoImage(file =lapin_png)  # ouverture d'un fichier PNG existant
        largeur_lapin =self.image_lapin.width(); hauteur_lapin =self.image_lapin.height() # determination des dimensions
        self.lapin =self.espace.create_image(largeur_lapin//2+20, hauteur_lapin//2+1, image =self.image_lapin) # image a centrer
        
        self.image_falaise =tkinter.PhotoImage(file =falaise_png)  # ouverture d'un fichier PNG existant
        largeur_falaise =self.image_falaise.width(); hauteur_falaise =self.image_falaise.height() # determination des dimensions
        self.falaise1 =self.espace.create_image(1*100+50, 3*100+50, image =self.image_falaise) # image a centrer
        self.falaise2 =self.espace.create_image(2*100+50, 3*100+50, image =self.image_falaise) # image a centrer
        self.falaise3 =self.espace.create_image(3*100+50, 3*100+50, image =self.image_falaise) # image a centrer
        self.falaise4 =self.espace.create_image(4*100+50, 3*100+50, image =self.image_falaise) # image a centrer

        self.image_carotte =tkinter.PhotoImage(file =carotte_png)  # ouverture d'un fichier PNG existant
        largeur_carotte =self.image_carotte.width(); hauteur_carotte =self.image_carotte.height() # determination des dimensions
        self.carotte =self.espace.create_image(largeur_carotte//2+520, hauteur_carotte//2+300, image =self.image_carotte) # image a centrer
        
        self.espace.update()    
        
