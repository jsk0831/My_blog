from django.shortcuts import render, redirect
from .models import Post, Comment, User, Address
from .forms import CommentForm, PostForm
from django.views import generic
from django.contrib import messages


class Home( generic.ListView ):
	template_name = "blog/home.html"
	context_object_name = "latest_post"
	def get_queryset(self):
		return Post.objects.order_by("-pub_date")[:10]


class Detail( generic.DetailView ):
	def get_ip( self, request ):
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]
		else:
			ip = request.META.get('REMOTE_ADDR')
		return ip

	def check_visited( self, request, pk ):
		ip = self.get_ip( request )
		# ip 체크
		try:
			address = Address.objects.get( post_id = pk, ip = ip )
			return False
		except:
			address = Address.objects.create( post_id = pk, ip = ip )
			return True

	def add_comment( self, request, pk ):
		# form을 통해 받은 POST를 이곳에 저장
		form = CommentForm( request.POST )
		# POST가 유효한지 확인 후 저장
		data = form.get_data()

		try:
			user = User.objects.get( name = data[ 'name' ] )
			# 입력한 pw가 일치하면
			if user.pw == data[ 'pw' ]:
				messages.info( request, "로그인 성공!  댓글이 작성되었습니다." )
				# 댓글 추가
				comment = Comment.objects.create( content = data['content'], post_id = pk, user_id = user.id )
				# Post의 댓글 수 추가
				comment.post.update_comments( len( Comment.objects.filter( post_id = pk ) ) )
				comment.post.save()

			else:
				messages.info( request, "로그인 실패!  댓글을 작성하지 못했습니다." )

		# user 정보가 없으면, 새로 생성
		except:
			address = Address.objects.get( ip = self.get_ip(request) )
			user = User( name = data[ 'name' ], pw = data[ 'pw' ], address_id = address.id )
			user.save()
			messages.info( request, "새로운 계정으로 댓글이 작성되었습니다." )

			# 댓글 추가
			comment = Comment.objects.create( content = data['content'], post_id = pk, user_id = user.id )
			# Post의 댓글 수 추가
			comment.post.update_comments( len( Comment.objects.filter( post_id = post.id ) ) )
			comment.post.save()


	def post( self, request, pk ):
		# 로그인 정보가 유효하면 댓글 추가
		self.add_comment( request, pk )
		return redirect( 'blog:detail', pk )

	def get( self, request, pk ):
		post = Post.objects.get( pk = pk )
		comments = post.comment_set.all()
		form = CommentForm()

		# 기존에 방문하지 않았으면 조회수 상승
		if self.check_visited( request, pk ):
			post.views += 1
			post.save()
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