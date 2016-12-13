class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    league_position = db.Column(db.Integer, unique=True)

    @staticmethod
    def insert_teams():
        '''
        @param id_names: Dictionary with the ids and names of the league teams
        '''
        ids_names = faw.ids_names

        for id, name in ids_names.items():
            team = Team.query.filter_by(id=id).first()
            if team is None:
                team = Team()
            team.id = id
            team.name = name
            db.session.add(team)
        db.session.commit()

    def __repr__(self):
        return '<TEAM> {}/{} league_position:{}'.format(
            self.id,
            self.name,
            self.league_position
            )

class Match(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime())
    time = db.Column(db.DateTime())
    played = db.Column(db.Boolean)
    hometeam_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    awayteam_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    hometeam_score = db.Column(db.Integer)
    awayteam_score = db.Column(db.Integer)
    #plays = db.relationship('', backref='role', lazy='dynamic')

    '''
    @staticmethod
    def insert_old_matches():
        pass
    '''

    def __repr__(self):
        return "<Match> date:{} home_team_id:{} away_team_id:{} score:{}-{} played?:{}".format(
            self.date,
            self.hometeam_id,
            self.awayteam_id,
            self.hometeam_score,
            self.awayteam_score,
            self.played
            )
