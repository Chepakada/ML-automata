from app import db, ma
from datetime import datetime

class Files(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(120), unique = True, nullable = False)
    filepath = db.Column(db.String(120), nullable = False)

    def __repr__(self):
        return "<Files %r>" % self.parameter

class FilesShema(ma.Schema):
    class Meta:
        fields = ("id", "filename", "filepath")

article_schema = FilesShema()

articles_schema = FilesShema(many = True)
    