from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly
from question.models import Question, Answer
from rest_framework.exceptions import ValidationError
from .serializers import QuestionSerializer, AnswerSerializer
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by("-created_at")
    serializer_class = QuestionSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    lookup_field = "slug"
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        

class AnswerCreateAPIView(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        request_user = self.request.user 
        kwarg_slug = self.kwargs.get('slug')
        question = get_object_or_404(Question, slug=kwarg_slug)
        if question.answers.filter(author=request_user).exists():
            raise ValidationError("You have already answered this Question!")
        serializer.save(author=request_user, question=question)
        
        
class AnswerRetreiveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    lookup_field = 'uuid'
   

class AnsewrListAPIView(generics.ListAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        return Answer.objects.filter(question__slug=kwarg_slug).order_by('-created_at')
    
    
class AnswerLikeAPIView(APIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, uuid):
        answer = get_object_or_404(Answer, uuid=uuid)
        answer.voters.add(request.user)
        answer.save()
        serializer = self.serializer_class(answer, context = {'request': request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, uuid):
        answer = get_object_or_404(Answer, uuid=uuid)
        answer.voters.remove(request.user)
        answer.save()
        serializer = self.serializer_class(answer, context = {'request': request})
        
        
        return Response(serializer.data, status=status.HTTP_200_OK)
       
    
    
    
    

    
    