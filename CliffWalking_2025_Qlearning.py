#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  9 16:10:03 2021
Derniere modification le 25 novembre 2024

@author: ajuton, a partir d'elements du code de Corentin Dancette
"""
#on importe les modules necessaires
import random 
import time
import numpy as np #module pour le calcul de matrices
from matplotlib import pyplot as plt
from CliffWalking_2025_fenetre import fenetre_apprentissage, espace_de_jeu_apprentissage

#Creation de la fenetre graphique (voir fichier CliffWalking_2023_fenetre_grilletype.py)
fenetre    = fenetre_apprentissage()
espace_jeu = espace_de_jeu_apprentissage(fenetre)

#Definition de l'environnement, etats, recompenses, actions
class Game:
    ACTION_H = 0
    ACTION_G = 1
    ACTION_D = 2
    ACTION_B = 3
    #table des actions possibles
    ACTIONS = [ACTION_H, ACTION_G, ACTION_D, ACTION_B]
    #table des noms des actions
    ACTION_NAMES = ["H", "G", "D", "B"]
    #coordonnees des mouvements
    MOUVEMENTS = {
        ACTION_H: ( 0, -1),
        ACTION_G: (-1,  0),
        ACTION_D: ( 1,  0),
        ACTION_B: ( 0,  1)
    }
    #nombre d'actions possibles
    num_actions = len(ACTIONS)

    #intilialisation de la grille avec largeur, hauteur et wrong_action_p
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.generate_game()

    #renvoie le numero de la case (entre 0 et n*m-1) si on donne x et y
    def _position_to_id(self, x, y):
        return x + y * self.n

    #genere la grille de depart 
    def generate_game(self):
        self.position_lapin     = (0,3)
        self.carotte            = (5,3)
        self.falaise1           = (1,3)
        self.falaise2           = (2,3)
        self.falaise3           = (3,3)
        self.falaise4           = (4,3)
        self.start              = (0,3)
        self.counter            = 0
        return self._get_state()
    
    #repositionne le lapin sur la case de depart de la grille et remet le compteur a 0
    def reset(self) :
        self.position_lapin = self.start
        self.counter = 0
        return self._get_state()

    def _get_state(self) :
        return self._position_to_id(*self.position_lapin)

    #fonction de deplacement : recoit une action et renvoie :
    #le nouvel etat de la grille, la recompense, 
    #si c'est termine (done)
    #Il est possible d'y ajouter un peu d'aleatoire (les glissades du lapin)
    def step(self, action) :
        self.counter += 1
        done = False
        reward = 0

        if action not in self.ACTIONS :
            raise Exception("Invalid action")

        #ajout d'une action aleatoire :
        # le lapin glisse et ne fait pas ce qu'il avait prevu
        #choice = random.random()
        #if choice < 0.1 :
         #   action = (action + 1) % 4
        #elif choice < 2 * 0.1 :
         #   action = (action - 1) % 4

        #calcul du deplacement prevu -> new_x et new_y        
        d_x, d_y     = self.MOUVEMENTS[action]
        x, y         = self.position_lapin
        new_x, new_y = x + d_x, y + d_y

        #calcul des consequences de l'action : 
        #nouvelle position, recompense, fin du jeu, info(inutilisee)
        
        #cas où le lapin tombe de la falaise
        if ((new_x, new_y) == self.falaise1) or ((new_x, new_y) == self.falaise2) or\
              ((new_x, new_y) == self.falaise3) or ((new_x, new_y) == self.falaise4) :
            self.position_lapin = new_x, new_y
            reward = -100
            done = True
        #cas où le lapin arrive a destination
        elif (new_x, new_y) == self.carotte :
            self.position_lapin = new_x, new_y
            reward = +10
            done = True
        #cas où le lapin cherche a sortir de la grille
        elif new_x >= self.n or new_y >= self.m or new_x < 0 or new_y < 0 :
            reward = -1
            done = False
        #cas où l'episode dure depuis trop longtemps
        elif self.counter > 190 :
            self.position_lapin = new_x, new_y
            reward = 0
            done = True
        #cas où le lapin fait un pas sur une case non speciale de la grille
        else :
            self.position_lapin = new_x, new_y
            reward = -0.1
            done = False
            
        return self._get_state(), reward, done
    
    #COMPORTEMENT DE L'environement 

    #affichage du lapin sur sa nouvelle position
    def print(self,espace_jeu) :
        for i in range(self.n - 1, -1, -1) :
            for j in range(self.m) :
                if (i, j)   == self.position_lapin :
                    espace_jeu.espace.coords(espace_jeu.lapin, (i*100+50, j*100+50))
        
#--------------------------------------------------------------------------
#Algorithme d'apprentissage        
states_n = 6*4
num_episodes = 100
actions_n = 4
#Hyper-parametres
alpha = 0.1
gamma = 0.9
epsilon = 0.1

while(True) :
    #initialisations
    cumul_reward_list = []

    #Creation d'un nouvel environnement aleatoire
    game = Game(6, 4)
    game.print(espace_jeu)
    Q = np.zeros([states_n, game.num_actions])
    espace_jeu.espace.update()
    time.sleep(1.0)
    
    #attente du bouton demarrer
    while(not fenetre.bouton_start) :
        espace_jeu.espace.update()
    fenetre.bouton_start=False

    #Demarrage de l'apprentissage sur un nombre d'episodes fixe
    for i in range(num_episodes) :
        print("episode numero "+str(i))
        
        #arret de l'apprentissage si appui sur demarrer
        if(fenetre.bouton_start) :
            fenetre.bouton_start=False
            break
    
        #RAZ de l'environnement au debut de chaque episode
        s            = game.reset() # SARSA : s1 = game.reset()
        cumul_reward = 0
        fin_du_jeu   = False 
        game.print(espace_jeu)
        espace_jeu.espace.update()
        
        ########################################################################################
        # Choix de la premiere action pour SARSA
        if (random.random()<epsilon): #exploration
            a = random.randint(0,3)
        else : #exploitation
            a = np.argmax(Q[s,:])
        
        
        ########################################################################################
        time.sleep(0.2)
        
        #demarrage de l'apprentissage jusqu'a la fin de l'episode (falaise ou Carotte trouves)
        while True:
                  
            ###################################################################################
            # Exploration / Exploitation, Pas a pas et Mise a jour de Q
            s1, reward, fin_du_jeu = game.step(a) #on recupere action avec nouvelle etat et recompense
        
            
            epsilon = 1/(1+num_episodes)  
            if (random.random()<epsilon): #exploration
                a1 = random.randint(0,3)
            else : #exploitation
                a1 = np.argmax(Q[s1,:])  

            Q[s,a] = Q[s,a] + alpha*(reward+gamma*np.max(Q[s1,:])-Q[s,a])
            cumul_reward += reward # nouvelle recompense 
            s = s1 #nouvelle etat 
            a = a1 # nouvelle action
            
            
            ###################################################################################
            
            #Mise a jour de l'affichage
            game.print(espace_jeu)
            espace_jeu.espace.update()
 
            #affichage de la Qtable
            fenetre.affichage_de_la_qtable(Q,game.num_actions,game.ACTION_NAMES)
  
            #si mode auto, on attend duree_entre_2_tests, si mode_manu, on attend le bouton pas_suivant
            if(fenetre.mode_manuel == False) :
                duree_entre_2_tests=float(fenetre.duree_entre_2_tests_recu.get()) #duree_entre_2_tests .5 par defaut
                time.sleep(duree_entre_2_tests)
            else:
                while fenetre.pas_suivant == False :
                    espace_jeu.espace.update()
                fenetre.pas_suivant = False #une fois pas_suivant pris en compte, on le remet a zero
            
            # si fin du jeu ou start, on recommence un nouvel episode
            if fin_du_jeu == True or fenetre.bouton_start == True:
                break            
            
        #sauvegarde des historiques des recompenses
        cumul_reward_list.append(cumul_reward)
    
    #A la fin, affichage du score.
    print("Score final : " +  str(sum(cumul_reward_list[-100:])/100.0))
    plt.plot(cumul_reward_list[0:len(cumul_reward_list)-1])
    plt.show()
    espace_jeu.espace.update()
espace_jeu.espace.mainloop()