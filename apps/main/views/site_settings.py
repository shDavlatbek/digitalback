from rest_framework.generics import RetrieveAPIView
from ..models import SiteSettings
from ..serializers.site_settings import SiteSettingsSerializer


class SiteSettingsView(RetrieveAPIView):
    serializer_class = SiteSettingsSerializer

    def get_object(self):
        obj, created = SiteSettings.objects.get_or_create(
            pk=SiteSettings.objects.values_list('pk', flat=True).first() or None,
            defaults={
                'school_life': "Maktabimiz hayoti haqida ma'lumot",
                'directions': "Bizning yo'nalishlar haqida ma'lumot",
                'numbers': "Maktab raqamlari haqida ma'lumot",
                'teachers': "O'qituvchilarimiz haqida ma'lumot",
                'honors': "Maktabimiz faxrlari haqida ma'lumot",
                'news': "Yangiliklar bo'limi haqida ma'lumot",
                'gallery': "Galereya bo'limi haqida ma'lumot",
                'contact': "Bog'lanish bo'limi haqida ma'lumot",
                'comments': "Izohlar bo'limi haqida ma'lumot",
                'faqs': "Ko'p beriladigan savollar haqida ma'lumot",
                'leaders': "Rahbariyat bo'limi haqida ma'lumot",
                'vacancies': "Vakansiyalar bo'limi haqida ma'lumot",
                'documents': "Hujjatlar bo'limi haqida ma'lumot",
                'timetables': "O'quv reja bo'limi haqida ma'lumot",
                'edu_infos': "Ta'lim ma'lumotlari bo'limi haqida ma'lumot",
                'events': "Tadbirlar bo'limi haqida ma'lumot",
                'resources': "Resurslar bo'limi haqida ma'lumot",
                'culture_services': "Madaniy xizmatlar haqida ma'lumot",
                'culture_arts': "Madaniy san'at haqida ma'lumot",
                'fine_arts': "Tasviriy san'at haqida ma'lumot"
            }
        )
        return obj
