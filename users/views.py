from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfileForm,SignUpForm
from .models import Profile
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login

User = get_user_model()

# --------- Registro de usuario ---------
class SignUpView(CreateView):
    form_class    = SignUpForm
    template_name = 'registration/signup.html'  # <-- aquí apuntamos
    success_url   = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.get_or_create(user=self.object)
        login(self.request, self.object)
        return response

# --------- Ver detalle de perfil ---------
class ProfileDetailView(DetailView):
    model = Profile
    template_name = "users/profile_detail.html"
    slug_field    = "user__username"
    slug_url_kwarg = "username"
    context_object_name = "profile"

# --------- Editar perfil y datos de usuario ---------
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "users/profile_form.html"
    slug_field    = "user__username"
    slug_url_kwarg = "username"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        # forzar que solo edite su propio perfil
        return self.request.user.profile

# --------- Eliminar cuenta ---------
class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "users/account_confirm_delete.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        return self.request.user
    
@method_decorator(staff_member_required, name='dispatch')
class ProfileListView(ListView):
    model = Profile
    template_name = 'users/profile_list.html'
    context_object_name = 'profiles'
    paginate_by = 20

@method_decorator(staff_member_required, name='dispatch')
class ProfileDeleteView(DeleteView):
    model = Profile
    template_name = 'users/profile_confirm_delete.html'
    success_url = reverse_lazy('users:profile_list')

    def delete(self, request, *args, **kwargs):
        # al borrar el Profile, borramos también al User
        self.object = self.get_object()
        user = self.object.user
        response = super().delete(request, *args, **kwargs)
        user.delete()
        return response