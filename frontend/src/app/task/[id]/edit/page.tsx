"use client";

import { useState, useEffect, FormEvent } from "react";
import { useParams, useRouter } from "next/navigation";
import apiClient from "@/src/lib/api_client";
import { Task } from "@/src/types/task";
import Link from "next/link";
import { useAuth } from "@/src/contexts/AuthContext";

const TaskEditPage = () => {
  const params = useParams();
  const router = useRouter();
  const { id } = params;

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [completed, setCompleted] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const { userId } = useAuth();

  useEffect(() => {
    if (id && userId) { // Ensure userId is available before fetching
      const fetchTask = async () => {
        try {
          const response = await apiClient.get<Task>(`/api/${userId}/tasks/${id}`);
          setTitle(response.data.title || "");
          setDescription(response.data.description || "");
          setCompleted(response.data.completed ?? false);
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

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!userId) {
      setError("User not authenticated. Please sign in again.");
      return;
    }
    try {
      await apiClient.put(`/api/${userId}/tasks/${id}`, { title, description, completed });
      router.push(`/task/${id}`);
    } catch (err) {
      setError("Failed to update task.");
    }
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Edit Task</h1>
          <Link
            href={`/task/${id}`}
            className="text-sm font-medium text-indigo-600 hover:text-indigo-500 transition-colors duration-200"
          >
            &larr; Back to Task
          </Link>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="title" className="block text-sm font-semibold text-gray-700 mb-1">
              Title
            </label>
            <input
              id="title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200 ease-in-out text-black"
            />
          </div>
          <div>
            <label htmlFor="description" className="block text-sm font-semibold text-gray-700 mb-1">
              Description
            </label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={3}
              className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200 ease-in-out text-black"
            />
          </div>
          <button
            type="submit"
            className="inline-flex justify-center py-2 px-5 border border-transparent shadow-md text-sm font-medium rounded-lg text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-60 disabled:cursor-not-allowed transition-all duration-300 ease-in-out transform hover:scale-105 cursor-pointer"
          >
            Update Task
          </button>
        </form>
      </div>
    </div>
  );
};

export default TaskEditPage;
