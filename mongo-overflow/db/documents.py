from mongoengine import * #tsk tsk...what would PEP say?!
from datetime import datetime


class User(Document):
    name = StringField(required = True)
    username = StringField(required = True)
    email = StringField(required = True)
    openid = StringField(required = True)
    avatar = URLField()
    rep = IntField(required = True, default = 0)
    joined = DateTimeField()
    last_login = DateTimeField()

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

    def __cmp__(self, other):
        return cmp(self.score, other.score)

    def vote_up(self, user):
        try:
            your_vote = AnswerVote.objects.get(answer = self, user = user)
            if your_vote.score == -1:
                your_vote.score = 1
                your_vote.save()
                Answer.objects(id=self.id).update_one(inc__score=2)
                User.objects(id = self.author.id).update_one(inc__rep=20)
            elif your_vote.score == 1:
                your_vote.delete()
                Answer.objects(id=self.id).update_one(dec__score=1)
                User.objects(id = self.author.id).update_one(dec__rep=10)
                return 0
        except:
            vote = AnswerVote(answer = self, user = user, score = 1)
            vote.save()
            Answer.objects(id=self.id).update_one(inc__score=1)
            User.objects(id = self.author.id).update_one(inc__rep=10)
        return 1


    def vote_down(self, user):
        try:
            your_vote = AnswerVote.objects.get(answer = self, user = user)
            if your_vote.score == 1:
                your_vote.score = -1
                your_vote.save()
                Answer.objects(id=self.id).update_one(dec__score=2)
                User.objects(id = self.author.id).update_one(dec__rep=20)
            elif your_vote.score == -1:
                your_vote.delete()
                Answer.objects(id=self.id).update_one(inc__score=1)
                User.objects(id = self.author.id).update_one(inc__rep=10)
                return 0
        except:
            vote = AnswerVote(answer = self, user = user, score = -1)
            vote.save()
            Answer.objects(id=self.id).update_one(dec__score=1)
            User.objects(id = self.author.id).update_one(dec__rep=10)
        return -1

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

    def vote_up(self, user):
        try:
            your_vote = Vote.objects.get(question = self, user = user)
            if your_vote.score == -1:
                your_vote.score = 1
                your_vote.save()
                Question.objects(id=self.id).update_one(inc__score=2)
                User.objects(id = self.author.id).update_one(inc__rep=20)
            elif your_vote.score == 1:
                your_vote.delete()
                Question.objects(id=self.id).update_one(dec__score=1)
                User.objects(id = self.author.id).update_one(dec__rep=10)
                return 0
        except:
            vote = Vote(question = self, user = user, score = 1)
            vote.save()
            Question.objects(id=self.id).update_one(inc__score=1)
            User.objects(id = self.author.id).update_one(inc__rep=10)
        return 1


    def vote_down(self, user):
        try:
            your_vote = Vote.objects.get(question = self, user = user)
            if your_vote.score == 1:
                your_vote.score = -1
                your_vote.save()
                Question.objects(id=self.id).update_one(dec__score=2)
                User.objects(id = self.author.id).update_one(dec__rep=20)
            elif your_vote.score == -1:
                your_vote.delete()
                Question.objects(id=self.id).update_one(inc__score=1)
                User.objects(id = self.author.id).update_one(inc__rep=10)
                return 0
        except:
            vote = Vote(question = self, user = user, score = -1)
            vote.save()
            Question.objects(id=self.id).update_one(dec__score=1)
            User.objects(id = self.author.id).update_one(dec__rep=10)
        return -1


class Vote(Document):
    user = ReferenceField(User, required = True)
    score = IntField(required = True, default = 0)
    question = ReferenceField(Question, required = True)

class AnswerVote(Document):
    user = ReferenceField(User, required = True)
    score = IntField(required = True, default = 0)
    answer = ReferenceField(Answer, required = True)

