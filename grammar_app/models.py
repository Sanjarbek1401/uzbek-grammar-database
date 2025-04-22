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
    TURKUMI_CHOICES = [
        ('Ko\'makchi', 'Ko\'makchi'),
        ('Bog\'lovchi', 'Bog\'lovchi'),
        ('Yuklama', 'Yuklama'),
    ]

    category = models.ForeignKey(GrammaticalCategory, on_delete=models.CASCADE, related_name='forms')
    term = models.CharField(max_length=255)
    grammatical_meaning = models.TextField()
    usage = models.CharField(max_length=100, choices=TURKUMI_CHOICES, verbose_name='Turkumi')
    translation = models.TextField(blank=True)
    period = models.CharField(max_length=100, blank=True)
    style = models.CharField(max_length=100, blank=True)
    
    special_code = models.CharField(max_length=100, blank=True)
    style_literary = models.CharField(max_length=100, blank=True)
    style_scientific = models.CharField(max_length=100, blank=True)
    style_journalistic = models.CharField(max_length=100, blank=True)
    style_official = models.CharField(max_length=100, blank=True)
    style_colloquial = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['term']

    def __str__(self):
        return f"{self.term} ({self.category.name})"

    def get_absolute_url(self):
        return reverse('form_detail', kwargs={'pk': self.pk})


class Example(models.Model):
    grammatical_form = models.ForeignKey(GrammaticalForm, on_delete=models.CASCADE, related_name='examples')
    uzbek_text = models.TextField()  # Using TextField for unlimited length
    english_translation = models.TextField(blank=True)  # Using TextField for unlimited length

    def __str__(self):
        return self.uzbek_text[:50]


class UslubData(models.Model):
    yordamchi_soz = models.CharField(max_length=255, verbose_name="Yordamchi so'z")
    maxsus_kodi = models.CharField(max_length=255, verbose_name="Maxsus kodi", blank=True)
    grammatik_manosi = models.TextField(verbose_name="Grammatik ma'nosi", blank=True)
    badiiy = models.BooleanField(default=False, verbose_name="Badiiy")
    ilmiy = models.BooleanField(default=False, verbose_name="Ilmiy")
    publitsistik = models.BooleanField(default=False, verbose_name="Publitsistik")
    rasmiy = models.BooleanField(default=False, verbose_name="Rasmiy")
    sozlashuv = models.BooleanField(default=False, verbose_name="So'zlashuv")

    def __str__(self):
        return self.yordamchi_soz

    class Meta:
        verbose_name = "Uslub ma'lumoti"
        verbose_name_plural = "Uslub ma'lumotlari"


class WordSynonym(models.Model):
    grammatical_word = models.CharField(max_length=255, verbose_name="Grammatik so'z")
    translations = models.TextField(verbose_name="Tarjimalar", blank=True)
    identity = models.CharField(max_length=255, verbose_name="Identifikator", blank=True)
    synonyms = models.TextField(verbose_name="Sinonimlar", blank=True)

    class Meta:
        verbose_name = "So'z sinonimi"
        verbose_name_plural = "So'z sinonimlari"
        ordering = ['grammatical_word']

    def __str__(self):
        return self.grammatical_word


class GrammatikManoData(models.Model):
    grammatik_manosi = models.TextField(verbose_name="So'zning grammatik ma'nosi")
    badiiy_uslub = models.TextField(verbose_name="Badiiy uslub", blank=True)
    ilmiy_uslub = models.TextField(verbose_name="Ilmiy uslub", blank=True)
    publitsistik_uslub = models.TextField(verbose_name="Publitsistik uslub", blank=True)
    rasmiy_uslub = models.TextField(verbose_name="Rasmiy uslub", blank=True)
    sozlashuv_uslubi = models.TextField(verbose_name="So'zlashuv uslubi", blank=True)

    class Meta:
        verbose_name = "Grammatik ma'no bo'yicha ma'lumot"
        verbose_name_plural = "Grammatik ma'no bo'yicha ma'lumotlar"
        ordering = ['grammatik_manosi']

    def __str__(self):
        return self.grammatik_manosi


class DavriylikiData(models.Model):
    period_11_12 = models.CharField(max_length=255, verbose_name="XI-XII asr", blank=True)
    period_13_14 = models.CharField(max_length=255, verbose_name="XIII-XIV asr", blank=True)
    period_15_18 = models.CharField(max_length=255, verbose_name="XV-XVIII asr", blank=True)
    period_19 = models.CharField(max_length=255, verbose_name="XIX asr", blank=True)
    period_20 = models.CharField(max_length=255, verbose_name="XX asr", blank=True)
    
    class Meta:
        verbose_name = "So'z davriyligi"
        verbose_name_plural = "So'z davriyligiga ko'ra"
    
    def __str__(self):
        return f"Davr: {self.period_11_12} - {self.period_20}"


class Sinonimlar(models.Model):
    grammatik_manosi = models.TextField(verbose_name="So'zning grammatik ma'nosi")
    sinonimlar = models.TextField(verbose_name="Sinonimlar")
    misol = models.TextField(verbose_name="Misol", blank=True)
    english = models.TextField(verbose_name="In English", blank=True)
    
    class Meta:
        verbose_name = "Sinonim"
        verbose_name_plural = "Sinonimlar"
        ordering = ['grammatik_manosi']
    
    def __str__(self):
        return self.grammatik_manosi