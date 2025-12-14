"use client";

import { useState, useEffect } from "react";
import apiClient from "@/src/lib/api_client";
import { Task } from "@/src/types/task";
import TaskItem from "./TaskItem";
import { useAuth } from "@/src/contexts/AuthContext";

const TaskList = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const { userId } = useAuth();

  const fetchTasks = async () => {
    if (!userId) {
      setError("User not authenticated.");
      setIsLoading(false);
      return;
    }
    try {
      setIsLoading(true);
      const response = await apiClient.get(`/api/${userId}/tasks`);
      setTasks(response.data);
    } catch (err) {
      setError("Failed to fetch tasks.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, [userId]);

  const handleTaskDeleted = (id: number) => {
    setTasks(tasks.filter((task) => task.id !== id));
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-32">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-600"></div>
        <p className="ml-4 text-gray-600">Loading tasks...</p>
      </div>
    );
  }

  if (error) {
    return <div className="text-red-600 bg-red-100 p-3 rounded-lg text-center">{error}</div>;
  }

  return (
    <div>
      {tasks.length === 0 ? (
        <div className="text-center p-8 bg-gray-50 rounded-lg shadow-inner">
          <p className="text-xl text-gray-600 font-semibold mb-2">No tasks yet!</p>
          <p className="text-gray-500">Looks like you're all caught up. Why not add a new task?</p>
        </div>
      ) : (
        <ul className="space-y-3">
          {tasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onTaskDeleted={handleTaskDeleted}
              onTaskUpdated={fetchTasks}
            />
          ))}
        </ul>
      )}
    </div>
  );
};

export default TaskList;
