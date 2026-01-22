# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

# إعدادات Flask-Login
login_manager.login_view = 'auth.login'
login_manager.login_message = 'الرجاء تسجيل الدخول للوصول إلى هذه الصفحة'
login_manager.login_message_category = 'warning'

# يجب تعريف user_loader هنا أو في مكان يمكن استيراده
@login_manager.user_loader
def load_user(user_id):
    from modules.auth import User
    return User.query.get(int(user_id))