from abc import ABC

from rest_framework import serializers
from dataclasses import dataclass


@dataclass
class Repo:
    name: str
    description: str
    html_url: str


class RepositoryInfoSerializer(serializers.Serializer):
    html_url = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField(allow_null=True)

    def create(self, validated_data):
        return Repo(**validated_data)
