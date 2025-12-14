"use client";

import { useState, FormEvent } from "react";
import { useAuth } from "../contexts/AuthContext";
import apiClient from "@/src/lib/api_client";
import { TaskCreate } from "../types/task";

interface AddTaskFormProps {
  onTaskAdded?: () => void;
}

export default function AddTaskForm({ onTaskAdded }: AddTaskFormProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { userId } = useAuth();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");

    if (!title.trim()) {
      setError("Title is required");
      return;
    }

    if (title.length > 100) {
      setError("Title must be 100 characters or less");
      return;
    }

    if (description && description.length > 500) {
      setError("Description must be 500 characters or less");
      return;
    }

    setIsLoading(true);

    if (!userId) {
      setError("User not authenticated. Please sign in again.");
      setIsLoading(false);
      return;
    }

    try {
      const taskData: TaskCreate = {
        title: title.trim(),
        description: description.trim() || undefined,
      };

      await apiClient.post(`/api/${userId}/tasks`, taskData);

      // Clear form
      setTitle("");
      setDescription("");

      // Notify parent to refresh list
      if (onTaskAdded) {
        onTaskAdded();
      }
    } catch (err: any) {
      setError(err.message || "Failed to add task");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg animate-fade-in">
          {error}
        </div>
      )}

      <div>
        <label htmlFor="title" className="block text-sm font-semibold text-gray-700 mb-1">
          Title <span className="text-red-500">*</span>
        </label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200 ease-in-out text-black"
          placeholder="Enter task title"
          maxLength={100}
          required
        />
      </div>
      <div>
        <label
          htmlFor="description"
          className="block text-sm font-semibold text-gray-700 mb-1"
        >
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
          className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200 ease-in-out text-black"
          placeholder="Enter task description (optional)"
          maxLength={500}
        ></textarea>
      </div>
      <button
        type="submit"
        disabled={isLoading}
        className="inline-flex justify-center py-2 px-5 border border-transparent shadow-md text-sm font-medium rounded-lg text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-60 disabled:cursor-not-allowed transition-all duration-300 ease-in-out transform hover:scale-105"
      >
        {isLoading ? "Adding Task..." : "Add Task"}
      </button>
    </form>
  );
}