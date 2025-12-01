from django.db import migrations

def add_inheritance(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS type_obj (
                id serial PRIMARY KEY,
                name varchar(255) UNIQUE NOT NULL
            );
        """)

        commands = [
            "ALTER TABLE status_obj INHERIT type_obj;",
            "ALTER TABLE event_types_obj INHERIT type_obj;",
            "ALTER TABLE ticket_types_obj INHERIT type_obj;",
            "ALTER TABLE seat_types_obj INHERIT type_obj;",
            "ALTER TABLE user_roles_obj INHERIT type_obj;",
            "ALTER TABLE discounts_obj INHERIT type_obj;",
        ]
        for cmd in commands:
            cursor.execute(cmd)

def remove_inheritance(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        commands = [
            "ALTER TABLE status_obj NO INHERIT type_obj;",
            "ALTER TABLE event_types_obj NO INHERIT type_obj;",
            "ALTER TABLE ticket_types_obj NO INHERIT type_obj;",
            "ALTER TABLE seat_types_obj NO INHERIT type_obj;",
            "ALTER TABLE user_roles_obj NO INHERIT type_obj;",
            "ALTER TABLE discounts_obj NO INHERIT type_obj;",
        ]
        for cmd in commands:
            cursor.execute(cmd)

class Migration(migrations.Migration):
    dependencies = [
        ('objective_relational', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_inheritance, reverse_code=remove_inheritance),
    ]