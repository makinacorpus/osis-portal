import requests
from django.conf import settings

from continuing_education.views.api import get_personal_token
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, BaseRenderer
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, BaseRenderer
from typing import List
from django.http import HttpResponse


def get_list_from_osis(url, **kwargs):
    header_to_get = {'Authorization': 'Token ' + settings.OSIS_PORTAL_TOKEN}
    response = requests.get(
        url=url,
        headers=header_to_get,
        params=kwargs,
    )
    data = response.json()
    return data


def get_country_list_from_osis(**kwargs):
    return get_list_from_osis(settings.URL_COUNTRY_API, **kwargs)


def get_training_list_from_osis(**kwargs):
    return get_list_from_osis(settings.URL_TRAINING_API, **kwargs)


@renderer_classes((BaseRenderer,))
def get_data_from_osis(request, luy, custom_path, content_type):
    list_learning_unit_id = luy.pk
    list_learning_unit_id = 559966

    token = get_personal_token(request)
    url = "{}/{}/{}/{}".format(settings.OSIS_BASE_API, custom_path, token, list_learning_unit_id)
    response = requests.get(
        url=url,
        headers={'Authorization': 'Token ' + token} if request.user.is_authenticated
        else REQUEST_HEADER
    )

    url_when_error_occured = reverse('students_list')

    if response.status_code == status.HTTP_404_NOT_FOUND:
        raise Http404
    elif response.status_code == 309:
        messages.add_message(
            request,
            messages.INFO,
            _("Impossible to create file, the learning unit doesn't exists"),
            "alert-info"
        )
        return url_when_error_occured
    elif response.status_code == status.HTTP_403_FORBIDDEN:
        raise PermissionDenied(response.json()['detail'] if response.content else '')
    elif response.status_code != 200:
        messages.add_message(
            request,
            messages.INFO,
            _("Error occurred while creating the export file"),
            "alert-info"
        )
        return url_when_error_occured

    number_session = "comment_l_avoir"
    if content_type == 'xls':
        content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        file_extension = 'xlsx'
    else:
        content_type = "application/pdf"
        file_extension = 'pdf'
    filename = "session_%s_%s_%s.%s" % (str(luy.academic_year.year), number_session, luy.acronym, file_extension)

    response = HttpResponse(response, content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response
