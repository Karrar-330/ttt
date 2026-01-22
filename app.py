# app.py
from flask import Flask, render_template
from extensions import db, login_manager, bcrypt

def create_app():
    app = Flask(__name__)
    
    # إعدادات
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'clinic-secret-key-123'
    
    # تهيئة الإضافات
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    # تعريف user_loader
    @login_manager.user_loader
    def load_user(user_id):
        from modules.auth import User
        return User.query.get(int(user_id))
    
    # استيراد وتسجيل Blueprints
    from modules.dashboard import dashboard_bp
    from modules.patients import patients_bp
    from modules.visits import visits_bp
    from modules.reception import reception_bp
    from modules.auth import auth_bp
    from modules.clinic_setup import clinic_bp
    from modules.users import users_bp
    from modules.accounting import accounting_bp
    from modules.secretary import secretary_bp
    
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(visits_bp)
    app.register_blueprint(reception_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(clinic_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(accounting_bp)
    app.register_blueprint(secretary_bp)
    
    # صفحات الأخطاء
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return render_template('500.html'), 500
    
    # إنشاء الجداول
    with app.app_context():
        db.create_all()
        
        from modules.auth import User
        from modules.clinic_setup import ClinicSettings
        
        if not User.query.first():
            print("\n" + "="*50)
            print("🚀 نظام إدارة العيادة")
            print("="*50)
            print("⚠️  لا يوجد مستخدمين في النظام")
            print("🔧 قم بزيارة: http://localhost:5000/clinic/setup للإعداد الأولي")
            print("="*50 + "\n")
        
        if not ClinicSettings.query.first():
            settings = ClinicSettings(
                clinic_name='عيادتي',
                doctor_name='الدكتور',
                visit_fee=100.0,
                currency='د.ع'
            )
            db.session.add(settings)
            db.session.commit()
            print("✅ تم إنشاء إعدادات العيادة الافتراضية")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)