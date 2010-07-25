from mongoengine import * #tsk tsk...what would PEP say?!
from datetime import datetime
#from uuid import uuid4
from django import forms

class User(Document):
    #oid = StringField(default = uuid4)
    name = StringField(required = True)
    email = StringField()
    avatar = URLField()
    rep = IntField(required = True, default = 0)

class Response(Document):
    #oid = StringField(required = True, default = uuid4)
    body = StringField(required = True)
    score = IntField(required = True, default = 0)
    created = DateTimeField(required = True, default = lambda : datetime.now())
    author = ReferenceField(User)

class Comment(Response):
    class Form(forms.Form):
        comment_body = forms.CharField(label = '')

class Answer(Response):
    comments = ListField(ReferenceField(Comment))

    class Form(forms.Form):
        body = forms.CharField(widget = forms.Textarea, label = '')

class Question(Document):
    #oid = StringField(required = True, default = uuid4)
    title = StringField(required = True)
    body = StringField(required = True)
    score = IntField(required = True, default = 0)
    created = DateTimeField(required = True, default = lambda : datetime.now())
    views = IntField(required = True, default = 0)
    comments = ListField(ReferenceField(Comment), default = lambda : [])
    answers = ListField(ReferenceField(Answer), default = lambda : [])
    tags = ListField(StringField(max_length = 50, default = lambda : []))
    author = ReferenceField(User)

    class Form(forms.Form):
        title = forms.CharField()
        body = forms.CharField(widget=forms.Textarea)
        tags = forms.CharField(required = False)

        def clean(self):
            cleaned_data = self.cleaned_data
            s_title = cleaned_data.get("title")
            s_body = cleaned_data.get("body")
            if not s_title:
                msg = "You must enter a title for your question."
                self._errors["title"] = self.error_class([msg])
            if not s_body:
                msg = "You must enter a body for your question."
                self._errors["body"] = self.error_class([msg])
            return cleaned_data

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
                tags = ['mongodb', 'python'], author = matt, created = datetime.now())

    a = Answer(body = 'It\'s awesome, for realz', author = jon_f)
    a.save()
    c = Comment(body = 'Possible dup', author = jon_f)
    c.save()

    q.answers.append(a)
    q.comments.append(c)
    q.save()

    q2 = Question(title = 'Another Question', body = 'Why is Python so cool?', \
                tags = ['django', 'python'], author = jon_f, created = datetime.now())
    q2.save()

    my_question = Question.objects()[0]
    
    print my_question.author.name 
    #matt
    print my_question.tags
    #[u'mongodb', u'python']
    print my_question.answers[0].body
    #It's awesome, for realz
