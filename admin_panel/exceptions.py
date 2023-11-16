from rest_framework.views import exception_handler
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            response.data = {
                'message': 'Tizimga kirishda xatolik',
                'code': '401'
            }
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            response.data = {
                'message': "Huquq yo'q!",
                'code': '403'
            }
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            response.data = {
                'message': 'Bunday malumot mavjud emas!',
                'code': '404'
            }
        elif response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            response.data = {
                'message': 'Tizimda xatolik!',
                'code': '500'
            }
        elif response.status_code == status.HTTP_201_CREATED:
            response.data = {
                'message': 'Muvaffaqiyatli yaratildi!',
                'code': '201'
            }
        # elif response.status_code == status.HTTP_400_BAD_REQUEST:
        #     response.data = {
        #         'message': 'Xatolik yuz berdi!',
        #         'code': '400'
        #     }

    return response
