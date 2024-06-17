from .imports import *
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def video_list(request):
    """
    List all videos.
    """
    videos = Video.objects.all()
    paginator = CustomPagination()
    page_obj = paginator.paginate_queryset(videos, request)
    serializer = VideoSerializer(page_obj, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def video_create(request):
    """
    Create a new video entry.
    """
    serializer = VideoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def video_detail(request, pk):
    """
    Retrieve details of a specific video by its primary key.
    """
    try:
        video = Video.objects.get(pk=pk)
    except Video.DoesNotExist:
        return Response({"errors": "Video not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = VideoSerializer(video)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def video_update(request, pk):
    """
    Update details of a specific video.
    """
    try:
        video = Video.objects.get(pk=pk)
    except Video.DoesNotExist:
        return Response({"errors": "Video not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = VideoSerializer(video, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def video_delete(request, pk):
    """
    Delete a specific video.
    """
    try:
        video = Video.objects.get(pk=pk)
        video.delete()
        return Response({"message": "Video deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Video.DoesNotExist:
        return Response({"errors": "Video not found."}, status=status.HTTP_404_NOT_FOUND)
