from rest_framework import serializers
from dataclasses import dataclass


@dataclass
class Repo:
    name: str
    description: str
    html_url: str


class RepositoryInfoSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    f = serializers.CharField(source="html_url")
    name = serializers.CharField()
    description = serializers.CharField(allow_null=True)

    def create(self, validated_data):
        return Repo(**validated_data)

