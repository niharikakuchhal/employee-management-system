from flask import request, jsonify, render_template, redirect, url_for, session, flash
from app import app, db
from app.models import Employee, Experience
from werkzeug.security import generate_password_hash, check_password_hash

# Registration endpoint
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return 'Passwords do not match', 400  # Or render_template with an error message
        
        hashed_password = generate_password_hash(password)

        new_user = Employee(name=name, phone=phone, email=email, password=hashed_password, status='active')
        
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    
    return render_template('register.html')

# Login endpoint
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Employee.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid email or password'
    
    return render_template('login.html')

# Dashboard/Experience endpoint
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = Employee.query.get(user_id)

    if request.method == 'POST':
        company_name = request.form.get('company_name')
        role = request.form.get('role')
        date_of_joining = request.form.get('date_of_joining')
        last_date = request.form.get('last_date')

        new_experience = Experience(employee_id=user.id, company_name=company_name, role=role, date_of_joining=date_of_joining, last_date=last_date)
        
        db.session.add(new_experience)
        db.session.commit()

        return redirect(url_for('dashboard'))

    experiences = Experience.query.filter_by(employee_id=user.id).all()
    return render_template('dashboard.html', experiences=experiences, user=user)

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/save_experience', methods=['POST'])
def save_experience():
    # print('From data: ',request.form)
    if 'user_id' not in session:
        # Redirect to login if the user is not logged in
        flash('Please log in to save experiences.', 'info')
        return redirect(url_for('login'))

    user_id = session['user_id']
    company_names = request.form.getlist('company_name[]')
    roles = request.form.getlist('role[]')
    dates_of_joining = request.form.getlist('date_of_joining[]')
    last_dates = request.form.getlist('last_date[]')

    # Assuming all lists are of the same length
    for i in range(len(company_names)):
        new_experience = Experience(
            employee_id=user_id,
            company_name=company_names[i],
            role=roles[i],
            date_of_joining=dates_of_joining[i],
            last_date=last_dates[i]
        )
        db.session.add(new_experience)
    
    db.session.commit()
    flash('Experiences saved successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/delete_experience/<int:experience_id>', methods=['POST'])
def delete_experience(experience_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    experience = Experience.query.get_or_404(experience_id)
    if experience.employee_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(experience)
    db.session.commit()
    return jsonify({'success': 'Experience deleted successfully'}), 200

