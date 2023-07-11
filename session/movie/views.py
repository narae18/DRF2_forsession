from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Movie,Comment, Tag
from .serializers import MovieSerializer, CommentSerializer

from django.shortcuts import get_object_or_404


# Create your views here.

@api_view(['GET','POST'])
def movie_list_create(request):
    
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(data=serializer.data)
    
    if request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()  #여기서 세이브 해주지않으면 객체 아이디가 부여되지않아서 뒤에서 가져올수업슴
            
            content = request.data['content']
            words = content.split(' ')
            tag_list = []
            for w in words :
                if w[0] == '#':
                    tag_list.append(w[1:])
            for t in tag_list:
                try:
                    tag = get_object_or_404(Tag, name=t)
                except:
                    tag = Tag(name=t)
                    tag.save()
                    
                movie = get_object_or_404(Movie, id=serializer.data['id'])#앞에서 세이브했기때문에 부여된아이디값을 여기서 쓰기때무네
                movie.tag.add(tag)
            movie.save() 
                
        return Response(data=MovieSerializer(movie).data)
        


@api_view(['GET','PATCH', 'DELETE'])
def movie_detail_update_delete(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = MovieSerializer(instance=movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            movie = get_object_or_404(Movie, id=serializer.data['id'])
            movie.tag.clear()
            #왜와이? : 수정할때 태그를 싹~지우고 다시 추가해줘야되기때문에/
            content = request.data['content']
            words = content.split(' ')
            tag_list = []
            for w in words :
                if w[0] == '#':
                    tag_list.append(w[1:])
            for t in tag_list:
                try:
                    tag = get_object_or_404(Tag, name=t)
                except:
                    tag = Tag(name=t)
                    tag.save()
                    
                movie = get_object_or_404(Movie, id=serializer.data['id'])#앞에서 세이브했기때문에 부여된아이디값을 여기서 쓰기때무네
                movie.tag.add(tag)
            movie.save() 
        
        return Response(data=MovieSerializer(movie).data)
        

    
    elif request.method =='DELETE':
        movie.delete()
        data = {
            'deleted_movie': movie_id
        }
        return Response(data)


@api_view(['GET','POST'])
def comment_read_create(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    if request.method == 'GET':
        comments = Comment.objects.filter(movie=movie)
        serializer = CommentSerializer(comments, many=True)
        return Response(data=serializer.data)
    
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(movie=movie)
        return Response(serializer.data)
    
    
@api_view(['GET'])
def find_tag(request, tag_name):
    f_tag = get_object_or_404(Tag, name=tag_name)
    if request.method == 'GET':
        movie = Movie.objects.filter(tag__in = [f_tag])  
        serializer = MovieSerializer(movie, many=True)
        return Response(data=serializer.data)