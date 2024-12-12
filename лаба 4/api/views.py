# Импорт рендеринга шаблонов (не используется в данном коде)
from django.shortcuts import render

# Импорт базового класса для создания API представлений
from rest_framework.views import APIView

# Импорт класса для формирования JSON-ответов
from rest_framework.response import Response

# Импорт модели Currency для работы с валютами
from currency.models import Currency

# Импорт сериализатора для модели Currency
from .serializers import CurrencySerializer

# Импорт HTTP статусов для удобного обозначения статусов ответов
from rest_framework import status

# Импорт аутентификации на основе JWT токенов
from rest_framework_simplejwt.authentication import JWTAuthentication

# Импорт класса проверки аутентификации пользователя
from rest_framework.permissions import IsAuthenticated


# Класс для обработки операций с валютами
class CurrencyExchange(APIView):
    # Указываем, что доступ к этому API имеют только аутентифицированные пользователи
    permission_classes = [IsAuthenticated]

    # Указываем, что для аутентификации используется JWT токен
    authentication_classes = [JWTAuthentication]

    # Обработка GET-запроса
    def get(self, request):
        # Получаем все записи валют из базы данных
        currencies = Currency.objects.all()

        # Сериализуем данные из объектов модели Currency в JSON
        serializer = CurrencySerializer(currencies, many=True)

        # Если данные сериализации не пусты, возвращаем их с кодом 200
        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Если данные некорректны, возвращаем ошибки сериализации с кодом 400
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Обработка POST-запроса (для конвертации валюты из одной в другую)
    def post(self, request):
        # Получаем данные из тела запроса
        currencyFrom = request.data['currencyFrom']  # Код исходной валюты
        currencyTo = request.data['currencyTo']      # Код целевой валюты
        ammount = request.data['ammount']            # Сумма для конвертации

        # Преобразуем сумму в число с плавающей точкой
        try:
            ammount = float(ammount)
        except ValueError:
            # Если преобразование не удалось, возвращаем ошибку
            return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, что сумма положительная
        if ammount <= 0:
            return Response("Invalid data2", status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, существуют ли указанные валюты и корректный ли тип данных
        if not (
            Currency.objects.filter(CharCode=currencyFrom).exists() and
            Currency.objects.filter(CharCode=currencyTo).exists() and
            isinstance(ammount, (int, float))
        ):
            # Если одна из проверок не пройдена, возвращаем ошибку
            return Response("Invalid data3", status=status.HTTP_400_BAD_REQUEST)

        # Получаем объекты исходной и целевой валют из базы данных
        currencyFrom = Currency.objects.filter(CharCode=currencyFrom).first()
        currencyTo = Currency.objects.filter(CharCode=currencyTo).first()

        # Рассчитываем результат конвертации
        result = currencyFrom.exchange_to(ammount, currencyTo)

        # Возвращаем результат с кодом 200
        return Response(f"{result}", status=status.HTTP_200_OK)
