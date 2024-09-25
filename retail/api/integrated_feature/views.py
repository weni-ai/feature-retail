from django.contrib.auth.models import User

from rest_framework import views, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from retail.features.models import Feature, IntegratedFeature
from retail.features.integrated_feature_eda import IntegratedFeatureEDA
from retail.projects.models import Project

class IntegratedFeatureView(views.APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        feature = Feature.objects.get(uuid=kwargs["feature_uuid"])
        try:
            project = Project.objects.get(uuid=request.data["project_uuid"])
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": f"Project with uuid equals {request.data['project_uuid' ]} does not exists!"})

        user, _ = User.objects.get_or_create(email=request.user.email)
        feature_version = feature.last_version
        
        integrated_feature = IntegratedFeature.objects.create(
            project=project,
            feature=feature,
            feature_version=feature_version,
            user=user
        )

        sectors_data = []
        integrated_feature.sectors = []
        if feature_version.sectors != None:
            for sector in feature_version.sectors:
                for r_sector in request.data.get("sectors", []):
                    if r_sector.get("name") == sector.get("name"):
                        new_sector = {
                            "name": r_sector.get("name"),
                            "tags": r_sector.get("tags"),
                            "queues": sector.get("queues")
                        }
                        integrated_feature.sectors.append(new_sector)
                        break
            for globals_key, globals_value in request.data.get("globals_values", {}).items():
                integrated_feature.globals_values[globals_key] = globals_value
            integrated_feature.action_base_flow = request.data.get("action_base_flow", "")
            integrated_feature.save(update_fields=["sectors", "globals_values", "action_base_flow"])
        
        for sector in integrated_feature.sectors:
            sectors_data.append(
                {
                    "name": sector.get("name", ""),
                    "tags": sector.get("tags", ""),
                    "service_limit": 4,
                    "working_hours": {"init": "08:00", "close": "18:00"},
                    "queues": sector.get("queues", []),
                }
            )

        body = {
            "definition": integrated_feature.feature_version.definition,
            "user_email": integrated_feature.user.email,
            "project_uuid": str(integrated_feature.project.uuid),
            "parameters": integrated_feature.globals_values,
            "feature_version": str(integrated_feature.feature_version.uuid),
            "feature_uuid": str(integrated_feature.feature.uuid),
            "sectors": sectors_data,
            "action": {
                "name": integrated_feature.feature_version.action_name,
                "prompt": integrated_feature.feature_version.action_prompt,
                "root_flow_uuid": integrated_feature.action_base_flow,
            },
        }

        IntegratedFeatureEDA().publisher(
            body=body, exchange="integrated-feature.topic"
        )
        print(f"message send `integrated feature` - body: {body}")

        response = {
            "status": 200,
            "data": {
                "feature": integrated_feature.feature.uuid,
                "feature_version": integrated_feature.feature_version.uuid,
                "project": integrated_feature.project.uuid,
                "user": integrated_feature.user.email,
                "integrated_on": integrated_feature.integrated_on
            }
        }
        return Response(response)

    def delete(self, request, *args, **kwargs):
        feature = Feature.objects.get(uuid=kwargs["feature_uuid"])
        try:
            project = Project.objects.get(uuid=request.data["project_uuid"])
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": f"Project with uuid equals {request.data['project_uuid' ]} does not exists!"})
        
        integrated_feature = IntegratedFeature.objects.get(project__uuid=str(project.uuid), feature__uuid=str(feature.uuid))
        
        body = {
            "project_uuid": str(project.uuid),
            "feature_version": str(integrated_feature.feature_version.uuid),
            "feature_uuid": str(integrated_feature.feature.uuid),
            "user_email": request.user.email,
        }

        IntegratedFeatureEDA().publisher(body=body, exchange="removed-feature.topic")
        print(f"message send to `removed-feature.topic`: {body}")
        integrated_feature.delete()
        return Response({"status": 200, "data":"integrated feature removed"})