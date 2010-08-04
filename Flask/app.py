from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/questions/')
def index():
    return "questions/index"

@app.route('/questions/<id>')
def question_details(id):
    return "question details"

@app.route('/questions/ask')
def ask_question():
    return "ask"

@app.route('/questions/unanswered')
def unanswered_questions():
    return "unanswered"

@app.route('/users/')
def user_list():
    return "all users"

@app.route('/users/<id>')
def user_details(id):
    return "user details"

@app.route('/posts/<id>/vote/<int:value>')
def vote(id, value):
    return "vote"

@app.route('/login')
def login():
    return "login"

@app.route('/logout')
def logout():
    return "logout"

if __name__ == '__main__':
    app.run()
