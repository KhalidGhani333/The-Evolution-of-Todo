/**
 * Tasks page - main dashboard for task management.
 * Displays task list and add task form.
 */
"use client";

import { useState, useEffect } from "react";
import { Task } from "@/types";
import AddTaskForm from "@/components/tasks/AddTaskForm";
import TaskList from "@/components/tasks/TaskList";
import EditTaskModal from "@/components/tasks/EditTaskModal";
import { signOut } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";

export default function TasksPage() {
  const { user, isLoading: authLoading } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>("");
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);

  const fetchTasks = async () => {
    if (!user) return;

    try {
      setIsLoading(true);
      const token = localStorage.getItem('auth_token');
      const response = await fetch(`/api/${user.id}/tasks`, {
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });
      if (!response.ok) throw new Error("Failed to fetch tasks");

      const data = await response.json();
      setTasks(data.tasks);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load tasks");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (user) {
      fetchTasks();
    }
  }, [user]);

  const handleTaskToggle = async (taskId: number, completed: boolean) => {
    if (!user) return;

    try {
      const token = localStorage.getItem('auth_token');
      const response = await fetch(`/api/${user.id}/tasks/${taskId}/complete`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ completed }),
      });

      if (!response.ok) throw new Error("Failed to update task");

      // Optimistic update
      setTasks(tasks.map(task =>
        task.id === taskId ? { ...task, completed } : task
      ));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update task");
    }
  };

  const handleTaskDelete = async (taskId: number) => {
    if (!user) return;
    if (!confirm("Are you sure you want to delete this task?")) return;

    try {
      const token = localStorage.getItem('auth_token');
      const response = await fetch(`/api/${user.id}/tasks/${taskId}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });

      if (!response.ok) throw new Error("Failed to delete task");

      // Remove from list
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete task");
    }
  };

  const handleTaskEdit = (task: Task) => {
    setEditingTask(task);
    setIsEditModalOpen(true);
  };

  const handleTaskUpdate = async (taskId: number, data: { title: string; description?: string; category?: string }) => {
    if (!user) return;

    try {
      const token = localStorage.getItem('auth_token');
      const response = await fetch(`/api/${user.id}/tasks/${taskId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) throw new Error("Failed to update task");

      const updatedTask = await response.json();

      // Update task in list
      setTasks(tasks.map(task =>
        task.id === taskId ? updatedTask : task
      ));

      setIsEditModalOpen(false);
      setEditingTask(null);
    } catch (err) {
      throw new Error(err instanceof Error ? err.message : "Failed to update task");
    }
  };

  if (authLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-4"></div>
          <p className="text-gray-600 font-medium">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center">
        <div className="text-center glass rounded-2xl p-8 shadow-xl">
          <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
          <p className="text-gray-600 font-medium">Please sign in to view tasks</p>
        </div>
      </div>
    );
  }

  const completedCount = tasks.filter(t => t.completed).length;
  const pendingCount = tasks.length - completedCount;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      {/* Modern Navigation Bar */}
      <nav className="bg-white shadow-lg border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center space-x-4">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center shadow-md">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  My Tasks
                </h1>
                <p className="text-xs text-gray-500">{user.email}</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="hidden sm:flex items-center space-x-4 text-sm">
                <div className="flex items-center space-x-2 px-3 py-1 bg-blue-50 rounded-full">
                  <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                  <span className="text-blue-700 font-medium">{pendingCount} Pending</span>
                </div>
                <div className="flex items-center space-x-2 px-3 py-1 bg-green-50 rounded-full">
                  <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                  <span className="text-green-700 font-medium">{completedCount} Done</span>
                </div>
              </div>
              <button
                onClick={signOut}
                className="flex items-center space-x-2 px-4 py-2 text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-all duration-200 font-medium"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                <span className="hidden sm:inline">Sign Out</span>
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-center animate-slideDown">
            <svg className="w-5 h-5 text-red-600 mr-3" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            <span className="text-red-800 font-medium">{error}</span>
          </div>
        )}

        <div className="space-y-8">
          {/* Add Task Form */}
          <div className="animate-slideUp">
            <AddTaskForm onTaskAdded={fetchTasks} userId={user.id} />
          </div>

          {/* Tasks List */}
          <div className="animate-slideUp" style={{ animationDelay: '0.1s' }}>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">
                All Tasks
                <span className="ml-3 text-lg font-normal text-gray-500">({tasks.length})</span>
              </h2>
            </div>

            {isLoading ? (
              <div className="text-center py-16">
                <div className="inline-block w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-4"></div>
                <p className="text-gray-600 font-medium">Loading tasks...</p>
              </div>
            ) : tasks.length === 0 ? (
              <div className="text-center py-16 glass rounded-2xl shadow-lg">
                <svg className="w-24 h-24 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
                <h3 className="text-xl font-semibold text-gray-700 mb-2">No tasks yet</h3>
                <p className="text-gray-500">Create your first task to get started!</p>
              </div>
            ) : (
              <TaskList
                tasks={tasks}
                onTaskToggle={handleTaskToggle}
                onTaskDelete={handleTaskDelete}
                onTaskEdit={handleTaskEdit}
              />
            )}
          </div>
        </div>
      </main>

      {/* Edit Task Modal */}
      {editingTask && (
        <EditTaskModal
          task={editingTask}
          isOpen={isEditModalOpen}
          onClose={() => {
            setIsEditModalOpen(false);
            setEditingTask(null);
          }}
          onSave={handleTaskUpdate}
        />
      )}
    </div>
  );
}
