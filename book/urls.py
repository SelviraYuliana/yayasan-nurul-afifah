from django.urls import path # type: ignore
from . import views

urlpatterns = [
    
    path('pelanggaran/', views.pelanggaran_view, name='pelanggaran'),
    path('get-student-data/', views.get_student_data, name='get_student_data'),

    # Utilitas
    path('login', views.entry, name='login'),
    path('logout', views.unplug, name='logout'),
    path('forbidden-access', views.forbidden, name='block_access'),
    path('unduh data santri', views.output, name='output'),

    # Master
    path('', views.home, name='beranda'),
    path('data_santri', views.data, name='data'),
    
    path('data_guru', views.dataguru, name='dataguru'),
    path('tambah_data_guru', views.add_dataguru, name='add_dataguru'),
    path('edit_data_guru/<str:pk>', views.edit_dataguru, name='update_dataguru'),
    path('delete_data_guru/<str:pk>', views.delete_dataguru, name='delete_dataguru'),
    
    path('detail_santri/<str:pk>', views.detail_data, name='detail_data'),
    path('tambah_data_santri', views.add_data, name='add_data'),
    path('edit_data_santri<str:pk>', views.update_data, name='update_data'),
    path('data_wilayah', views.wilayah, name='wilayah'),
    path('edit_data_wilayah<str:pk>', views.update_wilayah, name='update_wilayah'),
    path('data_alumni', views.alumni, name='alumni'),
    path('edit_data_alumni<str:pk>', views.update_alumni, name='update_alumni'),

    # Wilayah
    path('halaman beranda wilayah', views.beranda_wil, name='beranda_wil'),
    path('halaman data santri wilayah', views.data_wil, name='data_wil'),
    path('halaman data alumni wilayah', views.alumni_wil, name='alumni_wil'),
    path('halaman detail santri/<str:pk>', views.detail_wil, name='detail_wil'),
]
