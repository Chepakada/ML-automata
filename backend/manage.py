def deploy():
    '''Run deployment tasks'''

    from app import create_app, db
    
    from flask_migrate import upgrade, migrate, init, stamp
    from models import Files

    app = create_app()
    app.app_context().push()
    print("something was done")

    db.create_all()


    stamp()
    migrate()
    upgrade()

deploy()
