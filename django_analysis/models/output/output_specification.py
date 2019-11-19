from django.db import models
from django_analysis.models.managers.output_specification import (
    OutputSpecificationManager,
)


class OutputSpecification(models.Model):
    analysis = models.ForeignKey("django_analysis.Analysis", on_delete=models.CASCADE)
    base_output_definitions = models.ManyToManyField("django_analysis.OutputDefinition")

    objects = OutputSpecificationManager()

    def __str__(self) -> str:
        definitions = self.output_definitions.select_subclasses()
        formatted_definitions = "\n\t".join(
            [str(definition) for definition in definitions]
        )
        return f"\n[{self.analysis}]\n\t{formatted_definitions}\n"

    @property
    def output_definitions(self) -> models.QuerySet:
        return self.base_output_definitions.select_subclasses()