# clean_start.py
import os
import sys

def clean_database():
    """حذف وإعادة إنشاء قاعدة البيانات"""
    
    print("🧹 تنظيف وإعادة تهيئة النظام")
    print("-" * 40)
    
    # حذف قاعدة البيانات
    db_files = ['clinic.db', 'instance/clinic.db']
    deleted = False
    
    for db_file in db_files:
        if os.path.exists(db_file):
            os.remove(db_file)
            print(f"✅ تم حذف: {db_file}")
            deleted = True
    
    if not deleted:
        print("ℹ️  لم يتم العثور على قاعدة بيانات قديمة")
    
    # استيراد وإنشاء التطبيق
    try:
        from app import create_app
        from extensions import db
        
        app = create_app()
        
        with app.app_context():
            # إنشاء الجداول
            db.create_all()
            
            # عرض الجداول المنشأة
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print("\n📊 الجداول المنشأة:")
            for table in tables:
                print(f"   • {table}")
            
            print("\n" + "="*40)
            print("🎉 تم إعداد النظام بنجاح!")
            print("="*40)
            print("\n📋 خطوات البدء:")
            print("1. افتح المتصفح واذهب إلى: http://localhost:5000")
            print("2. انتقل إلى: /clinic/setup للإعداد الأولي")
            print("3. أدخل بيانات العيادة والحساب الرئيسي")
            print("4. سجل الدخول وابدأ استخدام النظام")
            print("\n⚡ للحصول على مساعدة: python app.py --help")
            
    except Exception as e:
        print(f"❌ خطأ أثناء إنشاء قاعدة البيانات: {e}")
        sys.exit(1)

if __name__ == '__main__':
    # طلب التأكيد
    print("⚠️  هذا الإجراء سيقوم بحذف جميع البيانات الحالية!")
    confirm = input("هل تريد المتابعة؟ (اكتب 'نعم' للموافقة): ")
    
    if confirm.strip().lower() in ['نعم', 'yes', 'y']:
        clean_database()
    else:
        print("❌ تم إلغاء العملية")