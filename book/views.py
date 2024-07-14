from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from . models import Guru as Teacher
from . models import Register as Santri
from . forms import *
from . resources import RegisterResource
from . filters import DataFilter

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from django.contrib.auth.decorators import login_required
from .decorators import *
from .telegram_util import send_telegram_message
from django.contrib.humanize.templatetags.humanize import intcomma
# Create your views here.

# Master
@login_required(login_url='login')
# @ijinkan_pengguna(yang_diizinkan=["master"])
@pilihan_login
def home(request):
    data = Register.objects.all()
    total_data = data.count()
    data_putra = data.filter(gender_santri = 'Laki-Laki').count()
    data_putri = data.filter(gender_santri = 'Perempuan').count()
    data_alumni = data.filter(status_santri = 'Lulus').count()

    jeda = {
        "judul": "Beranda",
        "menu": "home",
        "santri": total_data,
        "putra": data_putra,
        "putri": data_putri, 
        "alumni": data_alumni,
    }
    return render(request, 'halaman/home.html', jeda)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=["master"])
def data(request):
    data_santri = Register.objects.filter(status_santri='Aktif')
    filter_data = DataFilter(request.GET, queryset=data_santri)
    data_santri = filter_data.qs

    jeda = {
        "judul": "Daftar Data Santri",
        "menu": "data",
        "d_santri": data_santri,
        "filter": filter_data,
    }
    return render(request, 'halaman/data.html', jeda)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=["master"])
def dataguru(request):
    data_guru = Teacher.objects.order_by('-id') # order by id descending (data terbaru)

    jeda = {
        "judul": "Daftar Data Guru",
        "menu": "dataguru",
        "d_guru": data_guru,
    }
    return render(request, 'halaman/guru.html', jeda)


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=["master"])
def add_dataguru(request):
    f_register = GuruForm()

    if request.method == 'POST':
        # print('Cetak POST:', request.POST)
        f_simpan = GuruForm(request.POST)
        if f_simpan.is_valid:
            f_simpan.save()
            return redirect('dataguru')

    jeda = {
        "judul": "Add Data Guru",
        "menu": "dataguru",
        "form": f_register,
    }
    return render(request, 'halaman/new_dataguru.html', jeda)


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=["master"])
def edit_dataguru(request, pk):
    data_guru = Teacher.objects.get(id=pk)
    f_register = GuruForm(instance=data_guru)

    if request.method == 'POST':
        # print('Cetak POST:', request.POST)
        f_simpan = GuruForm(request.POST, instance=data_guru)
        if f_simpan.is_valid:
            f_simpan.save()
            return redirect('dataguru')

    jeda = {
        "judul": "Edit Data Guru",
        "menu": "dataguru",
        "form": f_register,
    }
    return render(request, 'halaman/edit_dataguru.html', jeda)


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=["master"])
def delete_dataguru(request, pk):
    data_guru = Teacher.objects.get(id=pk)
    data_guru.delete()
    return redirect('dataguru')



@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=["master"])
def detail_data(request, pk):
    detail_santri = Register.objects.get(nis=pk)

    jeda = {
        "judul": "Detail Profil Santri",
        "menu": "data",
        "dj": detail_santri,
    }
    return render(request, 'halaman/detail.html', jeda)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=["master"])
def add_data(request):
    f_register = RegisterForm()

    if request.method == 'POST':
        # print('Cetak POST:', request.POST)
        f_simpan = RegisterForm(request.POST, request.FILES)
        if f_simpan.is_valid:
            f_simpan.save()
            return redirect('data')

    jeda = {
        "judul": "Add Data Santri",
        "menu": "data",
        "form": f_register,
    }
    return render(request, 'halaman/new_data.html', jeda)


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=["master"])
def update_data(request, pk):
    data = Register.objects.get(nis=pk)
    f_register = RegisterForm(instance=data)

    if request.method == 'POST':
        f_edit = RegisterForm(request.POST, request.FILES, instance=data)
        if f_edit.is_valid:
            f_edit.save()
            return redirect('data')

    jeda = {
        "judul": "Update Data Santri",
        "menu": "data",
        "form": f_register,
    }
    return render(request, 'halaman/new_data.html', jeda)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=["master"])
