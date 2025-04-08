from django.db import models
from django.urls import reverse


class GrammaticalCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)  # For custom ordering

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Grammatical Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'pk': self.pk})


class GrammaticalForm(models.Model):
    category = models.ForeignKey(GrammaticalCategory, on_delete=models.CASCADE, related_name='forms')
    term = models.CharField(max_length=100)
    grammatical_meaning = models.TextField(blank=True)
    usage = models.TextField(blank=True)
    translation = models.CharField(max_length=200, blank=True)
    period = models.CharField(max_length=100, blank=True)
    style = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['term']

    def __str__(self):
        return self.term

    def get_absolute_url(self):
        return reverse('form_detail', kwargs={'pk': self.pk})


class Example(models.Model):
    grammatical_form = models.ForeignKey(GrammaticalForm, on_delete=models.CASCADE, related_name='examples')
    uzbek_text = models.TextField()
    english_translation = models.TextField()

    def __str__(self):
        return self.uzbek_text[:50]