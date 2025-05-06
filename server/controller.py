from server.models import db, User


class UserController:
    @staticmethod
    def create_user(data):
        user = User(username=data['username'].encode('utf-8'), email=data['email'])
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_all_users():
        return User.query.all()