from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId, errors as bson_errors
import pymongo

# MongoDB client setup
client = None
db = client['mongo']
collection = db['Tasks']

# Helper to serialize MongoDB documents
def serialize_task(task):
    task['_id'] = str(task['_id'])
    return task

class TaskListView(APIView):
    def get(self, request):
        tasks = list(collection.find())
        return Response([serialize_task(task) for task in tasks])

    def post(self, request):
        data = request.data
        new_task = {
            "title": data.get("title", ""),
            "completed": data.get("completed", False)
        }
        result = collection.insert_one(new_task)
        new_task['_id'] = str(result.inserted_id)
        return Response(new_task, status=status.HTTP_201_CREATED)

class TaskDetailView(APIView):
    def get(self, request, task_id):
        try:
            task = collection.find_one({"_id": ObjectId(task_id)})
            if not task:
                return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response(serialize_task(task))
        except bson_errors.InvalidId:
            return Response({"error": "Invalid ID"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, task_id):
        try:
            data = request.data
            result = collection.update_one(
                {"_id": ObjectId(task_id)},
                {"$set": {
                    "title": data.get("title", ""),
                    "completed": data.get("completed", False)
                }}
            )
            if result.matched_count == 0:
                return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Task updated successfully"})
        except bson_errors.InvalidId:
            return Response({"error": "Invalid ID"}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, task_id):
        try:
            data = request.data
            updates = {}
            if 'title' in data:
                updates['title'] = data['title']
            if 'completed' in data:
                updates['completed'] = data['completed']

            result = collection.update_one({"_id": ObjectId(task_id)}, {"$set": updates})
            if result.matched_count == 0:
                return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Task partially updated"})
        except bson_errors.InvalidId:
            return Response({"error": "Invalid ID"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id):
        try:
            result = collection.delete_one({"_id": ObjectId(task_id)})
            if result.deleted_count == 0:
                return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Task deleted successfully"})
        except bson_errors.InvalidId:
            return Response({"error": "Invalid ID"}, status=status.HTTP_400_BAD_REQUEST)
