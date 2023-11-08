from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class H1bRow(db.Model):

    __tablename__ = "h1b_rows"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employer = db.Column(db.String, nullable=False)
    job_title = db.Column(db.String, nullable=False)
    base_salary = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    
    def __init__(self, **kwargs):
        self.employer = kwargs.get("employer")
        self.job_title = kwargs.get("job_title")
        self.base_salary = kwargs.get("base_salary")
        self.location = kwargs.get("location")
        
    def serialize(self):
        return {
            "id": self.id,
            "employer": self.employer,
            "job_title": self.job_title,
            "base_salary": self.base_salary,
            "location": self.location
        }