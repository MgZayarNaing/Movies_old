from .imports import *
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_list(request):
    """
    List all comments for videos.
    """
    comments = VideoComment.objects.all()
    paginator = CustomPagination()
    page_obj = paginator.paginate_queryset(comments, request)
    serializer = VideoCommentSerializer(page_obj, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request):
    serializer = VideoCommentSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_detail(request, pk):
    """
    Retrieve a specific comment by its ID.
    """
    try:
        comment = VideoComment.objects.get(pk=pk)
        serializer = VideoCommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except VideoComment.DoesNotExist:
        return Response({'errors': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def comment_update(request, pk):
    """
    Update a specific comment.
    """
    try:
        comment = VideoComment.objects.get(pk=pk)
        serializer = VideoCommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except VideoComment.DoesNotExist:
        return Response({'errors': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_delete(request, pk):
    """
    Delete a specific comment.
    """
    try:
        comment = VideoComment.objects.get(pk=pk)
        comment.delete()
        return Response({'message': 'Comment deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except VideoComment.DoesNotExist:
        return Response({'errors': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)