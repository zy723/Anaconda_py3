from common.models import db


class City(db.Model):
    """
    城市模型
    """
    __tablename__ = "areas"
    id = db.Column(db.Integer, primary_key=True, doc="城市ID")
    name = db.Column(db.String(20), doc="城市名字")
    parent_id = db.Column("pid", db.Integer, db.ForeignKey("areas.id"), doc="父类ID")

    # 关系属性
    parent = db.relationship("City", remote_side=[id], backref=db.backref("childs", lazy="dynamic"))
