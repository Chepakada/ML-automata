from app import db, ma
from datetime import datetime

class Files(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(120), unique = False, nullable = False)
    filepath = db.Column(db.String(120), nullable = False)

    def __repr__(self):
        return "<Files %r>" % self.filename
    

class Column(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    column_name = db.Column(db.String(120), unique =False, nullable = False)

    def __repr__(self):
        return f"{self.column_name}"

class FilesShema(ma.Schema):
    class Meta:
        fields = ("id", "filename", "filepath")

   
class ColumnShema(ma.Schema):
    class Meta:
        fields = ("id", "column_name")

article_schema = FilesShema()

articles_schema = FilesShema(many = True)
    