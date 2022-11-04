import requests

import config


def send_error(modul_name='?', exception='?', traceback='?'):
    method = config.tb_url + config.TELEGA_TOKEN_VALSTANBOT + "/sendMessage"

    config.tb_params['text'] = f'Ошибка в NagradaRestAPI\n' \
                               f'МОДУЛЬ:\n{modul_name}\n' \
                               f'АШИПКА:\n{exception}\n' \
                               f'ПРИЧИНА:\n{traceback}\n'

    requests.post(method, data=config.tb_params)


if __name__ == '__main__':
    send_error("Запущен файл send_error вручную.")
