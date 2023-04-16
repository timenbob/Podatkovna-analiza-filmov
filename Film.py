class Film:
    
    def __init__(self,ime,leto=0,poraba='-',zasluzek='-',nagrade=0,nominacije=0):
        self.ime=ime
        self.leto=leto
        self.poraba=poraba
        self.zasluzek=zasluzek
        self.nagrade=nagrade
        self.nominacije=nominacije


    def get_ime(self):
        return self.ime
    def get_leto(self):
        return self.leto
    def get_poraba(self):
        return self.poraba
    def get_zasluzek(self):
        return self.zasluzek
    def get_nagrade(self):
        return self.nagrade
    def get_nominacije(self):
        return self.nominacije


    


