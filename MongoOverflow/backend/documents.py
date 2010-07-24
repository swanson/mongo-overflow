from mongoengine import * #tsk tsk...what would PEP say?!
from datetime import datetime

class User(Document):
    name = StringField(required = True)
    email = StringField()
    avatar = URLField()
    rep = IntField(required = True, default = 0)

class Response(Document):
    body = StringField(required = True)
    score = IntField(required = True, default = 0)
    created = DateTimeField(required = True, default = datetime.now)
    author = ReferenceField(User)

class Comment(Response):
    pass

class Answer(Response):
    comments = ListField(ReferenceField(Comment))

class Question(Document):
    title = StringField(required = True)
    body = StringField(required = True)
    score = IntField(required = True, default = 0)
    created = DateTimeField(required = True, default = datetime.now)
    views = IntField(required = True, default = 0)
    comments = ListField(ReferenceField(Comment), default = lambda : [])
    answers = ListField(ReferenceField(Answer), default = lambda : [])
    tags = ListField(StringField(max_length = 50))
    author = ReferenceField(User)

if __name__ == '__main__':
    connect('testing') #make sure mongod is running 
    User.drop_collection()
    Question.drop_collection()
    Answer.drop_collection()

    matt = User(name = 'matt', email = 'matt@mail.com')
    matt.save()
    jon_f = User(name = 'Jon F', email = 'jonf@mail.com')
    jon_f.save()

    q = Question(title = 'Is mongoDB cool?', body = 'It seems neat. Is it?', \
                tags = ['mongodb', 'python'], author = matt)

    a = Answer(body = 'It\'s awesome, for realz', author = jon_f)
    a.save()

    q.answers.append(a)
    q.save()

    q2 = Question(title = 'Another Question', body = 'It seems neat. Is it?', \
                tags = ['django', 'python'], author = jon_f)
    q2.save()

    my_question = Question.objects()[0]
    
    print my_question.author.name 
    #matt
    print my_question.tags
    #[u'mongodb', u'python']
    print my_question.answers[0].body
    #It's awesome, for realz
