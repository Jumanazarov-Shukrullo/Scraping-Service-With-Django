# import jsonfield
import jsonfield as jsonfield
from django.db import models
from django.template.defaultfilters import slugify


def default_urls():
    return {"hh_uz": '', }


class City(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(City, self).save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Programming Language'
        verbose_name_plural = 'Programming Languages'

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Language, self).save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='title')
    company = models.CharField(max_length=250, verbose_name='Company name')
    description = models.TextField(verbose_name='Description')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Enter City')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name='Programming Language')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vacancy'
        verbose_name_plural = 'Vacancies'
        ordering = ('-timestamp', )

    def __str__(self):
        return f"{self.title}"


class Error(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    data = jsonfield.JSONField()


class Url(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Enter City')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name='Programming Language')
    url_data = jsonfield.JSONField(default=default_urls)

    class Meta:
        unique_together = ('city', 'language')
