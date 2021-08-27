from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    handlers = {
        'ValidationError': _handle_generic_error,
    }
    response = exception_handler(exc, context)
    exception_class = exc.__class__.__name__
    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return response


def _handle_generic_error(exc, context, response):
    if 'RecipeView' in str(context['view']) and exc.status_code == 400:
        return _override_recipes_errors(exc, response)
    return response


def _override_recipes_errors(exc, response):
    fields = {
        'ingredients': 'Ингредиенты',
        'tags': 'Ярлыки',
        'name': 'Название',
        'text': 'Описание',
        'cooking_time': 'Время приготовления',
        'image': 'Изображение',
    }
    for field, text in fields.items():
        if exc.detail.get(field):
            if field == 'ingredients':
                errors_list = []
                for x in exc.detail.get('ingredients'):
                    for key, item in x.items():
                        errors_list.append(f'{text}: {item[0]}')
                response.data['ingredients'] = errors_list
                continue
            if field == 'image':
                exc.detail.get('image')[0] = (
                    'Пожалуйста, загрузите действительное изображение.'
                )

            exc.detail.get(field)[0] = f'{text}: {exc.detail.get(field)[0]}'

    return response
