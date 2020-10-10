import requests
import time

class Telecommande():
    def __init__(self):

        self.code = ""
        self.server_freebox = "http://mafreebox.freebox.fr/"
        self.url_freebox = "http://hd1.freebox.fr/"
        self.url_remote = "{}pub/remote_control?".format(self.url_freebox)
        self.dict_channel = {}
        self.programme_url = "{}api/v3/tv/epg/by_channel".format(self.server_freebox, )


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

        self.get_chaine()

    def get_chaine(self):
        list_channel = requests.get("{}api/v8/tv/channels/".format(self.server_freebox)).json()

        for channel, value in list_channel['result'].items():
            code_channel = value['uuid']
            channel_name = value['name']

            if value['available'] or value['has_abo']:
                self.dict_channel[channel_name] = code_channel

    def get_programme(self, channel):
        now=int(time.time())
        now = now-now%7200
        programme = requests.get('{}/{}/{}'.format(self.programme_url, self.dict_channel[channel], now+7200)).json()
        return programme

    def change_channel(self, channel=""):

        if channel != "":
            self.multi_commande(list(channel))

    def commande(self, commande):
        send = requests.get(
        "{}code={}&key={}".format(self.url_remote,
                                  self.code,
                                  self.dict_commande[commande]
        ))

        if send.status_code == 200:
            time.sleep(2.5) # wait commande execute

    def multi_commande(self, list_commande, count_timesleep=5, timesleep=4, chan_change=True):

        send = requests.get(
        "{}code={}&key=1".format(self.url_remote,
                                  self.code,
                                  #self.dict_commande[commande],
                                  #repeat
        ))
        send = requests.get(
        "{}code={}&key=5".format(self.url_remote,
                                  self.code
        ))
        send = requests.get(
        "{}code={}&key=5".format(self.url_remote,
                                  self.code,
        ))
        send = requests.get(
        "{}code={}&key".format(self.url_remote,
                                  self.code,
        ))
        for i, commande in enumerate(list_commande):

            send = requests.get(
            "{0}code={1}&key={2}".format(self.url_remote,
                                      self.code,
                                      self.dict_commande[commande],
            ))

            if not chan_change:
                if send.status_code == 200:
                    time.sleep(0.3) # wait commande execute

                if i % count_timesleep == count_timesleep-1:
                    time.sleep(timesleep) # wait 2 secondes after 5 commandes send

        if chan_change:
            send = requests.get(
            "{}code={}&key".format(self.url_remote,
                                      self.code,
            ))
            time.sleep(timesleep)

if __name__ == "__main__":
    telecommande = Telecommande()
    
    # Telecommande send button
    telecommande.multi_commande(["ok"]) # or
    
    # change channel
    telecommande.change_channel("15") # or
    
    # list multi button
    #telecommande.multi_commande(["1", "5"]) # or
    #telecommande.multi_commande(["up", "down"], chan_change=False)
    
    # get TV list programme 
    telecommande.get_programme("TF1")
