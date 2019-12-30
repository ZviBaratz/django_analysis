# Generated by Django 2.2.8 on 2019-12-30 08:38

from django.conf import settings
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('title', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Analyses',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='AnalysisVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('run_method_key', models.CharField(default='run', max_length=100)),
                ('nested_results_attribute', models.CharField(blank=True, max_length=100, null=True)),
                ('analysis', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='version_set', to='django_analyses.Analysis')),
            ],
            options={
                'ordering': ('-title',),
            },
        ),
        migrations.CreateModel(
            name='Input',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='InputDefinition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50)),
                ('required', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_configuration', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('key',),
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('configuration', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('analysis_version', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='django_analyses.AnalysisVersion')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OutputDefinition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pipeline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BooleanInputDefinition',
            fields=[
                ('inputdefinition_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_analyses.InputDefinition')),
                ('default', models.BooleanField(blank=True, null=True)),
            ],
            bases=('django_analyses.inputdefinition',),
        ),
        migrations.CreateModel(
            name='FileInputDefinition',
            fields=[
                ('inputdefinition_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_analyses.InputDefinition')),
            ],
            bases=('django_analyses.inputdefinition',),
        ),
        migrations.CreateModel(
            name='FileOutputDefinition',
            fields=[
                ('outputdefinition_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_analyses.OutputDefinition')),
            ],
            bases=('django_analyses.outputdefinition',),
        ),
        migrations.CreateModel(
            name='ListInputDefinition',
            fields=[
                ('inputdefinition_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_analyses.InputDefinition')),
                ('element_type', models.CharField(choices=[('STR', 'String'), ('INT', 'Integer'), ('FLT', 'Float'), ('BLN', 'Boolean')], max_length=3)),
                ('min_length', models.PositiveIntegerField(blank=True, null=True)),
                ('max_length', models.PositiveIntegerField(blank=True, null=True)),
                ('default', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
            bases=('django_analyses.inputdefinition',),
        ),
        migrations.CreateModel(
            name='NumberInput',
            fields=[
                ('input_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_analyses.Input')),
            ],
            bases=('django_analyses.input',),
        ),
        migrations.CreateModel(
            name='NumberInputDefinition',
            fields=[
                ('inputdefinition_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_analyses.InputDefinition')),
            ],
            bases=('django_analyses.inputdefinition',),
        ),
        migrations.CreateModel(
            name='StringInputDefinition',
            fields=[
                ('inputdefinition_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_analyses.InputDefinition')),
                ('min_length', models.IntegerField(blank=True, null=True)),
                ('max_length', models.IntegerField(blank=True, null=True)),
                ('default', models.CharField(blank=True, max_length=500, null=True)),
                ('choices', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255, null=True), blank=True, null=True, size=None)),
                ('is_output_path', models.BooleanField(default=False)),
            ],
            bases=('django_analyses.inputdefinition',),
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('analysis_version', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='django_analyses.AnalysisVersion')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Pipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_destination_port', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='django_analyses.InputDefinition')),
                ('base_source_port', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='django_analyses.OutputDefinition')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pipe_destination_set', to='django_analyses.Node')),
                ('pipeline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_analyses.Pipeline')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pipe_source_set', to='django_analyses.Node')),
            ],
        ),
        migrations.CreateModel(
            name='OutputSpecification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('analysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_analyses.Analysis')),
                ('base_output_definitions', models.ManyToManyField(to='django_analyses.OutputDefinition')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Output',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base_output_set', to='django_analyses.Run')),
            ],
        ),
        migrations.CreateModel(
            name='InputSpecification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('analysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_analyses.Analysis')),
                ('base_input_definitions', models.ManyToManyField(to='django_analyses.InputDefinition')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='input',
            name='run',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base_input_set', to='django_analyses.Run'),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='django_analyses.Category')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ('title',),
            },
        ),
        migrations.AddField(
            model_name='analysisversion',
            name='input_specification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='analysis_version_set', to='django_analyses.InputSpecification'),
        ),
        migrations.AddField(
            model_name='analysisversion',
            name='output_specification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='analysis_version_set', to='django_analyses.OutputSpecification'),
        ),
        migrations.AddField(
            model_name='analysis',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_analyses.Category'),
        ),
        migrations.CreateModel(
            name='FloatInputDefinition',
            fields=[
                ('numberinputdefinition_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_analyses.NumberInputDefinition')),
                ('min_value', models.FloatField(blank=True, null=True)),
                ('max_value', models.FloatField(blank=True, null=True)),
                ('default', models.FloatField(blank=True, null=True)),
            ],
            bases=('django_analyses.numberinputdefinition',),
        ),
        migrations.CreateModel(
            name='IntegerInputDefinition',
            fields=[
                ('numberinputdefinition_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_analyses.NumberInputDefinition')),
                ('min_value', models.IntegerField(blank=True, null=True)),
                ('max_value', models.IntegerField(blank=True, null=True)),
                ('default', models.IntegerField(blank=True, null=True)),
            ],
            bases=('django_analyses.numberinputdefinition',),
        ),
        migrations.CreateModel(
            name='StringInput',
            fields=[
                ('input_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_analyses.Input')),
                ('value', models.CharField(max_length=1000)),
                ('definition', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='input_set', to='django_analyses.StringInputDefinition')),
            ],
            bases=('django_analyses.input',),
        ),
        migrations.CreateModel(
            name='ListInput',
            fields=[
                ('input_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_analyses.Input')),
                ('value', django.contrib.postgres.fields.jsonb.JSONField()),
                ('definition', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='input_set', to='django_analyses.ListInputDefinition')),
            ],
            bases=('django_analyses.input',),
        ),
        migrations.CreateModel(
            name='FileOutput',
            fields=[
                ('output_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_analyses.Output')),
                ('value', models.FilePathField(blank=True, null=True, verbose_name='/home/zvi/Projects/labbing/pylabber/media')),
                ('definition', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='output_set', to='django_analyses.FileOutputDefinition')),
            ],
            bases=('django_analyses.output',),
        ),
        migrations.CreateModel(
            name='FileInput',
            fields=[
                ('input_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_analyses.Input')),
                ('value', models.FilePathField(verbose_name='/home/zvi/Projects/labbing/pylabber/media')),
                ('definition', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='input_set', to='django_analyses.FileInputDefinition')),
            ],
            bases=('django_analyses.input',),
        ),
        migrations.CreateModel(
            name='BooleanInput',
            fields=[
                ('input_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_analyses.Input')),
                ('value', models.BooleanField()),
                ('definition', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='input_set', to='django_analyses.BooleanInputDefinition')),
            ],
            bases=('django_analyses.input',),
        ),
        migrations.AlterUniqueTogether(
            name='analysisversion',
            unique_together={('analysis', 'title')},
        ),
        migrations.CreateModel(
            name='IntegerInput',
            fields=[
                ('numberinput_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_analyses.NumberInput')),
                ('value', models.IntegerField()),
                ('definition', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='input_set', to='django_analyses.IntegerInputDefinition')),
            ],
            bases=('django_analyses.numberinput',),
        ),
        migrations.CreateModel(
            name='FloatInput',
            fields=[
                ('numberinput_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_analyses.NumberInput')),
                ('value', models.FloatField()),
                ('definition', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='input_set', to='django_analyses.FloatInputDefinition')),
            ],
            bases=('django_analyses.numberinput',),
        ),
    ]
