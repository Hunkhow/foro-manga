from .models import Thread
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Thread, Post, Manga, Upvote
from django.urls import reverse_lazy, reverse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        # Llamamos al contexto base
        context = super().get_context_data(**kwargs)
        # Añadimos los 5 hilos más recientes
        context['recent_threads'] = Thread.objects.order_by('-created_at')[:5]
        return context

class ThreadListView(ListView):
    model               = Thread
    template_name       = "forum/thread_list.html"
    context_object_name = "threads"
    paginate_by         = 10

    def get_queryset(self):
        return (
            Thread.objects
                  .only('id','slug','title','created_at','author')
                  .annotate(num_upvotes=Count('posts__upvotes'))
                  .order_by('-num_upvotes','-created_at')
        )
class ThreadDetailView(LoginRequiredMixin, DetailView):
    model               = Thread
    template_name       = "forum/thread_detail.html"
    context_object_name = "thread"
    login_url           = 'login'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        thread = ctx['thread']
        # Total de upvotes en todos los posts de este hilo:
        agg = thread.posts.aggregate(total=Count('upvotes'))
        ctx['thread_upvotes'] = agg['total'] or 0

        # Lista de post_ids que este usuario ya votó, para desactivar botón
        user = self.request.user
        if user.is_authenticated:
            voted_ids = Upvote.objects.filter(
                user=user,
                post__thread=thread
            ).values_list('post_id', flat=True)
            ctx['user_upvoted_posts'] = set(voted_ids)
        else:
            ctx['user_upvoted_posts'] = set()

        return ctx

class ThreadCreateView(LoginRequiredMixin, CreateView):
    model = Thread
    fields = ['title', 'content', 'manga', 'tags']
    template_name = "forum/thread_form.html"
    login_url = 'login'
    redirect_field_name = 'next'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content']
    template_name = "forum/post_form.html"
    login_url = 'login'

    def get_context_data(self, **kwargs):
        # 1) Aceptamos **kwargs
        context = super().get_context_data(**kwargs)
        # 2) Inyectamos el thread en el contexto para el template
        context['thread'] = Thread.objects.get(slug=self.kwargs['slug'])
        return context

    def form_valid(self, form):
        # asignamos autor y thread antes de guardar
        form.instance.author = self.request.user
        form.instance.thread = Thread.objects.get(slug=self.kwargs['slug'])
        return super().form_valid(form)

    def get_success_url(self):
        # volvemos al detalle del mismo hilo
        return reverse_lazy('forum:thread-detail', kwargs={'slug': self.kwargs['slug']})

@login_required
def post_upvote_toggle(request, pk):
    post, created = None, False
    post = get_object_or_404(Post, pk=pk)
    up, created = Upvote.objects.get_or_create(user=request.user, post=post)
    if not created:
        up.delete()
    # volvemos a donde estábamos
    return redirect(
        request.META.get('HTTP_REFERER')
        or reverse('forum:thread-detail', kwargs={'slug': post.thread.slug})
    )