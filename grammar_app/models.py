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


class CodedWord(models.Model):
    special_code = models.CharField(max_length=255, verbose_name="So'zning maxsus kodi", db_column="sozning_maxsus_kodi")
    auxiliary_word = models.CharField(max_length=255, verbose_name="Yordamchi so'z", db_column="yordamchi_soz")
    grammatical_code = models.CharField(max_length=255, verbose_name="Grammatik kodi", db_column="grammatik_kodi")
    primary_meaning = models.TextField(verbose_name="So'zning birlamchi grammatik ma'nosi", db_column="sozning_birlamchi_grammatik_manosi")
    secondary_meaning = models.TextField(verbose_name="Ikkilamchi grammatik ma'nosi", blank=True, null=True, db_column="ikkilamchi_grammatik_manosi")
    third_meaning = models.TextField(verbose_name="Uchinchi grammatik ma'nosi", blank=True, null=True, db_column="uchinchi_grammatik_manosi")
    fourth_meaning = models.TextField(verbose_name="To'rtinchi grammatik ma'nosi", blank=True, null=True, db_column="tortinchi_grammatik_manosi")
    fifth_meaning = models.TextField(verbose_name="Beshinchi grammatik ma'nosi", blank=True, null=True, db_column="beshinchi_grammatik_manosi")
    sixth_meaning = models.TextField(verbose_name="Oltinchi grammatik ma'nosi", blank=True, null=True, db_column="oltinchi_grammatik_manosi")
    seventh_meaning = models.TextField(verbose_name="Yettinchi grammatik ma'nosi", blank=True, null=True, db_column="yettinchi_grammatik_manosi")
    eighth_meaning = models.TextField(verbose_name="Sakkizinchi grammatik ma'nosi", blank=True, null=True, db_column="sakkizinchi_grammatik_manosi")
    ninth_meaning = models.TextField(verbose_name="To'qqizinchi grammatik ma'nosi", blank=True, null=True, db_column="toqqizinchi_grammatik_manosi")
    tenth_meaning = models.TextField(verbose_name="O'ninchi grammatik ma'nosi", blank=True, null=True, db_column="oninchi_grammatik_manosi")

    class Meta:
        verbose_name = "Kodlangan so'z"
        verbose_name_plural = "Kodlangan so'zlar"
        ordering = ['special_code']

    def __str__(self):
        return f"{self.special_code} - {self.auxiliary_word}"