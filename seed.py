# run.py

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from app.models import User, RedFlag, Intervention, AdminAction

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def seed_db():
    """Seed the database with dummy data."""
    # Add your code here to create and add dummy data to the database
    # For example:
    user = User(username='dummy_user', name='Dummy User', email='dummy@example.com', password='password', phone_number='1234567890')
    db.session.add(user)

    redflag = RedFlag(title='Dummy RedFlag', description='This is a dummy red flag.', image_file='dummy.jpg', video_file='dummy.mp4', user=user)
    db.session.add(redflag)

    intervention = Intervention(title='Dummy Intervention', description='This is a dummy intervention.', image_file='dummy.jpg', video_file='dummy.mp4', user=user)
    db.session.add(intervention)

    admin_action = AdminAction(post_id=redflag.id, post_type='redflag', status='resolved', admin_id=user.id)
    db.session.add(admin_action)

    db.session.commit()
    print('Database seeded successfully.')

if __name__ == '__main__':
    manager.run()
