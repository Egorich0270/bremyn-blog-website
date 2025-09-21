from django.db import models

from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Card(models.Model):
    title = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    description = models.TextField()
    description_ru = models.TextField()
    preview = models.FileField(upload_to='cards/previews/')
    content_type = models.CharField(max_length=50, choices=[('image', 'Image'), ('video', 'Video')], default='image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    template_name = models.CharField(max_length=200, default='Gallery/Cards/card_default')
    tags = models.ManyToManyField(Tag, through='CardTag', related_name='cards')
    def __str__(self):
        return self.title


class CardTag(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('card', 'tag')
    def __str__(self):
        return f"{self.card} ↔ {self.tag}"


class AboutAuthor(models.Model):
    content_ru = models.TextField("Текст (RU)", blank=True)
    content_en = models.TextField("Text (EN)", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"AboutAuthor ({self.created_at.date()})"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    feedback_contact = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name}: {self.message[:30]}"
