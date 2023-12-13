from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from models import db, User
from Form import CreateUserForm
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
# from chatbot import chatbot
from flask_login import current_user, login_required
from flask_socketio import SocketIO, emit, join_room, send



app = Flask(__name__)

app.static_folder = 'static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'  # Replace with your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mockingjay_2918'
db.init_app(app)

socketio = SocketIO(app)
rooms = {}

uri = 'mongodb+srv://nicholaspoh05:Borderlands2232!!@Cluster0.8cesyej.mongodb.net/Cluster0?retryWrites=true&w=majority'
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['Cluster0']  # Replace 'Cluster0' with your actual database name
courses_collection = db['courses']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')
##------------------ NICHOLAS --------------------

@app.route('/createc', methods=['GET', 'POST'])
def createc():
    if request.method == 'POST':
        # Retrieve form data
        title = request.form['title']
        description = request.form['description']
        objectives = request.form['objectives']
        prerequisite = request.form['prerequisite']
        learners = request.form['learners']

        # Save the data to MongoDB
        course_data = {
            'title': title,
            'description': description,
            'objectives': objectives,
            'prerequisite': prerequisite,
            'learners': learners
        }
        courses_collection.insert_one(course_data)

        # Redirect to the 'courses.html' page with the form data
        return redirect(url_for('courses'))

    # Render the 'createc.html' page for GET requests
    return render_template('createc.html')

@app.route('/courses')
def courses():
    # Retrieve all courses from MongoDB
    all_courses = courses_collection.find()

    # Render the 'courses.html' page with the retrieved courses
    return render_template('courses.html', courses=all_courses)

##------------------------------------------------
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot.get_response(userText))

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST':
        user = User(
            first_name=create_user_form.first_name.data,
            last_name=create_user_form.last_name.data,
            username=create_user_form.username.data,
            email=create_user_form.email.data,
            date_of_birth=create_user_form.date_of_birth.data,
            password=create_user_form.password.data,
            confirm_password=create_user_form.confirm_password.data
        )

        db.session.add(user)
        db.session.commit()
        # Test code to print the newly added user details
        print(user.first_name, user.last_name, "was stored in the database successfully with user_id =", user.id)
        return redirect(url_for('login'))  # Redirect to success page after sign-up

    return render_template('sign_up.html', form=create_user_form)


@app.route('/retrieve_profile')
def retrieve_profile():
    # 'users' is all, 'user' is single
    users = User.query.all()
    print(users)
    return render_template('retrieve_profile.html', users=users)


@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


# ================= CHATROOM =======================
@app.route('/chatroom')
def chatroom():
    users = User.query.all()
    return render_template('chatroom.html', users=users)

@socketio.on('message')
def handle_message(data):
    user_id = request.sid
    room = user_id  # Use user_id as the room
    name = user_id

    if room not in rooms:
        rooms[room] = {'members': 1, 'messages': []}  # Initialize the room if it doesn't exist
    else:
        rooms[room]['members'] += 1  # Increment member count if the room already exists

    content = {'name': name, 'message': data['data']}
    send(content, to=room)
    rooms[room]['messages'].append(content)

@socketio.on('connect')
def handle_connect():
    user_id = request.sid
    room = user_id  # Use user_id as the room
    name = user_id

    if room not in rooms:
        rooms[room] = {'members': 1, 'messages': []}  # Initialize the room if it doesn't exist
    else:
        rooms[room]['members'] += 1  # Increment member count if the room already exists

    join_room(room)
    send({'name': name, 'message': 'has entered the room'}, to=room)
    rooms[room]['members'] += 1
















