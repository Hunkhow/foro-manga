from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, TemplateView,
    CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Count

from .models import Thread, Post, Upvote
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from .services import fetch_genres, fetch_anime_by_genre, JikanError
from django.core.paginator import Paginator

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

class ThreadUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Thread
    fields = ['title', 'content', 'manga', 'tags']
    template_name = "forum/thread_form.html"
    login_url = 'login'
    raise_exception = True

    def test_func(self):
        t = self.get_object()
        return (self.request.user.is_staff
                or t.author == self.request.user)

class ThreadDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Thread
    template_name = "forum/thread_confirm_delete.html"
    success_url = reverse_lazy('home')
    login_url = 'login'
    raise_exception = True

    def test_func(self):
        t = self.get_object()
        return (self.request.user.is_staff
                or t.author == self.request.user)
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content']
    template_name = "forum/post_form.html"
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']
    template_name = "forum/post_form.html"
    login_url = 'login'
    raise_exception = True

    def test_func(self):
        p = self.get_object()
        return (
            self.request.user.is_staff
            or p.author == self.request.user
            or p.thread.author == self.request.user
        )

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "forum/post_confirm_delete.html"

    def get_success_url(self):
        # Al borrar una respuesta, volvemos al detalle de su hilo
        return reverse_lazy(
            "forum:thread-detail",
            kwargs={"slug": self.object.thread.slug}
        )

    def test_func(self):
        post = self.get_object()
        user = self.request.user
        # Puede borrar si es autor del post, autor del hilo o staff
        return (
            user == post.author or
            user == post.thread.author or
            user.is_staff
        )

class AnimeGenreListView(TemplateView):
    template_name = "forum/genre_list.html"
    paginate_by = 10  # géneros por página

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # 1) Traemos todos los géneros de anime
        try:
            genres = fetch_genres("anime")
        except JikanError as e:
            genres = []
            ctx["error"] = str(e)

        # 2) Filtrado por búsqueda
        q = self.request.GET.get("q", "").strip()
        if q:
            genres = [g for g in genres if q.lower() in g["name"].lower()]
        ctx["q"] = q

        # 3) Paginación manual
        paginator = Paginator(genres, self.paginate_by)
        page = self.request.GET.get("page")
        page_obj = paginator.get_page(page)

        ctx["genres"]   = page_obj.object_list
        ctx["page_obj"] = page_obj
        ctx["paginator"] = paginator

        return ctx


class AnimeListByGenreView(TemplateView):
    template_name = "forum/anime_by_genre.html"
    paginate_by = 12  # animes por página

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        genre_id = self.kwargs["genre_id"]

        # 1) Traer todos los animes del género (limit amplio)
        try:
            all_animes = fetch_anime_by_genre(genre_id, page=1, limit=25)
        except JikanError as e:
            ctx["animes"] = []
            ctx["error"] = str(e)
            return ctx

        # 2) Filtrado por búsqueda
        q = self.request.GET.get("q", "").strip()
        if q:
            filtered = [
                a for a in all_animes
                if q.lower() in a.get("title", "").lower()
            ]
        else:
            filtered = all_animes
        ctx["q"] = q

        # 3) Paginación local
        paginator = Paginator(filtered, self.paginate_by)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        ctx["animes"]   = page_obj.object_list
        ctx["page_obj"] = page_obj
        ctx["paginator"] = paginator
        ctx["genre_id"] = genre_id  

        return ctx


