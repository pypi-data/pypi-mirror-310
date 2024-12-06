===========
task-jogger
===========

More affectionately known as ``jogger``.

``jogger`` is a simple Python-based command line tool that isn't quite a fully-fledged task *runner*. In addition to supporting arbitrary tasks, run either directly on the command line or as Python scripts, it ships with some common, useful, Django-aware tasks that can adapt their behaviour based on which packages are available in the system.

Full documentation at: https://task-jogger.readthedocs.io/

Installation
============

Install the latest stable version from PyPI::

    pip install task-jogger


Quick start
===========

1. Create ``jog.py``
--------------------

The ``jog.py`` file, created in the project root directory, stores the tasks defined for the project. It is a regular Python module, the only requirement being that it defines a ``tasks`` variable as a dictionary.

2. Define ``tasks``
-------------------

Keys in the ``jog.py`` file's ``tasks`` dictionary form each task's name, and values describe the tasks themselves. At their simplest, a task can be a string defining a command to execute on the command line:

.. code-block:: python

    # jog.py
    tasks = {
        'hello': 'echo "Hello, World!"',
        'test': 'coverage run python manage.py test'
    }

Alternatively, a task can be a Python function that *returns* a command to execute on the command line. This can be useful if the command is more complex to construct or depends on dynamic values:

.. code-block:: python

    # jog.py
    def run_tests(settings, stdout, stderr):
        """
        Run the Django test suite, with coverage.py if installed.
        """

        try:
            import coverage
        except ImportError:
            stdout.write('Warning: coverage.py not installed.', style='warning')
            return 'python manage.py test'
        else:
            return 'coverage run python manage.py test'

    tasks = {
        'test': run_tests
    }

Finally, particularly complex tasks can be defined as classes. Such tasks can define their own custom arguments:

.. code-block:: python

    # jog.py
    from jogger.tasks import Task


    class TestTask(Task):

        help = 'Run the Django test suite, with coverage.py if installed.'

        def add_arguments(self, parser):

            parser.add_argument(
                '-q', '--quick',
                action='store_true',
                help=(
                    'Run a "quick" variant of the task: no coverage analysis and '
                    'running tests in parallel.'
                )
            )

        def handle(self, *args, **options):

            command = 'python manage.py test'

            if options['quick']:
                command = f'{command} --parallel'
            else:
                try:
                    import coverage
                except ImportError:
                    self.stdout.write('Warning: coverage.py not installed.', style='warning')
                else:
                    command = f'coverage run {command}'

            self.cli(command)

    tasks = {
        'test': TestTask
    }

3. Run ``jog``
--------------

The ``jog`` command is the interface to the tasks defined in ``jog.py``.

Given the name of a task, ``jog`` will run that task::

    $ jog test

If the task accepts arguments, they can also be provided::

    $ jog test --quick

Executed with no arguments, ``jog`` will display a list of all available tasks. Tasks defined as functions or classes can define a description to be displayed in this listing. Tasks defined as strings simply display the command they will run. The following shows the output of a ``jog.py`` file containing a mixture of string-based, function-based, and class-based tasks::

    $ jog
    Available tasks:
    string: echo "Hello, World!"
    function: A task defined as a function.
    class: A task defined as a class.
        See "jog class --help" for usage details
