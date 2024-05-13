
from datetime import datetime

class Files(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    file = db.Column(db.LargeBinary, nullable = False)
    date = db.Column(db.DateTime(), default = datetime.now())

    def __repr__(self):
        return "<Files %r>" % self.title

class FilesShema(ma.Schema):
    class Meta:
        fields = ("id", "title", "file", "date")

article_schema = FilesShema()

article_schema = FilesShema(many = True)
    