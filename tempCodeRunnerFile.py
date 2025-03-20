class projects(db.Model):
    __tablename__ = 'projects'
    projectname = db.Column(db.String(100), unique=True, primary_key=True)
    quotedamount = db.Column(db.BigInteger, nullable=False, default=0)
    totexpense = db.Column(db.BigInteger, nullable=False)
    startdate = db.Column(db.Date, nullable=False)  # Add this line
    duration = db.Column(db.Integer, nullable=False)  # Add this line

    def __init__(self, projectname, quotedamount, totexpense, startdate, duration):
        self.projectname = projectname
        self.quotedamount = quotedamount
        self.totexpense = totexpense
        self.startdate = startdate  # Add this line
        self.duration = duration  # Add this line
