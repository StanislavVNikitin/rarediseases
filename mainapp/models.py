from django.db import models
from django.urls import reverse


# from django.urls import reverse

class Disease(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, verbose_name="Url страницы", unique=True)
    description = models.TextField(blank=True, verbose_name="Описание заболевания")
    codemkb = models.CharField(max_length=10, blank=True, verbose_name="Код по МКБ")
    search = models.CharField(max_length=255, blank=True, verbose_name="Для поиска")
    tags = models.ManyToManyField("Tag", blank=True, related_name="diseases", verbose_name="Тэг")
    communities = models.ManyToManyField('Community', blank=True, related_name="diseases", verbose_name="Сообщество")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return self.title

    def delete(self, *args):
        self.deleted = True
        self.save()

    def get_absolute_url(self):
        return reverse("mainapp:disease", kwargs={"slug": self.slug})

    def not_empty_codemkb(self):
        return self.codemkb

    class Meta:
        verbose_name = "Заболевание"
        verbose_name_plural = "Заболевания"
        ordering = ["title"]


class Community(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, verbose_name="Url страницы", unique=True)
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return self.title

    def delete(self, *args):
        self.deleted = True
        self.save()

    def get_absolute_url(self):
        pass
        # return reverse("mainapp:page_slug", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Сообщство"
        verbose_name_plural = "Сообщества"
        ordering = ["title"]


class Contact(models.Model):
    CONTACT_CHOICES = [
        ("EMAIL", "Емеил"),
        ("PHONE", "Телефон"),
        ("TG", "Телеграм"),
        ("WHATSAPP", "WhatsApp"),
        ("VK", "ВКонтакте"),
        ("SITE", "Сайт"),
        ("OK", "Однокласники"),
        ("FB", "Facebook"),
        ("INSTAGRAM", "Instagram")
    ]
    type = models.CharField(max_length=9, choices=CONTACT_CHOICES, blank=True, verbose_name="Тип")
    content = models.CharField(max_length=255, verbose_name="Содержание ссылки")
    community = models.ForeignKey('Community', on_delete=models.CASCADE, related_name="contact",
                                  verbose_name="Сообщество")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return self.content

    def delete(self, *args):
        self.deleted = True
        self.save()

    def get_type_icone(self):
        if self.type == 'SITE':
            return 'fa-solid fa-earth-americas'
        elif self.type == 'WHATSAPP':
            return 'fa-brands fa-whatsapp'
        elif self.type == 'EMAIL':
            return 'fa-regular fa-envelope>'
        elif self.type == 'PHONE':
            return 'fa-solid fa-phone'
        elif self.type == 'TG':
            return 'fa-brands fa-telegram'
        elif self.type == 'VK':
            return 'fa-brands fa-vk'
        elif self.type == 'OK':
            return 'fa-brands fa-square-odnoklassniki'
        elif self.type == "FB":
            return 'fa-brands fa-facebook'
        elif self.type == 'INSTAGRAM':
            return 'fa-brands fa-instagram'
        else:
            return ''

    def get_contact_url(self):
        if self.type == 'EMAIL':
            return 'mailto:' + self.content
        elif self.type == 'PHONE':
            return 'tel:' + self.content
        else:
            return self.content

    get_type_icone.short_description = 'Иконки типов контактов'
    get_contact_url.short_description = 'Url контакта'

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название")
    slug = models.SlugField(max_length=50, verbose_name="Url тэга", unique=True)
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return self.title

    def delete(self, *args):
        self.deleted = True
        self.save()

    def get_absolute_url(self):
        return reverse("mainapp:tag", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"
        ordering = ["title"]
