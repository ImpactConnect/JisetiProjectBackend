from flask import Flask, jsonify, Blueprint, render_template, flash, url_for, redirect, request
from forms import UserRegistration, UserLogin, AdminRegistration, AdminLogin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, User, RedFlag, Intervention
from flask_cors import CORS 
# from flask_simple_geoip import SimpleGeoIP



app = Flask(__name__)
CORS(app) 
# app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['GEOIP_DATABASE_PATH'] = 'GeoLite2-City.mmdb'
# simple_geoip = SimpleGeoIP(app)

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

# @app.route('/')
# def get_location():
#     location = simple_geoip.get_location()
#     # return jsonify(data=geoip_data)
#     return f'Your location: {location}'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = UserRegistration()
    if form.validate_on_submit():
        user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data, phone=form.phone.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))

    return render_template('register.jsx', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = UserLogin()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')

    return render_template('login.jsx', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

#display all users' posts after login
@app.route('/all_posts', methods=['GET'])
@login_required
def home_page():
    redflag_posts = RedFlag.query.all()
    intervention_posts = Intervention.query.all()
    redflags_data = [{
            'poster': User.query.get(redflag.user_id).username,
            'title': redflag.title,
            'description': redflag.description,
            'location': redflag.location,
            'image_file': redflag.image_file,
            'video_file': redflag.video_file,
            'date': redflag.date,
            'status': redflag.status}     
                for redflag in redflag_posts]
    
    interventions_data =[{
        'poster': User.query.get(intervention.user_id).username,
        'title': intervention.title,
        'description': intervention.description,
        'location': intervention.location,
        'image_file': intervention.image_flag,
        'date': intervention.date,
        'status': intervention.status
    } for intervention in intervention_posts]
    
    return jsonify({'redflag_posts': redflags_data, 'intervention_posts': interventions_data})

    
@app.route('/about')
def about():
    return render_template('about')


#User access to his personal posts after login
@app.route('/posts', methods=['GET'])
@login_required
def posts():
    redflags = RedFlag.query.filter_by(user_id=current_user.id).all()
    interventions = Intervention.query.filter_by(user_id=current_user.id).all()

    return render_template('posts.jsx', title='Posts', redflags=redflags, interventions=interventions)

#User filtering personal redflag posts
@app.route('/user/redflags', methods=['GET'])
@login_required
def get_user_redflags():
    redflags = RedFlag.query.filter_by(user_id=current_user.id).all()
    return jsonify([redflag.serialize() for redflag in redflags])

#User filtering personal intervention posts
@app.route('/user/interventions', methods=['GET'])
@login_required
def get_user_interventions():
    interventions = Intervention.query.filter_by(user_id=current_user.id).all()
    return jsonify([intervention.serialize() for intervention in interventions])


#Create new redflag post
@app.route('/user/create_redflag', methods=['POST'])
@login_required
def create_redflag():
    if request.method == 'POST':
        data = request.json
        title = data.get('title')
        description = data.get('description')
        # location_lat = data.get('location_lat')
        # location_long = data.get('location_long')
        image_file = data.get('image_file')
        video_file = data.get('video_file')


        if not title or not description:
            return jsonify({'error': 'Title and description are required'}), 400

        new_redflag = RedFlag(
            title=title,
            description=description,
            # location_lat=location_lat,
            # location_long=location_long,
            image_file=image_file,
            video_file=video_file,
            user_id=current_user.id
        )

        db.session.add(new_redflag)
        db.session.commit()

        return jsonify({'success': True, 'message': 'RedFlag created successfully'}), 201

    return jsonify({'error': 'Invalid request method'}), 405


#Create new intervention post
@app.route('/user/create_redflag', methods=['POST'])
@login_required
def create_intervention():
    if request.method == 'POST':
        data = request.json
        title = data.get('title')
        description = data.get('description')
        location_lat = data.get('location_lat')
        location_long = data.get('location_long')
        image_file = data.get('image_file')
        video_file = data.get('video_file')

        if not title or not description:
            return jsonify({'error': 'Title and description are required'}), 400

        new_intervention = RedFlag(
            title=title,
            description=description,
            location_lat=location_lat,
            location_long=location_long,
            image_file=image_file,
            video_file=video_file,
            user_id=current_user.id
        )

        db.session.add(new_intervention)
        db.session.commit()

        return jsonify({'success': True, 'message': 'RedFlag created successfully'}), 201

    return jsonify({'error': 'Invalid request method'}), 405

#User delete intervention post
@app.route('/user/delete_intervention/<int:intervention_id>', methods=['DELETE'])
@login_required
def delete_redflag(intervention_id):
    intervention = Intervention.query.get_or_404(intervention_id)

    if intervention.user_id == current_user.id:
        db.session.delete(intervention)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Post deleted successfully'}), 200
    else:
        return jsonify({'error': 'Unauthorized to delete this Post'}), 403

#user delete redflag post
@app.route('/user/delete_redflag/<int:redflag_id>', methods=['DELETE'])
@login_required
def delete_redflag(redflag_id):
    redflag = RedFlag.query.get_or_404(redflag_id)

    if redflag.user_id == current_user.id:
        db.session.delete(redflag)
        db.session.commit()
        return jsonify({'success': True, 'message': 'RedFlag deleted successfully'}), 200
    else:
        return jsonify({'error': 'Unauthorized to delete this RedFlag'}), 403
