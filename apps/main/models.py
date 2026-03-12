from django.db import models
from apps.common.mixins import SlugifyMixin
from tinymce.models import HTMLField
from django.utils.safestring import mark_safe
from django.core.validators import FileExtensionValidator
from apps.common.models import BaseModel
from apps.common.utils import generate_upload_path
from apps.common.validators import file_size, file_size_50


# =============================================
# MAIN SECTION - Settings (Singletons)
# =============================================

class MainSettings(BaseModel):
    logo = models.ImageField(
        upload_to=generate_upload_path,
        verbose_name="Logo",
        validators=[file_size],
        help_text="Rasm 5 MB dan katta bo'lishi mumkin emas."
    )
    title = models.CharField(max_length=500, verbose_name="Sarlavha")
    short_description = models.CharField(max_length=500, verbose_name="Qisqa Tavsif", null=True, blank=True)
    menu_timer = models.DateTimeField(verbose_name="Bosh menyu Timer", null=True, blank=True)

    # Section description texts
    main_participants = models.SmallIntegerField(
        verbose_name="Asosiy qatnashchilar",
        null=True, blank=True
    )
    top_managers = models.SmallIntegerField(
        verbose_name="Top menejerlar",
        null=True, blank=True
    )
    department_personnel = models.SmallIntegerField(
        verbose_name="Bo'lim shaxslari",
        null=True, blank=True
    )
    sponsors_and_partners = models.SmallIntegerField(
        verbose_name="Homiylar va hamkorlar",
        null=True, blank=True
    )
    location = models.CharField(max_length=500, verbose_name="Joylashuv", null=True, blank=True)

    facebook = models.URLField(verbose_name="Facebook", null=True, blank=True)
    instagram = models.URLField(verbose_name="Instagram", null=True, blank=True)
    youtube = models.URLField(verbose_name="YouTube", null=True, blank=True)
    x = models.URLField(verbose_name="X (Twitter)", null=True, blank=True)
    quote = models.TextField(verbose_name="Iqtibos", null=True, blank=True)

    phone_number = models.CharField(max_length=255, verbose_name="Telefon raqami")
    email = models.EmailField(verbose_name="Email")
    address = models.CharField(max_length=500, verbose_name="Manzil")

    def __str__(self):
        return "Asosiy sozlamalar"

    class Meta:
        verbose_name = "Asosiy sozlamalar"
        verbose_name_plural = "Asosiy sozlamalar"


# =============================================
# WEB SECTION - Content
# =============================================

class Event(SlugifyMixin, BaseModel):
    title = models.CharField(max_length=500, verbose_name="Sarlavha")
    slug = models.SlugField(max_length=500, verbose_name="Slug")
    address = models.CharField(max_length=500, verbose_name="Manzil")
    start_date = models.DateTimeField(verbose_name="Boshlanish sanasi")
    end_date = models.DateTimeField(verbose_name="Tugash sanasi", null=True, blank=True)
    content = HTMLField(verbose_name="Tafsilot")
    short_description = models.TextField(verbose_name="Qisqa tavsif", null=True, blank=True)
    location = models.CharField(max_length=500, verbose_name="Joylashuv")
    image = models.ImageField(
        upload_to=generate_upload_path,
        verbose_name="Rasm",
        validators=[file_size_50],
        null=True, blank=True,
        help_text="Rasm 50 MB dan katta bo'lishi mumkin emas."
    )

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" style="height: 50px; object-fit: cover;" />')
        return ""

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tadbir"
        verbose_name_plural = "Tadbirlar"
        ordering = ['-start_date']
        constraints = [
            models.UniqueConstraint(
                fields=['slug'],
                name='unique_event_slug',
            )
        ]


