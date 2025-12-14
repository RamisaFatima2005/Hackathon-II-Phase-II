"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import apiClient from "@/src/lib/api_client";
import { Task } from "@/src/types/task";
import Link from "next/link";
import { useAuth } from "@/src/contexts/AuthContext";

const TaskDetailPage = () => {
  const params = useParams();
  const router = useRouter();
  const { id } = params;

  const [task, setTask] = useState<Task | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const { userId } = useAuth();

  useEffect(() => {
    if (id && userId) { // Ensure userId is available before fetching
      const fetchTask = async () => {
        try {
          const response = await apiClient.get<Task>(`/api/${userId}/tasks/${id}`);
          setTask(response.data);
        } catch (err) {
          console.error("Error fetching task details:", err);
          setError("Failed to fetch task details.");
        } finally {
          setIsLoading(false);
        }
      };
      fetchTask();
    } else if (!userId) {
      setError("User not authenticated.");
      setIsLoading(false);
    }
  }, [id, userId]);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-600"></div>
        <p className="ml-4 text-gray-600">Loading task details...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100">
        <div className="text-red-600 bg-red-100 p-4 rounded-lg shadow-md text-center">
          <p className="font-semibold mb-2">Error:</p>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!task) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100">
        <div className="text-gray-700 bg-white p-4 rounded-lg shadow-md text-center">
          <p className="font-semibold text-xl mb-2">Task Not Found</p>
          <p>The requested task could not be found or does not exist.</p>
          <Link href="/dashboard" className="mt-4 inline-block text-indigo-600 hover:text-indigo-800 transition-colors duration-200">
            &larr; Back to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 font-sans p-8">
      <div className="max-w-3xl mx-auto bg-white rounded-xl shadow-xl p-8 md:p-10 border border-gray-200">
        <div className="flex justify-between items-start mb-6 border-b pb-4">
          <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight">
            {task.title}
          </h1>
          <div className="flex space-x-3">
            <Link
              href={`/task/${id}/edit`}
              className="px-4 py-2 bg-indigo-600 text-white rounded-lg shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 focus:ring-opacity-75 transition-all duration-300 ease-in-out transform hover:scale-105 font-medium text-sm"
            >
              Edit Task
            </Link>
            <Link
              href="/dashboard"
              className="px-4 py-2 text-indigo-700 bg-indigo-100 rounded-lg shadow-md hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 focus:ring-opacity-75 transition-all duration-300 ease-in-out transform hover:scale-105 font-medium text-sm"
            >
              &larr; Back to Dashboard
            </Link>
          </div>
        </div>
        <p className="text-lg text-gray-700 leading-relaxed mb-6">{task.description}</p>
        <div className="flex items-center text-md text-gray-800">
          <span className="font-bold mr-2">Status:</span>
          <span className={`px-3 py-1 rounded-full text-sm font-semibold ${task.completed ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"}`}>
            {task.completed ? "Completed" : "Pending"}
          </span>
        </div>
      </div>
    </div>
  );
};

export default TaskDetailPage;
