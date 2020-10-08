import requests
import time

class Telecommande():
    def __init__(self):

        self.code = ""

        self.dict_commande = {
            "red": "red", # Bouton roug
            "green": "green", # Bouton vert
            "blue": "blue", # Bouton bleu
            "yellow": "yellow", # Bouton jaune


            "power": "power", # Bouton Power
            "list": "list", # Affichage de la liste des chaines
            "tv": "tv", # Bouton tv

            "1": "1", # Bouton 1
            "2": "2", # Bouton 2
            "3": "3", # Bouton 3
            "4": "4", # Bouton 4
            "5": "5", # Bouton 5
            "6": "6", # Bouton 6
            "7": "7", # Bouton 7
            "8": "8", # Bouton 8
            "9": "9", # Bouton 9

            "back": "back", # Bouton jaune (retour)
            "0": "0", # Bouton 0
            "swap": "swap", # Bouton swap

            "info": "info", # Bouton info
            "epg": "epg", # Bouton epg (fct+)
            "mail": "mail", # Bouton mail
            "media": "media", # Bouton media (fct+)
            "help": "help", # Bouton help
            "options": "options", # Bouton options (fct+)
            "pip": "pip", # Bouton pip

            "vol_inc": "vol_inc", # Bouton volume +
            "vol_dec": "vol_dec", # Bouton volume -

            "ok": "ok", # Bouton ok
            "up": "up", # Bouton haut
            "right": "right", # Bouton droite
            "down": "down", # Bouton bas
            "left": "left", # Bouton gauche

            "prgm_inc": "prgm_inc", #Bouton programme +
            "prgm_dec": "prgm_dec", # Bouton programme -

            "mute": "mute", # Bouton sourdine
            "home": "home", # Bouton Free
            "rec": "rec", # Bouton Rec

            "bwd": "bwd", # Bouton << retour arrière
            "prev": "prev", # Bouton |<< précédent
            "play": "play", # Bouton Lecture / Pause
            "fwd": "fwd", # Bouton >> avance rapide
            "next": "next", # Bouton >>| suivant
        }

    def commande(self, commande):
        send = requests.get("http://hd1.freebox.fr/pub/remote_control?code={}&key={}".format(self.code, self.dict_commande[commande]))
        if send.status_code == 200:
            time.sleep(2.5) # wait commande execute

    def multi_commande(self, list_commande, count_timesleep=5):
        for i, commande in enumerate(list_commande):
            send = requests.get("http://hd1.freebox.fr/pub/remote_control?code={}&key={}".format(self.code, self.dict_commande[commande]))
            if send.status_code == 200:
                time.sleep(0.3) # wait commande execute

            if i % count_timesleep == count_timesleep-1:
                time.sleep(2.3) # wait 2 secondes after 5 commandes send

if __name__ == "__main__":
    telecommande = Telecommande()
    telecommande.multi_commande(["up", "down", "up", "down", "up",
                                 "down", "up", "down", "up", "down",
                                 "down", "up", "down", "up", "down"])
