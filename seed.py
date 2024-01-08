from app import create_app, db
from app.models import User, RedFlag, Intervention

def seed_data():
    app = create_app()
    with app.app_context():
        # Seed users
        user01 = User(username='testusr', name='Test Userr', email='tes11@example.com', password='password123', phone_number=1084767890)
        user22 = User(username='tesuser0', name='Test User r0', email='tes22@example.com', password='password456', phone_number=9872542710)

        db.session.add_all([user01, user22])

        # Commit the changes
        db.session.commit()

        # Create RedFlag posts
        redflag1 = RedFlag(title='Red Flag 1', description='Lorem ipsum dolor sit amet consectetur adipisicing elit. Ullam esse blanditiis, sapiente neque, corporis aliquid cum exercitationem libero maiores atque maxime itaque. Rem harum autem modi voluptates ut ex distinctio.1', user=user01, location_lat=12.345, location_long=67.890, image_file='redflag1.jpg', video_file='redflag1.mp4', status='pending', admin_id=5)
        redflag2 = RedFlag(title='Red Flag 2', description='Lorem ipsum dolor sit amet consectetur adipisicing elit. Ullam esse blanditiis, sapiente neque, corporis aliquid cum exercitationem libero maiores atque maxime itaque. Rem harum autem modi voluptates ut ex distinctio.2', user=user22, location_lat=98.765, location_long=43.210, image_file='redflag2.jpg', video_file='redflag2.mp4', status='pending', admin_id=5)

        db.session.add_all([redflag1, redflag2])

        # Create Intervention posts
        intervention1 = Intervention(title='Intervention 1', description='Lorem ipsum dolor sit amet consectetur adipisicing elit. Ullam esse blanditiis, sapiente neque, corporis aliquid cum exercitationem libero maiores atque maxime itaque. Rem harum autem modi voluptates ut ex distinctio.3', user=user01, location_lat=12.345, location_long=67.890, image_file='intervention1.jpg', video_file='intervention1.mp4', status='pending', admin_id=5)
        intervention2 = Intervention(title='Intervention 2', description='Lorem ipsum dolor sit amet consectetur adipisicing elit. Ullam esse blanditiis, sapiente neque, corporis aliquid cum exercitationem libero maiores atque maxime itaque. Rem harum autem modi voluptates ut ex distinctio.4', user=user22, location_lat=98.765, location_long=43.210, image_file='intervention2.jpg', video_file='intervention2.mp4', status='pending', admin_id=5)

        db.session.add_all([intervention1, intervention2])

        # Commit the changes
        db.session.commit()

if __name__ == '__main__':
    seed_data()
