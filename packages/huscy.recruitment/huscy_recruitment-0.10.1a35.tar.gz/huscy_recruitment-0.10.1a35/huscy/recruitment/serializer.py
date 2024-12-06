from rest_framework import serializers

from huscy.appointments.serializers import AppointmentSerializer
from huscy.recruitment import models, services
from huscy.recruitment.models import Recall
from huscy.recruitment.services import create_or_update_participation_request


class ParticipationRequestSerializer(serializers.ModelSerializer):
    appointment = serializers.DateTimeField(required=False)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    timeslots = serializers.ListField(required=False, child=serializers.IntegerField(min_value=1))
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.ParticipationRequest
        fields = (
            'appointment',
            'attribute_filterset',
            'id',
            'status',
            'status_display',
            'timeslots',
            'user',
        )
        read_only_fields = 'attribute_filterset',

    def create(self, validated_data):
        attribute_filterset = self.context.get('attribute_filterset')
        subject = self.context.get('subject')

        return create_or_update_participation_request(subject, attribute_filterset,
                                                      **validated_data)

    def to_representation(self, participation_request):
        response = super().to_representation(participation_request)
        if participation_request.status == models.ParticipationRequest.STATUS.get_value('pending'):
            try:
                recall = participation_request.recall.get()
            except Recall.DoesNotExist:
                return response

            # TODO: skip this, if appointment is in the past
            response['recall_appointment'] = AppointmentSerializer(recall.appointment).data
        return response


class AttributeFilterSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttributeFilterSet
        fields = (
            'filters',
            'id',
        )

    def update(self, attribute_filterset, validated_data):
        return services.update_attribute_filterset(attribute_filterset, **validated_data)


class SubjectGroupSerializer(serializers.ModelSerializer):
    attribute_filtersets = AttributeFilterSetSerializer(many=True, read_only=True)

    class Meta:
        model = models.SubjectGroup
        fields = (
            'attribute_filtersets',
            'description',
            'experiment',
            'id',
            'name',
            'order',
        )
        read_only_fields = ('experiment', )

    def create(self, validated_data):
        experiment = self.context['experiment']
        return services.create_subject_group(experiment, **validated_data)
