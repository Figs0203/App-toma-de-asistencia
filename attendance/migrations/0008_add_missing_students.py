from django.db import migrations
import unicodedata


def normalize_text(text):
    """Normaliza texto quitando acentos para ordenamiento."""
    if not text:
        return ''
    normalized = unicodedata.normalize('NFD', text)
    return ''.join(c for c in normalized if unicodedata.category(c) != 'Mn').lower()


def add_missing_students(apps, schema_editor):
    """Añadir los 3 estudiantes faltantes."""
    Student = apps.get_model('attendance', 'Student')
    
    new_students = [
        ("Juan Manuel", "Flórez Robledo"),
        ("Alexandra", "Hurtado David"),
        ("Isabella", "Idárraga Botero"),
    ]
    
    for first_name, last_name in new_students:
        Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=None,  # No se proporcionó correo
            is_active=True,
            last_name_normalized=normalize_text(last_name)
        )


def remove_missing_students(apps, schema_editor):
    """Eliminar los estudiantes añadidos."""
    Student = apps.get_model('attendance', 'Student')
    students_to_remove = [
        ("Juan Manuel", "Flórez Robledo"),
        ("Alexandra", "Hurtado David"),
        ("Isabella", "Idárraga Botero"),
    ]
    for first, last in students_to_remove:
        Student.objects.filter(first_name=first, last_name=last).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0007_alter_student_options_student_last_name_normalized'),
    ]

    operations = [
        migrations.RunPython(add_missing_students, remove_missing_students),
    ]
