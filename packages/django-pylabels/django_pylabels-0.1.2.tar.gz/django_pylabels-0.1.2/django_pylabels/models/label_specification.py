from django.db import models
from django.utils import timezone


class LabelSpecification(models.Model):

    name = models.CharField(max_length=50, default="default", unique=True, blank=False)
    sheet_width = models.FloatField(default=210.0, blank=False)
    sheet_height = models.FloatField(default=297.0, blank=False)
    columns = models.IntegerField(default=2, blank=False)
    rows = models.IntegerField(default=6, blank=False)
    label_width = models.FloatField(default=96.0, blank=False)
    label_height = models.FloatField(default=42.0, blank=False)
    border = models.BooleanField(default=True, blank=False)
    row_gap = models.FloatField(default=None, null=True, blank=True)
    column_gap = models.FloatField(default=None, null=True, blank=True)
    top_margin = models.FloatField(default=21.0)
    left_margin = models.FloatField(default=8.0)
    right_margin = models.FloatField(default=8.0)
    bottom_margin = models.FloatField(default=22.0)
    left_padding = models.FloatField(default=2.0)
    right_padding = models.FloatField(default=2.0)
    top_padding = models.FloatField(default=2.0)
    bottom_padding = models.FloatField(default=2.0)
    corner_radius = models.IntegerField(default=0)
    padding_radius = models.IntegerField(default=0)
    # background_image = models.CharField
    # background_image_filename = models.CharField
    page_description = models.CharField(max_length=250, null=True, blank=True)
    layout_description = models.CharField(max_length=250, null=True, blank=True)
    label_description = models.CharField(max_length=250, null=True, blank=True)
    created = models.DateTimeField(null=True, editable=False)
    modified = models.DateTimeField(null=True, editable=False)

    def __str__(self):
        return self.name

    @property
    def as_dict(self) -> dict[str, float | int | None]:
        attrs = [
            "sheet_width",
            "sheet_height",
            "columns",
            "rows",
            "label_width",
            "label_height",
            "corner_radius",
            "row_gap",
            "column_gap",
            "top_margin",
            "left_margin",
            "right_margin",
            "bottom_margin",
            "left_padding",
            "right_padding",
            "top_padding",
            "bottom_padding",
        ]
        return {k: getattr(self, k) for k in attrs}

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        self.page_description = f"{self.sheet_width} x {self.sheet_height}"
        self.layout_description = f"{self.rows} rows x {self.columns} cols"
        self.label_description = f"{self.label_width} x {self.label_height}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Label Sheet Specification"
        verbose_name_plural = "Label Sheet Specifications"
