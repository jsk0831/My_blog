from django import forms
from .models import Post, Comment, User

class PostForm( forms.Form ):
	title = forms.CharField(
		max_length = 100,
		label = '제목',
		widget = forms.TextInput( attrs = {
			'placeholder': '제목을 입력하세요.'
		} )
	)

	content = forms.CharField(
		label = '내용',
		widget = forms.TextInput( attrs = {
			'placeholder': '내용을 입력하세요.'
		} )
	)

	def get_data( self ):
		# form 데이터에 문제가 없으면
		if self.is_valid():
			title = self.cleaned_data[ 'title' ]
			content = self.cleaned_data[ 'content' ]
			data = { 'title': title, 'content': content }
			return data


class CommentForm( forms.Form ):
	content = forms.CharField(
		max_length = 5000,
		label = '내용',
		widget = forms.TextInput( attrs = {
			'placeholder': '댓글을 입력하세요.'
		} )
	)

	name = forms.CharField(
		max_length = 20,
		label = '작성자 ID',
		widget = forms.TextInput( attrs = {
			'placeholder': '아이디를 입력하세요.'
		} )
	)

	pw = forms.CharField(
		max_length = 20,
		label = '작성자 PW',
		widget = forms.PasswordInput( attrs = {
			'placeholder': '비밀번호를 입력하세요.'
		} )
	)

	def get_data( self ):
		# form 데이터에 문제가 없으면
		if self.is_valid():
			content = self.cleaned_data[ 'content' ]
			name = self.cleaned_data[ 'name' ]
			pw = self.cleaned_data[ 'pw' ]
			data = { 'content': content, 'name': name, 'pw': pw }
			return data