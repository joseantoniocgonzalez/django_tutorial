from django.db import migrations, models
from django.utils import timezone

def insert_initial_data(apps, schema_editor):
    Question = apps.get_model("polls", "Question")
    Choice = apps.get_model("polls", "Choice")

    q1 = Question.objects.create(
        question_text="¿Cuál es el río que pasa por Cardiff?",
        pub_date=timezone.now()
    )
    Choice.objects.create(question=q1, choice_text="Taff", votes=0)
    Choice.objects.create(question=q1, choice_text="Severn", votes=0)
    Choice.objects.create(question=q1, choice_text="Usk", votes=0)

    q2 = Question.objects.create(
        question_text="¿Cuál es el símbolo de Gales?",
        pub_date=timezone.now()
    )
    Choice.objects.create(question=q2, choice_text="Dragón rojo", votes=0)
    Choice.objects.create(question=q2, choice_text="Puerro", votes=0)
    Choice.objects.create(question=q2, choice_text="Trébol", votes=0)

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=models.CASCADE, to='polls.Question')),
            ],
        ),
        migrations.RunPython(insert_initial_data),
    ]
