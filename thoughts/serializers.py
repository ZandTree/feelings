from rest_framework import serializers as ser
from .models import Thought
from django.contrib.auth.models import User


class UserSerializer(ser.HyperlinkedModelSerializer):
    password = ser.HiddenField(default="") # исчезнет с глаз
    thoughts = ser.HyperlinkedRelatedField(
        many =True,
        read_only=True,
        view_name="thought-detail"
    )
    
    class Meta:
        """
        why write_only? он не пойдёт обратно, чтобы его потом все видели
        т.е. только написал ->  отправил
        """
        
        model = User      
        # extra_kwargs = {'email':{'write_only':True}}
        fields = ('username','email','date_joined','last_login','last_name','first_name','password','thoughts')
        read_only_fields = ['date_joind','last_login']

    

    def create(self, validated_data):
        print('inside create serializers')
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user    

    def update(self, instance,validated_data):
        try:
            del validated_data['username']
        except KeyError:
            pass    
        return super().update(instance,validated_data)
       

class ThoughtSerializer(ser.HyperlinkedModelSerializer):
    # toDo: add extra attr just for vue.js to toggle show object
    # ex:displayMore=False
    user = ser.HiddenField(default=ser.CurrentUserDefault())
    score_display = ser.SerializerMethodField()

    class Meta:
        model = Thought
        fields = ['id','url','user','score','notes','recorded_at','score_display']
        read_only_fields = ('recorded_at',)

    def get_score_display(self,obj):
        """ like in model: get_attr_dispaly"""
        return obj.get_score_display()    
        

    # def create(self, validated_data):
    #     print("inside create")
    #     thought = Thought(
    #         score=validated_data['score'],
    #         notes=validated_data['notes']
    #     )
    #     thought.user = self.context['request'].user
    #     thought.save()
    #     print("thought",thought)
    #     return super().create(validated_data)      
         
    

    

    # def create(self, validated_data):
    #     print("WHERE IS MY CREATE IN SERIALIZERS?????")
    #     # import pdb
    #     # print("pdb imported")
    #     # pdb.set_trace()
    #     data = validated_data
    #     print("found validated data",validated_data)
    #     thought = Thought.objects.get_or-create(
    #         score=validated_data['score'],
    #         notes=validated_data['notes']
    #     )
    #     thought.user = self._user(obj) #(self.context.request['user'])
    #     thought.save()
    #     return thought              

            


     

    
    

   


    

