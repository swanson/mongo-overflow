from wtforms import Form, TextField, TextAreaField, validators

class QuestionForm(Form):
    title = TextField("What's your question?", [validators.Required()])
    body = TextAreaField("Body", [validators.Required()])
    tags = TextField("Tags")

class AnswerForm(Form):
    answer_body = TextAreaField("Your Answer", [validators.Required()])

class CommentForm(Form):
    comment_body = TextAreaField(" ", [validators.Required()])
