# Generated by Django 4.1.2 on 2022-10-23 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('userId', models.URLField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('url', models.CharField(blank=True, max_length=200)),
                ('host', models.CharField(blank=True, max_length=200)),
                ('displayName', models.CharField(max_length=200)),
                ('github', models.CharField(blank=True, max_length=200)),
                ('profileImage', models.URLField(blank=True, null=True)),
                ('followers', models.ManyToManyField(to='frontend.author')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment', models.CharField(max_length=500)),
                ('id', models.URLField(blank=True, primary_key=True, serialize=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.author')),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='frontend.author')),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to='frontend.author')),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('api_domain', models.URLField(primary_key=True, serialize=False)),
                ('api_prefix', models.CharField(blank=True, max_length=200, null=True)),
                ('username', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.URLField(blank=True, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=50)),
                ('source', models.URLField(blank=True)),
                ('origin', models.URLField(blank=True)),
                ('description', models.CharField(blank=True, max_length=50)),
                ('content_type', models.CharField(blank=True, max_length=255, null=True)),
                ('content', models.CharField(blank=True, max_length=5000, null=True)),
                ('image_id', models.URLField(blank=True)),
                ('categories', models.CharField(blank=True, max_length=255, null=True)),
                ('count', models.IntegerField(default=0)),
                ('comments', models.URLField(blank=True)),
                ('comments_src', models.URLField(blank=True, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.author')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object', models.URLField(blank=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.author')),
            ],
        ),
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='author_inbox', to='frontend.author')),
                ('comments', models.ManyToManyField(to='frontend.comment')),
                ('follows', models.ManyToManyField(to='frontend.follow')),
                ('likes', models.ManyToManyField(to='frontend.like')),
                ('posts', models.ManyToManyField(related_name='inbox_posts', to='frontend.post')),
            ],
        ),
        migrations.CreateModel(
            name='FollowRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='Follow', max_length=200)),
                ('summary', models.TextField()),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_request_sender', to='frontend.author')),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_request_receiver', to='frontend.author')),
            ],
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='followers', max_length=200)),
                ('items', models.ManyToManyField(blank=True, related_name='items', to='frontend.author')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='frontend.author')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.post'),
        ),
    ]