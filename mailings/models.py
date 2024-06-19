from django.conf import settings
from django.db import models
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """
    Модель клиента сервиса
    """
    email = models.EmailField(unique=True, verbose_name='Email', help_text='Введите адрес электронной почты')
    name = models.CharField(max_length=200, verbose_name='Имя',
                            help_text='Введите имя (по желанию ФИО)', **NULLABLE)
    comment = models.CharField(max_length=300, verbose_name='Комментарий',
                               help_text='Введите комментарий', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              verbose_name="Владелец", **NULLABLE)

    def __str__(self):
        return f'{self.email}  {self.name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    """
    Модель сообщения рассылки
    """
    title = models.CharField(max_length=150, verbose_name='Название', help_text='Введите название рассылки')
    content = models.CharField(max_length=300, verbose_name='Содержание', help_text='Введите содержание рассылки')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Владелец', on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f'{self.title} {self.content}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mail(models.Model):
    """
    Модель рассылки, содержит периодичность рассылки и статус
    """
    ONCE_HOUR = "Каждый час"
    DAILY = "Раз в день"
    WEEKLY = "Раз в неделю"
    MONTHLY = "Раз в месяц"

    PERIOD = [
        ("DAILY", "Раз в день"),
        ("WEEKLY", "Раз в неделю"),
        ("MONTHLY", "Раз в месяц"),
    ]

    CREATED = "Создана"
    STARTED = "Запущена"
    COMPLETED = "Завершена"

    STATUS = [
        ("CREATED", "Создана"),
        ("STARTED", "Запущена"),
        ("COMPLETED", "Завершена"),
    ]

    content = models.OneToOneField(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    clients = models.ManyToManyField(Client, verbose_name='Клиенты', related_name='client')
    start_time = models.DateTimeField(default=timezone.now, verbose_name='Начало отправки рассылки')
    end_time_last = models.DateTimeField(default=timezone.now, verbose_name='Последняя дата отправки рассылки',
                                         **NULLABLE)
    period = models.CharField(max_length=30, verbose_name='Периодичность', choices=PERIOD)
    status = models.CharField(max_length=30, verbose_name='Статус рассылки', choices=STATUS, default='CREATED')
    mail_active = models.BooleanField(verbose_name='Активность рассылки', default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.period} {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            (
                'change_status', 'Can change mailing status'
            )
        ]


class Log(models.Model):
    """
    Модель попытки рассылки
    """
    SUCCESS = "Успешно"
    FAILED = "Ошибка отправки"

    STATUS = [
        ("SUCCESS", "Успешно"),
        ("FAILED", "Ошибка отправки"),
    ]
    last_attempt = models.DateTimeField(verbose_name='Дата и время последней попытки', auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS, verbose_name="Cтатус попытки", default='CREATED')
    server_response = models.CharField(max_length=200, verbose_name="Ответ почтового сервера", **NULLABLE)
    mail = models.ForeignKey(Mail, verbose_name="Рассылка", on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Владелец', on_delete=models.SET_NULL, **NULLABLE)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name="клиент рассылки", **NULLABLE)

    def __str__(self):
        return f"{self.mail}, {self.last_attempt}, {self.status}, {self.server_response}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
