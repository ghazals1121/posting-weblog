from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import login, logout
from rest_framework import views, permissions, authentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from django.shortcuts import render

# Create your views here.
from panel.models import Post, Comment, Reply
from panel.serializers import LoginSerializer, RegisterSerializer


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get(self, request):
        serializer = LoginSerializer()
        return render(request, template_name='login.html', context={'form': serializer}, status=200)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            # user.backend = settings.AUTHENTICATION_BACKENDS[0]
            login(request, user)

            return Response({'message': 'Login Successful'}, status=200)

        except ValidationError as e:
            return Response({'message': e.detail.get('non_field_errors')[0]})


class RegisterView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'message': 'Bad Credentials'}, status=400)
        user = serializer.create(serializer.validated_data)
        # user.backend = settings.AUTHENTICATION_BACKENDS[0]
        login(self.request, user)
        return Response({'message': 'Registered Successfully'}, status=200)


@api_view(['GET'])
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return Response("logout successfully", status=200)


@api_view(['POST'])
@login_required()
@authentication_classes([CsrfExemptSessionAuthentication])
def create_post(request):
    author = request.user
    post_id = Post.objects.count() + 1
    new_post = Post.objects.create(post_id=post_id, author=author)
    if 'title' in request.data.keys():
        new_post.title = request.data['title']
    if 'content' in request.data.keys():
        new_post.content = request.data['content']
    if 'category' in request.data.keys():
        new_post.category = request.data['category']
    new_post.save()
    return Response('post created', status=200)


@api_view(['POST'])
@login_required()
@authentication_classes([CsrfExemptSessionAuthentication])
def edit_post(request):
    author = request.user
    if 'post_id' not in request.data.keys():
        return JsonResponse({
            'message': 'no post specified'}, status=400)
    post_id = request.data['post_id']
    try:
        post = Post.objects.get(post_id=post_id)
        if post.author == author:
            if 'title' in request.data.keys():
                post.title = request.data['title']
            if 'content' in request.data.keys():
                post.content = request.data['content']
            if 'category' in request.data.keys():
                post.category = request.data['category']
            post.save()
            return Response("post updated", status=200)
        else:
            return Response("you are not the author of post", status=400)
    except Post.DoesNotExist:
        return Response("no such post", status=400)


@api_view(['POST'])
@login_required()
@authentication_classes([CsrfExemptSessionAuthentication])
def delete_post(request):
    author = request.user
    if 'post_id' not in request.data.keys():
        return JsonResponse({
            'message': 'no post specified'}, status=400)
    post_id = request.data['post_id']
    try:
        post = Post.objects.get(post_id=post_id)
        if post:
            if post.author == author:
                post.delete()
            else:
                return Response("you are not the author of post", status=400)
    except Post.DoesNotExist:
        return Response("no such post", status=400)


@api_view(['POST'])
@login_required()
@authentication_classes([CsrfExemptSessionAuthentication])
def post_comment(request):
    comment_id = Comment.objects.count() + 1
    author = request.user
    if 'post_id' not in request.data.keys():
        return JsonResponse({
            'message': 'no post specified'}, status=400)
    if 'text' not in request.data.keys():
        return JsonResponse({
            'message': 'no text for comment'}, status=400)
    post_id = request.data['post_id']
    text = request.data['text']
    try:
        post = Post.objects.get(post_id=post_id)
        new_comment = Comment.objects.create(comment_id=comment_id, author=author, post=post, text=text)
        return Response('comment created', status=200)
    except Post.DoesNotExist:
        return Response("no such post", status=400)


@api_view(['POST'])
@login_required()
@authentication_classes([CsrfExemptSessionAuthentication])
def post_reply(request):
    reply_id = Reply.objects.count() + 1
    author = request.user
    if 'comment_id' not in request.data.keys():
        return JsonResponse({
            'message': 'no comment specified'}, status=400)
    if 'text' not in request.data.keys():
        return JsonResponse({
            'message': 'no text for reply'}, status=400)
    comment_id = request.data['comment_id']
    text = request.data['text']
    try:
        comment = Comment.objects.get(comment_id=comment_id)
        new_reply = Reply.objects.create(reply_id=reply_id, author=author, text=text, comment=comment)
        return Response('reply created', status=200)
    except Comment.DoesNotExist:
        return Response("no such comment", status=400)


@api_view(['POST'])
@login_required()
@authentication_classes([CsrfExemptSessionAuthentication])
def post_like(request):
    liker = request.user
    if 'post_id' not in request.data.keys():
        return JsonResponse({
            'message': 'no post specified'}, status=400)
    post_id = request.data['post_id']
    try:
        post = Post.objects.get(post_id=post_id)
        post.likes = post.likes + 1
        post.users_liked.add(liker)
        post.save()
        return Response("post liked", status=200)
    except Post.DoesNotExist:
        return Response("no such post", status=400)


@api_view(['POST'])
@login_required()
@authentication_classes([CsrfExemptSessionAuthentication])
def comment_like(request):
    liker = request.user
    if 'comment_id' not in request.data.keys():
        return JsonResponse({
            'message': 'no comment specified'}, status=400)
    comment_id = request.data['comment_id']
    try:
        comment = Comment.objects.get(comment_id=comment_id)
        comment.likes = comment.likes + 1
        comment.users_liked.add(liker)
        comment.save()
        return Response("comment liked", status=200)
    except Comment.DoesNotExist:
        return Response("no such comment", status=400)


@api_view(['POST'])
@login_required()
@authentication_classes([CsrfExemptSessionAuthentication])
def post_dislike(request):
    disliker = request.user
    if 'post_id' not in request.data.keys():
        return JsonResponse({
            'message': 'no post specified'}, status=400)
    post_id = request.data['post_id']
    post = Post.objects.get(post_id=post_id)
    if post:
        post.dislikes = post.dislikes + 1
        post.users_disliked.add(disliker)
        post.save()
        return Response("post disliked", status=200)
    else:
        return Response("no such post", status=400)


@api_view(['POST'])
@login_required()
@authentication_classes([CsrfExemptSessionAuthentication])
def comment_dislike(request):
    disliker = request.user
    if 'comment_id' not in request.data.keys():
        return JsonResponse({
            'message': 'no comment specified'}, status=400)
    comment_id = request.data['comment_id']
    try:
        comment = Comment.objects.get(comment_id=comment_id)
        comment.dislikes = comment.dislikes + 1
        comment.users_disliked.add(disliker)
        comment.save()
        return Response("comment disliked", status=200)
    except Comment.DoesNotExist:
        return Response("no such comment", status=400)
