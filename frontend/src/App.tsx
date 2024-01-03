import React, { useState, useEffect, useCallback } from "react";
import AddTask from "./components/AddTask";
import "./App.scss";
import AppTitle from "./components/AppTitle/AppTitle";
import TaskList from "./components/task-list/TaskList";


type TaskType = {
  id: number;
  title: string;
  completed: boolean;
  position: number;
};

const App: React.FC = () => {
  const [tasks, setTasks] = useState<TaskType[]>([]);
  const [addTaskLoading, setAddTaskLoading] = useState<boolean>(false);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await fetch("http://localhost:8000/tasks/");
        const data = await response.json();
        if (data.length === 0) {
          console.log("No tasks found");
        } else {
          setTasks(data);
        }
      } catch (error) {
        console.error("Error fetching tasks:", error);
      }
    };

    fetchTasks();
  }, []);

  const handleAddTask = async (title: string) => {
    setAddTaskLoading(true);
    try {
      const newTask = await addTask(title);
      setTasks([newTask, ...tasks]);
    } catch (error) {
      console.error('Error adding task:', error);
    } finally {
      setAddTaskLoading(false);
    }
  };
  
  async function addTask(title: string) {
    setAddTaskLoading(true);
    const response = await fetch("http://localhost:8000/tasks/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title }),
    })
    return response.json();
  }

  const handleToggleCompleted = async (id: number) => {
    const task = tasks.find((task) => task.id === id);
    if (task) {
      const updatedTask = { ...task, completed: !task.completed };
      const response = await fetch(`http://localhost:8000/tasks/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedTask),
      });
      if (response.ok) {
        setTasks(tasks.map((t) => (t.id === id ? updatedTask : t)));
      }
    }
  };

  const handleDeleteTask = async (id: number) => {
    const response = await fetch(`http://localhost:8000/tasks/${id}`, {
      method: "DELETE",
    });
    if (response.ok) {
      setTasks(tasks.filter((task) => task.id !== id));
    }
  };

  const handleReorder = (newOrder: TaskType[]) => {
    setTasks(newOrder);
  };

  const handleDragEnd = useCallback(async () => {
    const reorderedTasks = tasks.map((task, index) => ({ id: task.id, position: index }));

    try {
      const response = await fetch("http://localhost:8000/tasks/reorder", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ tasks: reorderedTasks }),
      });

      if (response.ok) {
        console.log("Reordered tasks saved successfully");
      } else {
        console.error("Failed to save reordered tasks");
        const errorData = await response.json();
        console.error("Error details:", errorData);
      }
    } catch (error) {
      console.error("Error sending reordered tasks to server:", error);
    }
  }, [tasks]);

  useEffect(() => {
    window.addEventListener('pointerup', handleDragEnd);
    return () => {
      window.removeEventListener('pointerup', handleDragEnd);
    };
  }, [handleDragEnd, tasks]);

  const updateTaskTitle = async (taskId:number, title:string) => {
    const response = await fetch(`http://localhost:8000/tasks/${taskId}/title`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title })
    });
    if (!response.ok) {
        throw new Error('Failed to update task title');
    }
    return await response.json();
  };


  return (
    <div id="App">
      <div id="MainWrapper">

        <header>
          <AppTitle />
          <AddTask onAdd={handleAddTask} loading={addTaskLoading} />
        </header>

        <TaskList
          tasks={tasks}
          onReorder={handleReorder}
          onToggleCompleted={handleToggleCompleted}
          onDelete={handleDeleteTask}
          updateTaskTitle={updateTaskTitle}
        />
      </div>
    </div>
  );
};

export default App;
