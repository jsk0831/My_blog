from django.shortcuts import render, redirect
from .models import Post, Comment, User
from .forms import CommentForm, PostForm
from django.views import generic
from django.contrib import messages


class Home( generic.ListView ):
	template_name = "blog/home.html"
	context_object_name = "latest_post"
	def get_queryset(self):
		return Post.objects.order_by("-pub_date")[:10]


class Detail( generic.DetailView ):
	def post( self, request, pk ):
		# 블로그 게시물
		post = Post.objects.get( pk = pk )
		# form을 통해 받은 POST를 이곳에 저장
		form = CommentForm( request.POST )
		data = form.get_data()

		try:
			user = User.objects.get( name = data[ 'name' ] )
			# 입력한 pw가 일치하면
			if user.pw == data[ 'pw' ]:
				messages.info( request, "로그인 성공!  댓글이 작성되었습니다." )
			else:
				messages.info( request, "로그인 실패!  댓글을 작성하지 못했습니다." )

		# user 정보가 없으면, 새로 생성
		except:
			user = User( name = data[ 'name' ], pw = data[ 'pw' ] )
			user.save()
			messages.info( request, "새로운 계정으로 댓글이 작성되었습니다." )

		# 댓글 추가
		Comment.add_comment( content = data[ 'content' ], post = post, user_id = user.id )
		return redirect( 'blog:detail', pk )

	def get( self, request, pk ):
		post = Post.objects.get( pk = pk )
		comments = post.comment_set.all()
		form = CommentForm()
		return render( request, 'blog/detail.html', { 'post': post, 'comments': comments, 'form': form } )


class Publish( generic.DetailView ):
	def post( self, request ):
		form = PostForm( request.POST )
		data = form.get_data()
		post = Post( title = data[ 'title' ], content = data[ 'content' ] )
		post.save()
		return redirect( 'blog:detail', post.id )

	def get( self, request ):
		form = PostForm()
		return render( request, 'blog/publish.html', {'form': form} )