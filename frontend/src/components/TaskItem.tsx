"use client";

import { Task } from "@/src/types/task";
import Link from "next/link";
import apiClient from "@/src/lib/api_client";
import { useAuth } from "@/src/contexts/AuthContext";

interface TaskItemProps {
  task: Task;
  onTaskDeleted: (id: number) => void;
  onTaskUpdated: () => void;
}

const TaskItem = ({ task, onTaskDeleted, onTaskUpdated }: TaskItemProps) => {
  const { userId } = useAuth();

  const handleDelete = async () => {
    if (!userId) {
      alert("User not authenticated. Please sign in again.");
      return;
    }
    if (window.confirm("Are you sure you want to delete this task?")) {
      try {
        await apiClient.delete(`/api/${userId}/tasks/${task.id}`);
        onTaskDeleted(task.id);
      } catch (error) {
        alert("Failed to delete task.");
      }
    }
  };

  const handleToggleComplete = async () => {
    if (!userId) {
      alert("User not authenticated. Please sign in again.");
      return;
    }
    try {
      await apiClient.patch(`/api/${userId}/tasks/${task.id}/complete`);
      onTaskUpdated();
    } catch (error) {
      alert("Failed to update task status.");
    }
  };

  return (
    <li
      className={`p-5 mb-3 bg-white rounded-lg shadow-md flex justify-between items-center transform transition-all duration-300 ease-in-out hover:scale-[1.02] hover:shadow-lg ${
        task.completed ? "opacity-70 border-l-4 border-green-500" : "border-l-4 border-indigo-500"
      }`}
    >
      <div>
        <Link href={`/task/${task.id}`}>
          <h3 className={`text-xl font-semibold ${task.completed ? "line-through text-gray-500" : "text-gray-800"}`}>
            {task.title}
          </h3>
        </Link>
        <p className="text-gray-600 text-sm mt-1">{task.description}</p>
      </div>
      <div className="flex items-center space-x-3">
        <button
          onClick={handleToggleComplete}
          className={`p-2 rounded-lg text-white font-medium shadow-md transition-all duration-300 ease-in-out transform hover:scale-105 ${
            task.completed
              ? "bg-yellow-500 hover:bg-yellow-600"
              : "bg-green-600 hover:bg-green-700"
          } cursor-pointer`}
        >
          {task.completed ? "Mark as Incomplete" : "Mark as Complete"}
        </button>
        <Link
          href={`/task/${task.id}/edit`}
          className="p-2 bg-indigo-600 text-white rounded-lg shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 focus:ring-opacity-75 transition-all duration-300 ease-in-out transform hover:scale-105 cursor-pointer"
        >
          Edit
        </Link>
        <button
          onClick={handleDelete}
          className="p-2 bg-red-600 text-white rounded-lg shadow-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 focus:ring-opacity-75 transition-all duration-300 ease-in-out transform hover:scale-105 cursor-pointer"
        >
          Delete
        </button>
      </div>
    </li>
  );
};

export default TaskItem;
