"use client";

import ProtectedRoute from "@/src/components/ProtectedRoute";
import { useAuth } from "@/src/contexts/AuthContext";
import TaskList from "@/src/components/TaskList";
import AddTaskForm from "@/src/components/AddTaskForm";
import { useState } from "react";

export default function DashboardPage() {
  const { user } = useAuth(); // Keep user for email
  const [refreshTasks, setRefreshTasks] = useState(false);

  const handleTaskAdded = () => {
    setRefreshTasks(!refreshTasks);
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-100 font-sans">
        {/* Main Content */}
        <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight">My Todos</h1>
            {user && (
              <p className="text-lg text-gray-600">Welcome, <span className="font-semibold text-indigo-700">{user.email}</span></p>
            )}
          </div>

          <div className="space-y-8">
            {/* Add Task Form */}
            <section className="bg-white rounded-xl shadow-xl p-6 md:p-8 transform transition-all duration-300 ease-in-out hover:shadow-2xl">
              <h2 className="text-2xl font-bold text-gray-800 mb-6 border-b pb-4">Add New Task</h2>
              <AddTaskForm onTaskAdded={handleTaskAdded} />
            </section>

            {/* Task List */}
            <section className="bg-white rounded-xl shadow-xl p-6 md:p-8 transform transition-all duration-300 ease-in-out hover:shadow-2xl">
              <h2 className="text-2xl font-bold text-gray-800 mb-6 border-b pb-4">Your Tasks</h2>
              <TaskList key={refreshTasks.toString()} />
            </section>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}