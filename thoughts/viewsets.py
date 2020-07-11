from .models import Thought
from django.contrib.auth.models import User
# rest-framework
from .serializers import ThoughtSerializer,UserSerializer
from rest_framework import viewsets

from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer 

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
   


class ThoughtViewSet(viewsets.ModelViewSet):
    # queryset = Thought.objects.all()
    serializer_class = ThoughtSerializer

    def get_queryset(self):
        print("where am I?")
        return self.request.user.thoughts.all()

    #  def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)    

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     # print("serializer",serializer)
    #     if serializer.is_valid:
    #         print("serial is valid")
    #         print("data in serial",serializer.initial_data)
    #     else:
    #         print("smth wrong with that serializer")    
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     print("seria data final",serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)    

    # def create(self,request,*args,**kwargs):
    #     return Response({'status': 'AND?'})

        # pass
    #     data = self.request.data
    #     notes = data['notes']
    #     score = data['score']
    #     user = self.request.user
    #     thought = Thought.objects.create(score=score,notes=notes,user=user)      
    #     print("thought",thought)
    #     thought.save()
    #     return Response({'status': 'thougth created'})

