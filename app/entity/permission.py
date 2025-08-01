from app.database import db

class Permission(db.Model):
    __tablename__ = 'permission'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    endpoint = db.Column(db.String(200))

    role_permission = db.relationship('RolePermissions', back_populates='permission')

    def __repr__(self):
        return f"<Permission(id='{self.id}', name='{self.name}')>"