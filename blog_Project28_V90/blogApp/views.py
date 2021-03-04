from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render,get_object_or_404
from blogApp.models import Post
from django.views.generic import ListView, DetailView
from blogApp.forms import EmailSendForm,CommentForm

class PostListView(ListView):
    model = Post
    paginate_by = 3
    template_name = 'post_list.html'

#class PostDetailView(DetailView):
#    model = Post
 #   template_name = 'blog/post_detail.html'
def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug_field=post,
                                status='published',
                                publish__year=year,
                                publish__month=month,
                                publish__day=day)
    #post_tags_ids=post.tags.values_list('id',flat=True)
    #similar_posts=Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    #similar_posts=similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','publish')[:4]

    comments=post.comments.filter(active=True)
    new_comment=None
    if request.method=='POST':
        form=CommentForm(data=request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
          #  csubmit=True
    else:
        form=CommentForm()
    return render(request, 'post_detail.html', {'post':post, 'form':form, 'comments':comments, 'new_comment':new_comment})

def mail_send_view(request,post_id):
    post= get_object_or_404(Post,id=post_id,status='published')
    sent = False
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            subject = '{} ({}) recommends you to read"{}"'.format(cd['name'],cd['email'], post.title)
            post_url = request.build_absolute_uri(post.get_absolute_url())
            message = 'Read Post At:\n{}\n\n{}\'s Comments:\n{}'.format(post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'abhirvablog@gmail.com',[cd['to']])
            sent=True
    else:
        form=EmailSendForm()
    return render(request, "sharebymail.html", {'form':form, 'post':post, 'sent':sent})





























# Create your views here.
#def post_list_view(request):
    #post_list = Post.objects.all()
   # return render(request, "blog/post_list.html",{'post_list':post_list})

#def post_detail_view(request,year,month,day,post):
    #post = get_object_or_404(Post,slug_field=post,
    #                         status='published',
    #                         publish__year=year,
    #                         publish__month=month,
    #                         publish__day=day)
    #return render(request,'blog/post_detail.html',{'post':post})

#def post_list(self,request):
    #    post_list = Post.objects.all()
    #    paginator = Paginator(post_list,2)
    #    page_number = request.GET.get('page')
    #    try:
    #        post_list=paginator.page(page_number)
    #    except PageNotAnInteger:
     #       post_list=paginator.page(1)
     #   except EmptyPage:
    #        post_list=paginator.page(paginator.num_pages)
    #    return render(request,"blog/post_list.html",{'post_list':post_list})
