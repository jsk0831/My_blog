from django.shortcuts import render, redirect
from .models import Post, Comment, User
from .forms import CommentForm
from django.views import generic


class Home( generic.ListView ):
	template_name = "blog/home.html"
	context_object_name = "latest_post"
	def get_queryset(self):
		return Post.objects.order_by("-pub_date")[:10]


class Detail( generic.DetailView ):
	def post( self, request, pk ):
		post = Post.objects.get( pk = pk )
		comments = post.comment_set.all()

		# form을 통해 받은 POST를 이곳에 저장
		form = CommentForm( request.POST )
		data = form.get_data()

		# user 정보 확인
		try:
			user = User.objects.get( name = data[ 'name' ] )
			# 입력한 pw가 일치하면
			if user.pw == data[ 'pw' ]:
				Comment.objects.create( content = data[ 'content' ], post_id = pk, user_id = user.id )
				# Post의 댓글 수 추가
				post.update_comments( len( Comment.objects.all() ) )
			# pw가 일치하지 않으면
			else:
				return redirect( 'blog:detail', pk )

		# user 정보 생성
		except:
			user = User( name = data[ 'name' ], pw = data[ 'pw' ] )
			user.save()
			# model에 댓글 추가
			Comment.objects.create( content = data[ 'content' ], post_id = pk, user_id = user.id )
			# Post의 댓글 수 추가
			post.update_comments( len( Comment.objects.all() ) )

		return redirect( 'blog:detail', pk )

	def get( self, request, pk ):
		post = Post.objects.get( pk = pk )
		comments = post.comment_set.all()
		form = CommentForm()
		return render( request, 'blog/detail.html', { 'post': post, 'comments': comments, 'form': form } )