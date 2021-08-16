import mimetypes
import os
import uuid

from django.conf import settings
from django.http.response import HttpResponse


class DownloadList:
    """ Преобразует queryset в string для последующего
    формирования отчета.

    Сейчас работает только с моделью IngredientsAmount, где должны быть
    поля ingredient и amount.

    Поддерживает вывод только в txt файл.
    """

    def __init__(self, queryset):
        self.queryset = queryset
        self.data = self._get_data_from_queryset()

    def _get_data_from_queryset(self):
        """Создается словарь с уникальными ингредиентами и суммой их
        количества.
        :return: dict(Ingredient: amount)
        """
        ingredients = dict()
        for items in self.queryset:
            for item in items:
                if ingredients.get(item.ingredient):
                    ingredients[item.ingredient] += item.amount
                else:
                    ingredients[item.ingredient] = item.amount
        return ingredients

    def make_txt_file(self):
        """Создает файл txt по пути MEDIA_ROOT и наполняет его
        из self.data.
        :return: tuple(filename(str), filepath(str), mime_type(str))
        """
        filename = str(uuid.uuid4()) + '.txt'
        filepath = os.path.join(settings.MEDIA_ROOT, filename)
        with open(filepath, 'w') as file:
            divided_line = f'\n{"<" * 20} FOODGRAM {">" * 20}\n'
            print(f'Список покупок для выбраных рецептов{divided_line}',
                  file=file)
            for index, (item, amount) in enumerate(self.data.items(), 1):
                print(f'{index}. {str(item.name).capitalize()} '
                      f'({item.measurement_unit}) — {int(amount)}', file=file)
            print(f'{divided_line}С любовью, команда FoodGram.',
                  file=file, end='')

        mime_type, _ = mimetypes.guess_type(filepath)
        return filename, filepath, mime_type

    def download_file(self):
        """Подгатавливается HttpResponse, context наполняется из ранее
        созданного файла. Передаются заголовки attachment.
        После формирования HttpResponse подготовленный файл удаляется.
        :return: HttpResponse
        """
        filename, path, mime_type = self.make_txt_file()
        response = HttpResponse(open(path).readlines(), content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        self._delete_file(path)
        return response

    def _delete_file(self, path):
        if os.path.isfile(path):
            os.remove(path)
