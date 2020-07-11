from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from datetime import datetime

class Comment:
    def __init__(self,email,content,created = None):
        self.email = email
        self.content = content
        self.created= datetime.now()

    def __str__(self):
        return f'{self.email} made a comment.'

class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

obje = Comment('zoo@mail.com','Nice to see you again')
print("got an obj ",obj)
obj = CommentSerializer(obje)
print("after serial",obj.data)
fin = JSONRenderer().render(obj.data)
print("puur beauty",fin)


# print("context",obj.is_valid())