def wilayah(request):
    f_wilayah = WilayahForm()
    data_wilayah = Wilayah.objects.all()

    formWilayah = WilayahForm(request.POST)

    if request.method == 'POST':
        username = request.POST.get("username")
        password1 = request.POST.get("password")
        password2 = request.POST.get("password2")

        if username == "":
            messages.warning(request, "Username tidak boleh kosong.")
            return redirect("wilayah")
        if password1 == "":
            messages.warning(request, "Password tidak boleh kosong.")
            return redirect("wilayah")
        if password2 == "":
            messages.warning(request, "Mohon konfirmasi password Anda.")
            return redirect("wilayah")
        if User.objects.filter(username=username).first():
            messages.warning(request, "Username sudah ada.")
            return redirect("wilayah")
        if password1 != password2:
            messages.warning(request, "Password tidak sama!")
            return redirect("wilayah")

         # menambahkan data ke dalam table User
        user = User.objects.create_user(username=username)
        user.set_password(password1)
        user.is_active = True
        user.save()

        # Group
        addGroup = Group.objects.get(name="wilayah")
        user.groups.add(addGroup)

        formSimpanWilayah = formWilayah.save()
        formSimpanWilayah.user = user
        formSimpanWilayah.save()

        return redirect('wilayah')

    jeda = {
        "judul": "Daftar Wilayah",
        "menu": "wilayah",
        "form": f_wilayah,
        "wilayah": data_wilayah,
    }
    return render(request, 'halaman/wilayah.html', jeda)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=["master"])
def update_wilayah(request, pk):
    data = Wilayah.objects.get(nama_wilayah=pk)
    f_wilayah = WilayahForm(instance=data)
    data_wilayah = Wilayah.objects.all()

    if request.method == 'POST':
        f_edit = WilayahForm(request.POST, instance=data)
        if f_edit.is_valid:
            f_edit.save()
            return redirect('wilayah')

    jeda = {
        "judul": "Update Data Wilayah",
        "menu": "wilayah",
        "form": f_wilayah,
        "wilayah": data_wilayah,
    }
    return render(request, 'halaman/wilayah.html', jeda)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=["master"])
def alumni(request):
    santri = Register.objects.filter(status_santri='Lulus')

    jeda = {
        "judul": "Daftar Alumni",
        "menu": "alumni",
        "alumni": santri,
    }
    return render(request, 'halaman/alumni.html', jeda)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=["master"])
def update_alumni(request, pk):
    data = Register.objects.get(nis=pk)
    f_wilayah = AlumniForm(instance=data)

    if request.method == 'POST':
        f_edit = AlumniForm(request.POST, instance=data)
        if f_edit.is_valid:
            f_edit.save()
            return redirect('alumni')

    jeda = {
        "judul": "Update Status Santri",
        "menu": "alumni",
        "form": f_wilayah,
    }
    return render(request, 'halaman/edit_alumni.html', jeda)


# Wilayah
@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=["wilayah"])
# @pilihan_login
def beranda_wil(request):
    santri = request.user.wilayah.register_set.all()
    total = santri.count()
    putra = santri.filter(gender_santri='Laki-Laki').count()
    putri = santri.filter(gender_santri='Perempuan').count()
    alumni = santri.filter(status_santri='Lulus').count()

    jeda = {
        "judul": "Beranda",
        "menu": "beranda_wil",
        "total": total,
        "putra": putra,
        "putri": putri,
        "alumni": alumni,
    }
    return render(request, 'wilayah/home.html', jeda)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=["wilayah"])
