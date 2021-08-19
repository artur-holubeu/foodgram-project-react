import mimetypes
import os
import uuid

from django.conf import settings
from django.http.response import HttpResponse


class DownloadList:
    """ Преобразует queryset в string для последующего
    формирования отчета.

    Поддерживает вывод только в txt файл.
    """

    def __init__(self, queryset):
        self.queryset = queryset
        self.data = self._get_data_from_queryset()

    def _get_data_from_queryset(self) -> dict:
        """Создается словарь с уникальными ингредиентами и суммой их
        количества.
        :return: dict(name(dict(amount, unit)))
        """
        ingredients = {}
        for name, unit, amount in self.queryset:
            if all((name, unit, amount,)):
                if ingredients.get(name):
                    ingredients[name]['amount'] += amount
                else:
                    ingredients[name] = {'amount': amount, 'unit': unit}
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
            file.write(f'Список покупок для выбранных рецептов{divided_line}\n')
            for index, (name, payload) in enumerate(self.data.items(), 1):
                file.write(f'{index}. {name.capitalize()} ({payload["unit"]})'
                           f' — {int(payload["amount"])}\n')
            file.write(f'{divided_line}С любовью, команда FoodGram.')

        mime_type, _ = mimetypes.guess_type(filepath)
        return filename, filepath, mime_type

    def download_file(self):
        """Подготавливается HttpResponse, context наполняется из ранее
        созданного файла. Передаются заголовки attachment.
        После формирования HttpResponse подготовленный файл удаляется.
        :return: HttpResponse
        """
        filename, path, mime_type = self.make_txt_file()
        response = HttpResponse(open(path).readlines(), content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        self._delete_file(path)
        return response

    @staticmethod
    def _delete_file(path):
        if os.path.isfile(path):
            os.remove(path)
