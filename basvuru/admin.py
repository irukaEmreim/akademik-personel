from django.contrib import admin
from .models import Kullanici, Ilan, KadroKriterleri, Basvuru, Belge, JuriDegerlendirme, Bildirim

admin.site.register(Kullanici)
admin.site.register(Ilan)
admin.site.register(KadroKriterleri)
admin.site.register(Basvuru)
admin.site.register(Belge)
admin.site.register(JuriDegerlendirme)
admin.site.register(Bildirim)
