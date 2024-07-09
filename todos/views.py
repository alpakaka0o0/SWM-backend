# todos/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from todos.models import Todo
from accounts.models import User
from todos.serializers import TodoSerializer
import re

class TodoView(APIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def post(self, request):
        '''
        - 이 함수는 todo를 생성하는 함수입니다.
        - deadline 은 항상 start_date 와 같은 날이거나 그 이후여야합니다
        - category는 #으로 시작하며 뒤에는 6자여야 합니다.
        - content는 1자 이상 50자 이하여야합니다.
        - user_id 는 user 테이블에 존재해야합니다.
        '''
        data = request.data

        # deadline >= startdate
        if 'start_date' in data and 'deadline' in data:
            if data['deadline'] <= data['start_date']:
                return Response({"error": "deadline must be on or after start_date."}, status=status.HTTP_400_BAD_REQUEST)
        
        # category = 6자리 hex 색상코드 형식
        if 'category' in data:
            if not re.match(r'^#[0-9A-Fa-f]{6}$', data['category']):
                return Response({"error": "category must be a valid hex color code."}, status=status.HTTP_400_BAD_REQUEST)

        # content = 1자 이상 50자 이하
        if 'content' in data:
            if not (1 <= len(data['content']) <= 50):
                return Response({"error": "content must be between 1 and 50 characters."}, status=status.HTTP_400_BAD_REQUEST)
        # user_id = user 테이블에 존재
        if 'user_id' in data:
            if not User.objects.filter(id=data['user_id']).exists():
                return Response({"error": "user_id does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = TodoSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({"id": serializer.instance.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        '''
        - 이 함수는 todo list를 불러오는 함수입니다.
        - 입력으로 받는 것은 user_id 와 start_date, end_date 입니다.
        - start_date와 end_date가 없는 경우 user_id에 해당하는 모든 todo를 불러옵니다.
        - start_date와 end_date가 있는 경우 user_id에 해당하는 todo 중 start_date와 end_date 사이에 있는 todo를 불러옵니다.
        '''
        user_id = request.GET.get('user_id')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        if start_date and end_date:
            todos = Todo.objects.filter(deleted_at__isnull=True, user_id=user_id, start_date__gte=start_date, deadline__lte=end_date)
        else:
            todos = Todo.objects.filter(deleted_at__isnull=True, user_id=user_id)

        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        '''
        - 이 함수는 todo를 수정하는 함수입니다.
        - deadline 은 항상 start_date 와 같은 날이거나 그 이후여야합니다
        - 
        '''



    def delete(self, request):
        '''
        - 이 함수는 todo를 삭제하는 함수입니다.
        - 
        '''