from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from api import views


urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('', views.getRoutes),
    path('profile/', views.ProfileView.as_view(), name='get_profile'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='update_profile'),
    path('books/', views.BookListCreateView.as_view(), name='book_list_create'),
    path('my-books/', views.UserBooksList.as_view(), name='user-book-list'),
    path('books/<int:book_id>/', views.BookDetailView.as_view(), name='book_detail'),
    path('books/<int:book_id>/edit/', views.BookEditView.as_view(), name='book_edit'),
    path('books/<int:book_id>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    path('reading-lists/', views.ReadingListView.as_view(), name='reading_list'),
    path('reading-lists/<int:list_id>/', views.ReadingListDetailView.as_view(), name='reading_list_detail'),
    path('reading-lists/<int:list_id>/items/', views.ReadingListItemView.as_view(), name='reading_list_items'),
    path('reading-lists/<int:list_id>/items/<int:item_id>/', views.ReadingListItemView.as_view(), name='reading_list_items'),  # Updated URL
]