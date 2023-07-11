# Generated by Django 4.2.2 on 2023-07-05 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='comment',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='movie.movie'),
        ),
        migrations.AddField(
            model_name='movie',
            name='tag',
            field=models.ManyToManyField(blank=True, to='movie.tag'),
        ),
    ]