class EventSchedule(BaseModel):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE,
        verbose_name="Tadbir",
        related_name="schedules",
    )
    date = models.DateField(verbose_name="Sana")
    name = models.CharField(max_length=500, verbose_name="Nomi")
    start_time = models.TimeField(verbose_name="Boshlanish vaqti")
    end_time = models.TimeField(verbose_name="Tugash vaqti")

    def __str__(self):
        return f"{self.event.title} - {self.name}"

    class Meta:
        verbose_name = "Kun tartibi"
        verbose_name_plural = "Kun tartibi"
        ordering = ['date', 'start_time']


class Speaker(BaseModel):
    full_name = models.CharField(max_length=500, verbose_name="F.I.O")
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE,
        verbose_name="Tadbir",
        related_name="speakers",
    )
    profession = models.CharField(max_length=500, verbose_name="Lavozimi", null=True, blank=True)
    content = HTMLField(verbose_name="Tafsilot", null=True, blank=True)
    image = models.ImageField(
        upload_to=generate_upload_path,
        verbose_name="Rasm",
        validators=[file_size],
        null=True, blank=True,
        help_text="Rasm 5 MB dan katta bo'lishi mumkin emas."
    )

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" style="height: 50px; object-fit: cover; border-radius: 50%;" />')
        return ""

    def __str__(self):
        return f"{self.full_name} - {self.event.title}"

    class Meta:
        verbose_name = "Spiker"
        verbose_name_plural = "Spikerlar"


MEDIA_TYPE_CHOICES = [
    ('image', 'Rasm'),
    ('video', 'Video'),
    ('file', 'Fayl'),
]


