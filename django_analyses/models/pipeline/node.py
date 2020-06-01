from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from django_analyses.models.run import Run
from django_extensions.db.models import TimeStampedModel

User = get_user_model()


class Node(TimeStampedModel):
    analysis_version = models.ForeignKey(
        "django_analyses.AnalysisVersion", on_delete=models.PROTECT
    )
    configuration = JSONField(default=dict)

    class Meta:
        ordering = ("-created",)
        unique_together = "analysis_version", "configuration"

    def __str__(self) -> str:
        version = self.analysis_version
        config = self.configuration
        return f"\nNode #{self.id}\n{version}\nConfiguration: [{config}]\n"

    def save(self, *args, **kwargs):
        self.validate()
        super().save(*args, **kwargs)

    def get_configuration(self) -> dict:
        """
        Undo any changes made to the node's configuration for serialization
        before passing them on to the interface.

        Returns
        -------
        :obj:`dict`
            Node's analysis version configuration
        """

        configuration = {}
        for key, value in self.configuration.items():
            definition = self.analysis_version.input_definitions.get(key=key)
            value_field = definition.input_class._meta.get_field("value")
            is_foreign_key = isinstance(value_field, models.ForeignKey)
            if is_foreign_key:
                configuration[key] = value_field.related_model.objects.get(id=value)
            else:
                configuration[key] = value
        return configuration

    def validate(self) -> None:
        if self.configuration:
            self.analysis_version.input_specification.validate_keys(
                **self.configuration
            )

    def get_full_configuration(self, inputs: dict) -> dict:
        defaults = self.analysis_version.input_specification.default_configuration
        node_configuration = defaults.copy()
        node_configuration.update(self.get_configuration())
        node_configuration.update(inputs)
        return node_configuration

    def run(self, inputs: dict, user: User = None) -> Run:
        full_configuration = self.get_full_configuration(inputs)
        return Run.objects.get_or_execute(
            self.analysis_version, user=user, **full_configuration
        )

    def get_required_nodes(self) -> models.QuerySet:
        node_ids = self.pipe_destination_set.values_list("source", flat=True)
        return Node.objects.filter(id__in=list(node_ids))

    def get_requiring_nodes(self) -> models.QuerySet:
        node_ids = self.pipe_source_set.values_list("destination", flat=True)
        return Node.objects.filter(id__in=list(node_ids))

    def check_configuration_sameness(self, key: str, value) -> bool:
        is_same = value == self.configuration.get(key)
        input_definition = self.analysis_version.input_definitions.get(key=key)
        is_default = (
            value == input_definition.default and self.configuration.get(key) is None
        )
        not_configuration = input_definition.is_configuration is False
        return is_same or is_default or not_configuration

    def check_run_configuration_sameness(self, run: Run) -> bool:
        return all(
            [
                self.check_configuration_sameness(key, value)
                for key, value in run.input_configuration.items()
            ]
        )

    def get_run_set(self) -> models.QuerySet:
        all_runs = Run.objects.filter(analysis_version=self.analysis_version)
        runs = [run for run in all_runs if self.check_run_configuration_sameness(run)]
        run_ids = [run.id for run in runs]
        return Run.objects.filter(id__in=run_ids)

    @property
    def required_nodes(self) -> models.QuerySet:
        return self.get_required_nodes() or None

    @property
    def requiring_nodes(self) -> models.QuerySet:
        return self.get_requiring_nodes() or None

    @property
    def run_set(self) -> models.QuerySet:
        return self.get_run_set()
