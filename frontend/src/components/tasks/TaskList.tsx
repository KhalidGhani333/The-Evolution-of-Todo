/**
 * TaskList component.
 * Displays all tasks with completion status and actions.
 */
"use client";

import { Task } from "@/types";

interface TaskListProps {
  tasks: Task[];
  onTaskToggle: (taskId: number, completed: boolean) => void;
  onTaskDelete: (taskId: number) => void;
  onTaskEdit: (task: Task) => void;
}

const categoryColors: { [key: string]: string } = {
  work: "bg-blue-100 text-blue-800 border-blue-200",
  personal: "bg-purple-100 text-purple-800 border-purple-200",
  shopping: "bg-green-100 text-green-800 border-green-200",
  health: "bg-red-100 text-red-800 border-red-200",
  finance: "bg-yellow-100 text-yellow-800 border-yellow-200",
  default: "bg-gray-100 text-gray-800 border-gray-200",
};

function getCategoryColor(category: string | undefined): string {
  if (!category) return categoryColors.default;
  const key = category.toLowerCase();
  return categoryColors[key] || categoryColors.default;
}

export default function TaskList({ tasks, onTaskToggle, onTaskDelete, onTaskEdit }: TaskListProps) {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {tasks.map((task, index) => (
        <div
          key={task.id}
          className="glass rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:scale-[1.02] border border-white/20 overflow-hidden animate-slideUp"
          style={{ animationDelay: `${index * 0.05}s` }}
        >
          <div className="p-5">
            {/* Header with checkbox and actions */}
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-start space-x-3 flex-1">
                <div className="flex-shrink-0 mt-1">
                  <button
                    onClick={() => onTaskToggle(task.id, !task.completed)}
                    className={`w-6 h-6 rounded-lg border-2 flex items-center justify-center transition-all duration-200 ${
                      task.completed
                        ? "bg-gradient-to-r from-green-500 to-emerald-500 border-green-500"
                        : "border-gray-300 hover:border-blue-500"
                    }`}
                    title={task.completed ? "Mark as incomplete" : "Mark as complete"}
                  >
                    {task.completed && (
                      <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                      </svg>
                    )}
                  </button>
                </div>
                <div className="flex-1 min-w-0">
                  <h3
                    className={`text-base font-semibold mb-1 transition-all duration-200 ${
                      task.completed
                        ? "line-through text-gray-400"
                        : "text-gray-900"
                    }`}
                  >
                    {task.title}
                  </h3>
                  {task.description && (
                    <p
                      className={`text-sm mt-2 line-clamp-2 ${
                        task.completed ? "text-gray-400" : "text-gray-600"
                      }`}
                    >
                      {task.description}
                    </p>
                  )}
                </div>
              </div>
              <div className="flex items-center space-x-1 ml-2">
                <button
                  onClick={() => onTaskEdit(task)}
                  className="flex-shrink-0 p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-200"
                  title="Edit task"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
                <button
                  onClick={() => onTaskDelete(task.id)}
                  className="flex-shrink-0 p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all duration-200"
                  title="Delete task"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>

            {/* Footer with category and date */}
            <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-200">
              <div className="flex items-center space-x-2">
                {task.category ? (
                  <span
                    className={`inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-semibold border ${getCategoryColor(
                      task.category
                    )}`}
                  >
                    <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                    </svg>
                    {task.category}
                  </span>
                ) : (
                  <span className="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-medium bg-gray-100 text-gray-500 border border-gray-200">
                    No category
                  </span>
                )}
              </div>
              <div className="flex items-center text-xs text-gray-500">
                <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                {new Date(task.created_at).toLocaleDateString('en-US', {
                  month: 'short',
                  day: 'numeric',
                })}
              </div>
            </div>
          </div>

          {/* Completion indicator bar */}
          {task.completed && (
            <div className="h-1 bg-gradient-to-r from-green-500 to-emerald-500"></div>
          )}
        </div>
      ))}
    </div>
  );
}