class EventMedia(BaseModel):
    name = models.CharField(max_length=500, verbose_name="Nomi")
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE,
        verbose_name="Tadbir",
        related_name="event_media",
    )
    date = models.DateField(verbose_name="Sana", null=True, blank=True)
    type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPE_CHOICES,
        default='image',
        verbose_name="Turi"
    )
    file = models.FileField(
        upload_to=generate_upload_path,
        verbose_name="Fayl",
        validators=[file_size_50],
        null=True, blank=True,
        help_text="Fayl 50 MB dan katta bo'lishi mumkin emas."
    )
    url = models.URLField(verbose_name="Havola", null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

    class Meta:
        verbose_name = "Tadbir mediasi"
        verbose_name_plural = "Tadbir medialari"


class News(BaseModel):
    title = models.CharField(max_length=500, verbose_name="Sarlavha")
    image = models.ImageField(
        upload_to=generate_upload_path,
        verbose_name="Rasm",
        validators=[file_size],
        null=True, blank=True,
        help_text="Rasm 5 MB dan katta bo'lishi mumkin emas."
    )
    content = HTMLField(verbose_name="Tafsilot")

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" style="height: 50px; object-fit: cover;" />')
        return ""

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"
        ordering = ['-created_at']


class Supporter(BaseModel):
    logo = models.ImageField(
        upload_to=generate_upload_path,
        verbose_name="Logo",
        validators=[file_size],
        help_text="Rasm 5 MB dan katta bo'lishi mumkin emas."
    )
    company_name = models.CharField(max_length=500, verbose_name="Kompaniya nomi")

    def logo_tag(self):
        if self.logo:
            return mark_safe(f'<img src="{self.logo.url}" style="height: 40px; object-fit: contain;" />')
        return ""

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = "Qo'llab-quvvatlovchi"
        verbose_name_plural = "Qo'llab-quvvatlovchilar"


class Sponsor(BaseModel):
    logo = models.ImageField(
        upload_to=generate_upload_path,
        verbose_name="Logo",
        validators=[file_size_50],
        help_text="Rasm 50 MB dan katta bo'lishi mumkin emas."
    )
    company_name = models.CharField(max_length=500, verbose_name="Kompaniya nomi")

    def logo_tag(self):
        if self.logo:
            return mark_safe(f'<img src="{self.logo.url}" style="height: 40px; object-fit: contain;" />')
        return ""

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = "Homiy"
        verbose_name_plural = "Homiylar"


class FAQ(BaseModel):
    question = models.CharField(max_length=500, verbose_name="Savol")
    answer = HTMLField(verbose_name="Javob")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"


class Comment(BaseModel):
    image = models.ImageField(
        upload_to=generate_upload_path,
        verbose_name="Rasm",
        validators=[file_size_50],
        null=True, blank=True,
        help_text="Rasm 50 MB dan katta bo'lishi mumkin emas."
    )
    full_name = models.CharField(max_length=500, verbose_name="F.I.O")
    profession = models.CharField(max_length=500, verbose_name="Lavozimi")
    comment = HTMLField(verbose_name="Izoh")

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" style="height: 50px; width: 50px; object-fit: cover; border-radius: 50%;" />')
        return ""

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Izoh"
        verbose_name_plural = "Izohlar"
        ordering = ['-created_at']


class PastForum(BaseModel):
    image = models.ImageField(
        upload_to=generate_upload_path,
        verbose_name="Rasm",
        validators=[file_size_50],
        null=True, blank=True,
        help_text="Rasm 50 MB dan katta bo'lishi mumkin emas."
    )
    name = models.CharField(max_length=500, verbose_name="Nomi")

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" style="height: 50px; object-fit: cover;" />')
        return ""

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "O'tgan forum"
        verbose_name_plural = "O'tgan forumlar"


# =============================================
# FORMS SECTION - Submissions
# =============================================

class PresentationSubmission(BaseModel):
    full_name = models.CharField(max_length=500, verbose_name="Ism va familiya")
    profession = models.CharField(max_length=500, verbose_name="Lavozim")
    organization_name = models.CharField(max_length=500, verbose_name="Tashkilot nomi")
    phone = models.CharField(max_length=255, verbose_name="Telefon raqami")
    email = models.EmailField(verbose_name="Email manzili")
    organization_website = models.URLField(
        verbose_name="Tashkilot sayti",
    )
    presentation_topic = models.CharField(max_length=500, verbose_name="Taqdimot mavzusi")
    pdf_file = models.FileField(
        upload_to=generate_upload_path,
        verbose_name="PDF fayl",
        validators=[file_size_50, FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="Fayl 50 MB dan katta bo'lishi mumkin emas. PDF formatida bo'lishi kerak."
    )

    def __str__(self):
        return f"{self.full_name} - {self.organization_name}"

    class Meta:
        verbose_name = "Taqdimot arizasi"
        verbose_name_plural = "Taqdimot arizalari"
        ordering = ['-created_at']


class PartnerApplication(BaseModel):
    organization_name = models.CharField(max_length=500, verbose_name="Tashkilot nomi")
    contact_person = models.CharField(max_length=500, verbose_name="Bog'lanish uchun shaxs")
    phone = models.CharField(max_length=255, verbose_name="Telefon raqami")
    email = models.EmailField(verbose_name="Email manzili")

    def __str__(self):
        return f"{self.organization_name} - {self.contact_person}"

    class Meta:
        verbose_name = "Hamkorlik arizasi"
        verbose_name_plural = "Hamkorlik arizalari"
        ordering = ['-created_at']


class Certificate(BaseModel):
    file = models.FileField(
        upload_to=generate_upload_path,
        verbose_name="PDF fayl",
        null=True, blank=True,
        validators=[file_size_50, FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="Fayl 50 MB dan katta bo'lishi mumkin emas. PDF formatida bo'lishi kerak."
    )
    
    event_name = models.CharField(max_length=500, verbose_name="Tadbir nomi")
    full_name = models.CharField(max_length=500, verbose_name="Ism va familiya")
    certificate_number = models.CharField(max_length=255, verbose_name="Sertifikat raqami")

    def __str__(self):
        return f"{self.full_name} - {self.certificate_number}"

    class Meta:
        verbose_name = "Sertifikat tekshiruvi"
        verbose_name_plural = "Sertifikat tekshiruvlari"
        ordering = ['-created_at']