def data_wil(request):
    santri_wilayah = request.user.wilayah.register_set.all()
    data = santri_wilayah.filter(status_santri='Aktif')
    filter_data = DataFilter(request.GET, queryset=data)
    data = filter_data.qs

    jeda = {
        "judul": "Data Santri",
        "menu": "data_wil",
        "data": data,
        "filter": filter_data,
    }
    return render(request, 'wilayah/data.html', jeda)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=["wilayah"])
def alumni_wil(request):
    alumni  = request.user.wilayah.register_set.all()
    data = alumni.filter(status_santri='Lulus')

    jeda = {
        "judul": "Data Alumni Santri",
        "menu": "alumni_wil",
        "alumni": data,
    }
    return render(request, 'wilayah/alumni.html', jeda)


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=["wilayah"])
def detail_wil(request, pk):
    detail_santri = Register.objects.get(nis=pk)

    jeda = {
        "judul": "Detail Profil Santri",
        "menu": "data_wil",
        "dj": detail_santri,
    }
    return render(request, 'wilayah/detail.html', jeda)

# Utilitas
@tolakhalaman_ini
def entry(request):
    f_login = AuthenticationForm()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        cek_data = authenticate(request, username=username, password=password)

        if cek_data is not None:
            login(request, cek_data)
            return redirect('beranda')
        
        else:
            messages.error(request, 'Username atau password anda salah...')
            return redirect('login')

    else:
        jeda = {
            "judul": "PP. Jalaluddin Ar-Rumi",
            "menu": "Login",
            "form": f_login,
        }
        return render(request, 'auth/login.html', jeda)

def unplug(request):
    logout(request)
    return redirect('login')

def forbidden(request):
    jeda = {
        "judul": "Halaman tidak diizinkan!"
    }
    return render(request, 'auth/block.html', jeda)

def output(request):
    register = RegisterResource()
    data = register.export()
    response = HttpResponse(data.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="datasantri.xls"'
    
    return response

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=["wilayah"])
def pelanggaran_view(request):
    if request.method == 'POST':
        form = PelanggaranForm(request.POST)
        if form.is_valid():
            nama = form.cleaned_data['nama']
            kelas = form.cleaned_data['kelas']
            sekolah = form.cleaned_data['sekolah']
            alamat = form.cleaned_data['alamat']
            nomer_wa = form.cleaned_data['nomer_wa']
            subject = form.cleaned_data['subject']
            isi_pesan = form.cleaned_data['isi_pesan']
            
            # Ambil chat_id dari model ChatID berdasarkan nomor HP (atau kriteria lain)
            try:
                chat_id = ChatID.objects.filter(aktif=True).values_list('chatid', flat=True).first()
                # Format pesan yang akan dikirim
                message = f"Nama: {nama}\nKelas: {kelas}\nSekolah: {sekolah}\nAlamat: {alamat}\nNomer WA: {nomer_wa}\nSubject: {subject}\nIsi Pesan: {isi_pesan}"
                # Kirim pesan menggunakan bot Telegram
                send_telegram_message(chat_id, message)
                messages.success(request, "Pesan sukses dikirimkan ke yayasan")
                return redirect('pelanggaran')
            except ChatID.DoesNotExist:
                form.add_error(None, 'Chat ID tidak ditemukan untuk nomor HP ini.')
    else:
        form = PelanggaranForm()
    
    return render(request, 'pelanggaran_form.html', {'form': form, 'menu': 'pelanggaran', 'judul': 'Pelanggaran'})




@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=["wilayah"])
def get_student_data(request):
    nis = request.GET.get('nis')
    try:
        student = Santri.objects.get(nis=nis)
        data = {
            'nama': student.nama_lengkap,
            'kelas': student.kelas.tingkat,
            'sekolah': student.masuk_lembaga,
            'alamat': student.alamat,
            'nomer_wa': student.telp,
        }
        return JsonResponse(data)
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)