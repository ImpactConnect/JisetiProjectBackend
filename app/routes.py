from flask import render_template, flash, redirect, url_for, jsonify, request, current_app
from app import db, login_manager
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User, RedFlag, Intervention, AdminAction
from app.forms import UserRegistration, UserLogin

def init_routes(app):
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('home'))

        form = UserRegistration()
        if form.validate_on_submit():
            password_hash = generate_password_hash(form.password.data)
            user = User(username=form.username.data, name=form.name.data, phone=form.phone.data, email=form.email.data, password=password_hash)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created!', 'success')
            return redirect(url_for('login'))

        return render_template('register.jsx', title='Register', form=form)

    #user login route
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))

        form = UserLogin()
        if form.validate_on_submit(): #
            user = User.query.filter_by(email=form.email.data).first() #
            if user and check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data) #
                return redirect(url_for('home'))
            else:
                flash('Login unsuccessful. Please check email and password.', 'danger')

        return render_template('login.jsx', title='Login', form=form)

    #User logout
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('home'))

    #display all posts in the home page
    @app.route('/', methods=['GET'])
    @login_required
    def home_page():
        redflag_posts = RedFlag.query.all()
        intervention_posts = Intervention.query.all()
        
        # To display the current user's username
        current_username = current_user.username if current_user.is_authenticated else None

        
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
            location_lat = data.get('location_lat')
            location_long = data.get('location_long')
            image_file = data.get('image_file')
            video_file = data.get('video_file')


            if not title or not description:
                return jsonify({'error': 'Title and description are required'}), 400

            new_redflag = RedFlag(
                title=title,
                description=description,
                location_lat=location_lat,
                location_long=location_long,
                image_file=image_file,
                video_file=video_file,
                user_id=current_user.id
            )

            db.session.add(new_redflag)
            db.session.commit()

            return jsonify({'success': True, 'message': 'RedFlag created successfully'}), 201

        return jsonify({'error': 'Invalid request method'}), 405


    #Create new intervention post
    @app.route('/user/create_intervention', methods=['POST'])
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
    def delete_intervention(intervention_id):
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

    #Access to edit personal redflag post
    @app.route('/user/edit_redflag/<int:redflag_id>', methods=['PUT'])
    @login_required
    def edit_redflag(redflag_id):
        redflag = RedFlag.query.get_or_404(redflag_id)

        if redflag.user_id == current_user.id:
            data = request.json
            title = data.get('title', redflag.title)
            description = data.get('description', redflag.description)
            location_lat = data.get('location_lat', redflag.location_lat)
            location_long = data.get('location_long', redflag.location_long)
            image_file = data.get('image_file', redflag.image_file)

            redflag.title = title
            redflag.description = description
            redflag.location_lat = location_lat
            redflag.location_long = location_long
            redflag.image_file = image_file

            db.session.commit()

            return jsonify({'success': True, 'message': 'Post edited successfully'}), 200
        else:
            return jsonify({'error': 'Unauthorized to edit this Post'}), 403
        
    #Access to edit personal redflag post    
    @app.route('/user/edit_intervention/<int:intervention_id>', methods=['PUT'])
    @login_required
    def edit_intervention(intervention_id):
        intervention = RedFlag.query.get_or_404(intervention_id)

        if intervention.user_id == current_user.id:
            data = request.json
            title = data.get('title', intervention.title)
            description = data.get('description', intervention.description)
            location_lat = data.get('location_lat', intervention.location_lat)
            location_long = data.get('location_long', intervention.location_long)
            image_file = data.get('image_file', intervention.image_file)

            intervention.title = title
            intervention.description = description
            intervention.location_lat = location_lat
            intervention.location_long = location_long
            intervention.image_file = image_file

            db.session.commit()

            return jsonify({'success': True, 'message': 'Post edited successfully'}), 200
        else:
            return jsonify({'error': 'Unauthorized to edit this Post'}), 403
        
        
    #Admin function to change post status
    @app.route('/admin/change_status/<int:post_id>/<string:post_type>', methods=['PUT'])
    @login_required
    def change_status(post_id, post_type):
        if not current_user.is_admin:
            return jsonify({'error': 'Unauthorized to perform this action'}), 403

        post_model = RedFlag if post_type == 'redflag' else Intervention
        post = post_model.query.get_or_404(post_id)

        data = request.json
        status = data.get('status')

        if status not in ['under investigation', 'rejected', 'resolved']:
            return jsonify({'error': 'Invalid status'}), 400

        post.status = status
        db.session.commit()

        admin_action = AdminAction(
            post_id=post_id,
            post_type=post_type,
            status=status,
            admin_id=current_user.id
        )
        db.session.add(admin_action)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Status changed successfully'}), 200
    
    return app
