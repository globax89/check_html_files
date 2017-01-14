# coding: utf-8
import Queue
import threading
import requests

# Сформировать очередь урлов для загрузки проверки html файла в последовательность


class VerifyHtml(threading.Thread):
    """Потоковая проверка html файлов"""

    def __init__(self, queue):
            threading.Thread.__init__(self)
            self.queue = queue

    def run(self):
        while True:
            # Получить урлы из очереди
            url = self.queue.get()
            self.check_html_file(url)

            # Послать сигнал в очередь, что задача завершена
            self.queue.task_done()

    def check_html_file(self, url):
        # Обработать исключение
        try:
            r = requests.get(url)
            status = r.status_code
        except Exception as err:
            print({"status_code": -1, "err": err, "url": url})
        else:
            print({"status_code": status, "url": url, "content": r.content})


class AsyncDownLoad():
    """Породить потоки и загрузить очередь урлов"""

    def __init__(self, download_list, thread_count=5):
        self.thread_count = thread_count
        self.download_list = download_list

    # Начало загрузки потоков и заполнение очереди урлами
    def get_pages(self):
        queue = Queue.Queue()

        # Создать пул потоков и отдать их очереди
        for i in range(self.thread_count):
            t = VerifyHtml(queue)
            t.setDaemon(True)
            t.start()

        # Загрузить очередь
        for url in self.download_list:
            queue.put(url)

        # Ждать очередь
        queue.join()
        return


if __name__ == "__main__":

    check_test_list = ["http://globaxnet.ru/csgo/files/1542.html",
                        "http://globaxnet.ru/csgo/files/1543.html",
                        "http://globaxnet.ru/csgo/files/1544.html",
                        "http://globaxnet.ru/csgo/files/1545.html",
                        "http://globaxnet.ru/csgo/files/1548.html",
                        "http://globaxnet.ru/csgo/files/1547.html",
                        "html://badurl!!",
                        "html://badurl!!33",
                        "html://badurl!!tey@",
                        "http://globaxnet.ru/csgo/files/1549.html"]

    check_html_file = AsyncDownLoad(check_test_list, 3)
    check_html_file.get_pages()
