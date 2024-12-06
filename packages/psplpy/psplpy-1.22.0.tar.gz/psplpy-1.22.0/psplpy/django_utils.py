import re
import django
from django.conf import settings
from django.db import models, connections
from psplpy.image_det import TxtProc
from pathlib import Path


class DbBackend:
    SQLITE3 = 'django.db.backends.sqlite3'
    POSTGRESQL = 'django.db.backends.postgresql'
    MYSQL = 'django.db.backends.mysql'


class Database:
    def __init__(self, engine: str = DbBackend.SQLITE3, name=None, user=None, password=None,
                 host='localhost', port=None, app_label: str = '', **django_settings):
        databases = {
            'default': {
                'ENGINE': engine,
                'NAME': name,
                'USER': user,
                'PASSWORD': password,
                'HOST': host,
                'PORT': port,
                'APP_LABEL': app_label,
            }
        }

        # Update the settings with the custom DATABASES dictionary
        settings_dict = {'DATABASES': databases}
        settings_dict.update(django_settings)
        settings.configure(**settings_dict)
        # Initialize Django
        django.setup()

        # Create the custom base model
        class CustomBaseModel(models.Model):
            class Meta:
                app_label = databases['default']['APP_LABEL']
                abstract = True

            @classmethod
            def init(cls, new_name=None) -> None:
                Database.change_table_name(cls, new_name)
                Database.create_table(cls)
                Database.update_table(cls)

        self.Model = CustomBaseModel

    @staticmethod
    def change_table_name(model, new_name=None) -> None:
        if new_name is None:
            new_name = TxtProc.camel_to_snake(model.__name__)
        model._meta.db_table = new_name

    @staticmethod
    # Create a table if it doesn't exist
    def create_table(model) -> None:
        with connections['default'].schema_editor() as schema_editor:
            if model._meta.db_table not in connections['default'].introspection.table_names():
                schema_editor.create_model(model)

    @staticmethod
    # Update table if you added fields (doesn't drop fields as far as i know, which i was too afraid to implement)
    def update_table(model) -> None:
        with connections['default'].schema_editor() as schema_editor:
            if model._meta.db_table not in connections['default'].introspection.table_names():
                raise ValueError(f'Table "{model._meta.db_table}" not found.')
            else:
                # Get the database columns
                database_columns = connections['default'].introspection.get_table_description(
                    connections['default'].cursor(), model._meta.db_table)
                database_column_names = [column.name for column in database_columns]
                # Check if each field in the model exists in the database table
                for field in model._meta.fields:
                    if field.column not in database_column_names:
                        # Add the new column to the table
                        schema_editor.add_field(model, field)


class DjangoInit:
    def __init__(self, project_dir: str | Path = None, database: str = None):
        self.project_dir = Path(project_dir) if project_dir else Path(__file__).parent
        self.database = database
        self.manage_py_path = self._find_manage_py()
        self.project_name = self._extract_project_name()
        self.settings_py_path = self.project_dir / self.project_name / 'settings.py'

    def _find_manage_py(self) -> Path:
        manage_py_path = self.project_dir / 'manage.py'
        if manage_py_path.exists():
            return manage_py_path
        raise FileNotFoundError(f'manage.py not found at {manage_py_path}')

    def _extract_project_name(self) -> str:
        content = self.manage_py_path.read_text(encoding='utf-8')
        match = re.search(r"os\.environ\.setdefault\('DJANGO_SETTINGS_MODULE', '([^']+)'\)", content)
        if match:
            return match.group(1).split('.')[0]
        raise ValueError("Cannot extract project name from manage.py")

    def init(self) -> None:
        settings_str = self.settings_py_path.read_text(encoding='utf-8')
        # make global templates dir
        templates_dir = self.project_dir / 'templates'
        templates_dir.mkdir(exist_ok=True)
        settings_str = settings_str.replace("'DIRS': [],", "'DIRS': [BASE_DIR / 'templates'],")
        # modify allowed hosts
        settings_str = settings_str.replace("ALLOWED_HOSTS = []", "ALLOWED_HOSTS = ['*']")
        # set database
        if self.database and self.database != DbBackend.SQLITE3:
            db_setting = f"""DATABASES = {{
    'default': {{
        'ENGINE': '{self.database}',
        'NAME': get_env("DB_NAME"),
        'USER': get_env("DB_USER"),
        'PASSWORD': get_env("DB_PASSWORD"),
        'HOST': get_env("DB_HOST"),
        'PORT': get_env("DB_PORT"),
    }}
}}"""
            old = """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""
            settings_str = settings_str.replace(old, db_setting)
            old = "from pathlib import Path\n\n# Build paths inside the project like this: BASE_DIR / 'subdir'."
            new = ('from pathlib import Path\n'
                   'from psplpy.other_utils import get_env\n'
                   'get_env.env_file = Path(__file__).resolve().parent.parent.parent / ".env"\n\n'
                   "# Build paths inside the project like this: BASE_DIR / 'subdir'.")
            settings_str = settings_str.replace(old, new)
        # write settings
        self.settings_py_path.write_text(settings_str, encoding='utf-8')
