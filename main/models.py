from django.db import models


class Seo(models.Model):
    title = models.CharField(max_length=64, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    keywords = models.CharField(max_length=64, verbose_name='Keywords')

    class Meta:
        verbose_name = 'SEO-блок'
        verbose_name_plural = 'SEO-блоки'


class MainPage(models.Model):
    slide_1 = models.ImageField(upload_to='gallery/', verbose_name='Слайд 1')
    slide_2 = models.ImageField(upload_to='gallery/', verbose_name='Слайд 2')
    slide_3 = models.ImageField(upload_to='gallery/', verbose_name='Слайд 3')
    header = models.CharField(max_length=64, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Краткий текст')
    show_urls = models.BooleanField(default=True, verbose_name='Показывать ссылки на приложения')
    seo = models.OneToOneField(Seo, on_delete=models.PROTECT, verbose_name='SEO-блок')

    class Meta:
        verbose_name = 'Главная страница'


class Block(models.Model):
    page_id = models.ForeignKey(MainPage, on_delete=models.CASCADE, verbose_name='Главная страница')
    image = models.ImageField(upload_to='gallery/', verbose_name='Изображение')
    header = models.CharField(max_length=64, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Блок'
        verbose_name_plural = 'Блоки'


class AboutPage(models.Model):
    header = models.CharField(max_length=64, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Краткий текст')
    avatar = models.ImageField(upload_to='gallery/', verbose_name='Фото директора')
    additional_header = models.CharField(max_length=64, verbose_name='Дополнительный заголовок')
    additional_text = models.TextField(verbose_name='Дополнительный краткий текст')
    seo = models.OneToOneField(Seo, on_delete=models.PROTECT, verbose_name='SEO-блок')

    class Meta:
        verbose_name = 'О нас'


class Photo(models.Model):
    page_id = models.ForeignKey(AboutPage, on_delete=models.CASCADE, verbose_name='О нас')
    photo = models.ImageField(upload_to='gallery/', verbose_name='Фото')
    is_main = models.BooleanField(default=True, verbose_name='Главное фото')

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'


class Document(models.Model):
    page_id = models.ForeignKey(AboutPage, on_delete=models.CASCADE, verbose_name='О нас')
    document = models.FileField(upload_to='files/', verbose_name='Документ')

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class ServicePage(models.Model):
    seo = models.OneToOneField(Seo, on_delete=models.PROTECT, verbose_name='SEO-блок')

    class Meta:
        verbose_name = 'Страница наших услуг'


class AboutService(models.Model):
    page_id = models.ForeignKey(MainPage, on_delete=models.CASCADE, verbose_name='Страница наших услуг')
    image = models.ImageField(upload_to='gallery/', verbose_name='Изображение')
    name = models.CharField(max_length=64, verbose_name='Название услуги')
    description = models.TextField(verbose_name='Описание услуги')

    class Meta:
        verbose_name = 'Об услуге'
        verbose_name_plural = 'Об услугах'


class ContactPage(models.Model):
    header = models.CharField(max_length=64, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Краткий текст')
    url = models.URLField(verbose_name='Ссылка на коммерческий сайт')
    full_name = models.CharField(max_length=128, verbose_name='ФИО')
    location = models.CharField(max_length=128, verbose_name='Локация')
    address = models.CharField(max_length=128, verbose_name='Адрес')
    telephone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='E-mail')
    map = models.TextField(verbose_name='Код карты')
    seo = models.OneToOneField(Seo, on_delete=models.PROTECT, verbose_name='SEO-блок')

    class Meta:
        verbose_name = 'Контакты'