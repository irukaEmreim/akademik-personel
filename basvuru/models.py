from django.db import models
from django.contrib.auth.models import AbstractUser

class Kullanici(AbstractUser):
    tc_kimlik = models.CharField(max_length=11, unique=True)
    ad = models.CharField(max_length=100)
    soyad = models.CharField(max_length=100)
    rol = models.CharField(
        max_length=20,
        choices=[('Aday', 'Aday'), ('Admin', 'Admin'), ('Yönetici', 'Yönetici'), ('Jüri Üyesi', 'Jüri Üyesi')]
    )
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="kullanici_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="kullanici_set",
        blank=True
    )

    def __str__(self):
        return f"{self.ad} {self.soyad} ({self.rol})"

# İlan Modeli
class Ilan(models.Model):
    KADRO_TURLERI = [
        ('Dr. Öğr. Üyesi', 'Dr. Öğr. Üyesi'),
        ('Doçent', 'Doçent'),
        ('Profesör', 'Profesör'),
    ]
    baslik = models.CharField(max_length=255)
    aciklama = models.TextField()
    kadro = models.CharField(max_length=20, choices=KADRO_TURLERI)
    gereksinimler = models.TextField()
    baslangic_tarihi = models.DateField()
    bitis_tarihi = models.DateField()
    olusturan = models.ForeignKey(Kullanici, on_delete=models.SET_NULL, null=True)

# Kadro Kriterleri Modeli
class KadroKriterleri(models.Model):
    kriter_adi = models.CharField(max_length=255)
    kriter_detaylari = models.JSONField()

# Başvurular Modeli
class Basvuru(models.Model):
    DURUMLAR = [
        ('Beklemede', 'Beklemede'),
        ('Onaylandı', 'Onaylandı'),
        ('Reddedildi', 'Reddedildi'),
    ]
    kullanici = models.ForeignKey(Kullanici, on_delete=models.CASCADE)
    ilan = models.ForeignKey(Ilan, on_delete=models.CASCADE)
    durum = models.CharField(max_length=20, choices=DURUMLAR, default='Beklemede')
    basvuru_tarihi = models.DateTimeField(auto_now_add=True)

# Belgeler Modeli
class Belge(models.Model):
    BELGE_TURLERI = [
        ('Atıf Sayısı', 'Atıf Sayısı'),
        ('Konferans Yayını', 'Konferans Yayını'),
        ('Diğer', 'Diğer'),
    ]
    basvuru = models.ForeignKey(Basvuru, on_delete=models.CASCADE)
    belge_turu = models.CharField(max_length=50, choices=BELGE_TURLERI)
    dosya_yolu = models.CharField(max_length=255)
    yuklenme_tarihi = models.DateTimeField(auto_now_add=True)

# Jüri Değerlendirmeleri Modeli
class JuriDegerlendirme(models.Model):
    KARARLAR = [
        ('Olumlu', 'Olumlu'),
        ('Olumsuz', 'Olumsuz'),
    ]
    kullanici = models.ForeignKey(Kullanici, on_delete=models.CASCADE)
    basvuru = models.ForeignKey(Basvuru, on_delete=models.CASCADE)
    karar = models.CharField(max_length=20, choices=KARARLAR)
    degerlendirme_metni = models.TextField()
    degerlendirme_tarihi = models.DateTimeField(auto_now_add=True)

# Bildirimler Modeli
class Bildirim(models.Model):
    kullanici = models.ForeignKey(Kullanici, on_delete=models.CASCADE)
    mesaj = models.TextField()
    gonderim_tarihi = models.DateTimeField(auto_now_add=True)
