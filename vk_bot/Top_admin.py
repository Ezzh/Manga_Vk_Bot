class Top_admin:
    def __init__(self, id, status, db):
        self.id = id
        self.status = status
        self.proverka = None
        self.db = db

    def accept(self):
        self.db.adding_captain(self.proverka[0], self.proverka[1])
        self.db.removal_captain_to_the_check(self.proverka[0])

    def deny(self):
        self.db.removal_captain_to_the_check(self.proverka[0])
