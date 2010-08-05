from mongoengine import * #tsk tsk...what would PEP say?!
from datetime import datetime
from wtforms import Form, TextField, TextAreaField, validators

class User(Document):
    name = StringField(required = True)
    username = StringField(required = True)
    email = StringField(required = True)
    openid = StringField(required = True)
    avatar = URLField()
    rep = IntField(required = True, default = 0)

class Response(Document):
    body = StringField(required = True)
    score = IntField(required = True, default = 0)
    created = DateTimeField(required = True, default = lambda : datetime.now())
    author = ReferenceField(User)
    voters = ListField(ReferenceField(User), default = lambda : [])

class Comment(Response):
    pass

class Answer(Response):
    comments = ListField(ReferenceField(Comment), default = lambda : [])

class Question(Document):
    title = StringField(required = True)
    body = StringField(required = True)
    score = IntField(required = True, default = 0)
    created = DateTimeField(required = True, default = lambda : datetime.now())
    views = IntField(required = True, default = 0)
    comments = ListField(ReferenceField(Comment), default = lambda : [])
    answers = ListField(ReferenceField(Answer), default = lambda : [])
    tags = ListField(StringField(max_length = 50, default = lambda : []))
    author = ReferenceField(User)

class QuestionInputForm(Form):
    title = TextField("What's your question?", [validators.Required()])
    body = TextAreaField("Body", [validators.Required()])
    tags = TextField("Tags")

class AnswerInputForm(Form):
    answer_body = TextAreaField("Your Answer", [validators.Required()])

class Vote(Document):
    user = ReferenceField(User, required = True)
    score = IntField(required = True, default = 0)
    question = ReferenceField(Question, required = True)
