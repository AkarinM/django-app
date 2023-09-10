from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def upload_file(request: HttpRequest) -> HttpResponse:
    """
    Load files from form
    :param request: request
    """
    from django.core.files.storage import FileSystemStorage

    context = {
        'finish': '',
        'error': '',
    }
    # if request.method == 'POST' and request.FILES['file']:
    if request.method == 'POST':
        file_to_save = request.FILES.get('file')
        if file_to_save:
            if 1 < file_to_save.size <= 1048576:  #больше 1байта и до 1мб включительно
                fs = FileSystemStorage()
                file_saved = fs.save(file_to_save.name, file_to_save)
                context['finish'] = f'File {file_to_save.name!r} is upload and save with name {file_saved!r} '
            else:
                context['error'] = 'Размер файла больше 1б и меньше 30б!'
        else:
            context['error'] = 'Не выбран файл для загрузки!'



    return render(request, 'requestdataapp/uploadfile.html', context=context)
