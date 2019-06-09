from copy import deepcopy
from locust import HttpLocust, TaskSet, task


class TaskBuilder:

    path = None
    
    def __init__(self, path=None):
        self.path = path

    @classmethod
    def compile_tasks(klass, domain):
        response = {}

        for item in [{'path':'/', 'weight':2}, {'path':'/about', 'weight': 4}]:
            handler = TaskBuilder(path=item['path'])
            response.update({
                handler.task_template: item['weight']
            })
        return response
    
    def task_template(self, caller):
        caller.client.get(self.path)


class WebsiteTasks(TaskSet):

    def __init__(self, *args, **kwargs):
        super(WebsiteTasks, self).__init__(*args, **kwargs)
        for handler, weight in TaskBuilder.compile_tasks(self.client.base_url).items():
            [self.tasks.append(handler) for i in range(weight)]


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 5000
    max_wait = 30000 