from functools import wraps

class Task(object):
    """
    Abstract base class for objects wishing to be picked up as Fabric tasks.

    Instances of subclasses will be treated as valid tasks when present in
    fabfiles loaded by the :doc:`fab </usage/fab>` tool.

    For details on how to implement and use `~fabric.tasks.Task` subclasses,
    please see the usage documentation on :ref:`new-style tasks
    <new-style-tasks>`.

    .. versionadded:: 1.1
    """
    name = 'undefined'
    use_task_objects = True

    # TODO: make it so that this wraps other decorators as expected

    def __init__(self):
        Task.register(self)

    def run(self):
        raise NotImplementedError

    @classmethod
    def _init_task_registry(cls):
        """ Create a task registry if one does not already exist. """
        if not hasattr(cls, "_registry"):
            cls._registry = dict()

    @classmethod
    def register(cls, task):
        """ Add a Task to the task registry. """
        cls._init_task_registry()
        cls._registry[task.name] = task

    @classmethod
    def unregister(cls, task):
        """ Remove a task from the task registry. """
        cls._init_task_registry()
        if task.name in cls._registry:
            del cls._registry[task.name]
       
    @classmethod
    def all(cls):
        """ Return all the tasks in the task registry. """
        cls._init_task_registry()
        return cls._registry.items()

    @classmethod
    def get_by_name(cls, name):
        """ Get a task from the registry by name. """
        cls._init_task_registry()
        return cls._registry[name]


class WrappedCallableTask(Task):
    """
    Wraps a given callable transparently, while marking it as a valid Task.

    Generally used via the `~fabric.decorators.task` decorator and not
    directly.

    .. versionadded:: 1.1
    """
    def __init__(self, callable):
        self.wrapped = callable
        self.__name__ = self.name = callable.__name__
        self.__doc__ = callable.__doc__
        super(WrappedCallableTask, self).__init__()

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)

    def __getattr__(self, k):
        return getattr(self.wrapped, k)
