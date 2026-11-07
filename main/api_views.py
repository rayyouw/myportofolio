from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Award, Project
from main.permissions import (
    IsPortfolioOwnerOrEditorOrReadOnly,
    IsPortfolioOwnerOrReadOnly,
)
from main.serializers import AwardSerializer, ProjectSerializer


def _project_or_404(project_id):
    if not str(project_id).isdigit():
        raise Http404
    return get_object_or_404(
        Project.objects.prefetch_related("starred_by"), pk=project_id,
    )


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_list(request):
    projects = Project.objects.prefetch_related("starred_by").order_by("title", "id")
    title_query = request.query_params.get("title", "").strip()
    if title_query:
        projects = projects.filter(title__icontains=title_query)

    if request.method in ("GET", "HEAD"):
        serializer = ProjectSerializer(
            projects, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = ProjectSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_detail(request, project_id):
    project = _project_or_404(project_id)
    if request.method in ("GET", "HEAD"):
        serializer = ProjectSerializer(project, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ProjectSerializer(
        project,
        data=request.data,
        partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def project_star(request, project_id):
    project = _project_or_404(project_id)
    if project.starred_by.filter(pk=request.user.pk).exists():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)
    serializer = ProjectSerializer(project, context={"request": request})
    return Response(serializer.data)


def _award_or_404(award_id):
    if not str(award_id).isdigit():
        raise Http404
    return get_object_or_404(
        Award.objects.prefetch_related("starred_by"), pk=award_id,
    )


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def award_list(request):
    awards = Award.objects.prefetch_related("starred_by").order_by("-created_at", "id")
    title_query = request.query_params.get("title", "").strip()
    if title_query:
        awards = awards.filter(title__icontains=title_query)

    if request.method in ("GET", "HEAD"):
        serializer = AwardSerializer(
            awards, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = AwardSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    award = serializer.save()
    return Response(
        AwardSerializer(award, context={"request": request}).data,
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def award_detail(request, award_id):
    award = _award_or_404(award_id)
    if request.method in ("GET", "HEAD"):
        return Response(
            AwardSerializer(award, context={"request": request}).data,
        )

    if request.method == "DELETE":
        award.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = AwardSerializer(
        award,
        data=request.data,
        partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def award_star(request, award_id):
    award = _award_or_404(award_id)
    if award.starred_by.filter(pk=request.user.pk).exists():
        award.starred_by.remove(request.user)
    else:
        award.starred_by.add(request.user)
    return Response(AwardSerializer(award, context={"request": request}).data)
