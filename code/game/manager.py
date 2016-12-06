class Player:
    def __init__(self, name):
        self.i = {'name': name, 'score': 0, 'live': True}

    def __repr__(self):
        return str(self.i)

    def score_up(self):
        self.i['score'] += 1

    def die(self):
        self.i['live'] = False

    def resurrect(self):
        self.i['live'] = True

class PlayerManager:
    def __init__(self):
        pass

    def add(self, player):
        raise NotImplementedError

    def delete(self, pid):
        raise NotImplementedError

    def kill(self, pid):
        raise NotImplementedError

    def ressurect(self, pid):
        raise NotImplementedError

    def get_name(self, pid):
        raise NotImplementedError

    def get_list(self):
        raise NotImplementedError

class MapPlayerManager(PlayerManager):
    def __init__(self):
        super().__init__()
        self.players = {}

    def has(self, pid):
        return pid in self.players

    def add(self, name, pid):
        if not self.has(pid):
            player_dict = Player(name)
            self.players[pid] = player_dict
            return True
        else:
            return False

    def delete(self, pid):
        if self.has(pid):
            self.players.pop(pid)
            return True
        else:
            return False

    def kill(self, killer_pid, killed_pid):
        if self.has(killer_pid) and self.has(killed_pid):
            self.players[killer_pid].score_up()
            self.players[killed_pid].die()
            return True
        else:
            return False

    def ressurect(self, pid):
        if self.has(pid):
            self.players[pid].ressurect()
            return True
        else:
            return False

    def get_name(self, pid):
        if self.has(pid):
            return self.players[pid]
        else:
            return ''

    def get_list(self):
        return self.players

class GameMaster:
    def __init__(self):
        self.ready = False

    def getready(self):
        self.ready = True

    def is_ready(self):
        return self.ready
