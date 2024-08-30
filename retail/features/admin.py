from django.contrib import admin
from django import forms

from retail.features.models import Feature, FeatureVersion
from retail.event_driven import eda_publisher
from retail.features.forms import FeatureForm


class FeatureVersionInlineForm(forms.ModelForm):
    class Meta:
        model = FeatureVersion
        fields = ["definition", "parameters", "version"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit: bool) -> FeatureVersion:
        feature_version: FeatureVersion = super().save(commit)
        feature = feature_version.feature
        if feature.feature_type == "FEATURE":
            for feature_function in feature.functions.all():
                function_version = feature_function.versions.order_by("created_on").last()

                for flow in function_version.definition["flows"]:
                    self.instance.definition["flows"].append(flow)

                for campaign in function_version.definition["campaigns"]:
                    self.instance.defintion["campaigns"].append(campaign)

                for trigger in function_version.definition["triggers"]:
                    self.instance.defintion["triggers"].append(trigger)

                for field in function_version.definition["fields"]:
                    self.instance.definition["fields"].append(field)

                for group in function_version.definition["groups"]:
                    self.instance.definition["groups"].append(group)

                for parameter in function_version.parameters:
                    self.instance.parameters.append(parameter)
            self.instance.save()

        flows = self.instance.definition["flows"]
        sectors = []
        for flow in flows:
            if len(flow["integrations"]["ticketers"]) > 0:
                for ticketer in flow["integrations"]["ticketers"]:
                    sectors.append(ticketer)

        sectors_base = []
        for sector in sectors:
            queues = []
            if "queues" in sector:
                for queue in sector["queues"]:
                    queues.append({
                        "name": queue["name"],
                    })
            sectors_base.append({
                "name": sector["name"],
                "tags": [""],
                "queues": queues
            })

        self.instance.sectors = sectors_base
        self.instance.save()
        return feature_version


class FeatureVersionInline(admin.StackedInline):
    model = FeatureVersion
    form = FeatureVersionInlineForm
    extra = 0


class FeatureAdmin(admin.ModelAdmin):
    search_fields = ["name", "uuid"]
    inlines = [FeatureVersionInline]
    form = FeatureForm

admin.site.register(Feature, FeatureAdmin)
