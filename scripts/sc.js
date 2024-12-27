// RANDOM JAVASCRIPT CODE
function generateRandomString(length) {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}

// Simulate a basic to-do list app
class TodoList {
    constructor() {
        this.tasks = [];
    }

    addTask(task) {
        this.tasks.push({ id: generateRandomString(5), task, completed: false });
        console.log(`Added task: "${task}"`);
    }

    completeTask(id) {
        const task = this.tasks.find(t => t.id === id);
        if (task) {
            task.completed = true;
            console.log(`Task "${task.task}" marked as completed!`);
        } else {
            console.log(`Task with ID "${id}" not found.`);
        }
    }

    showTasks() {
        console.log("To-Do List:");
        this.tasks.forEach(task =>
            console.log(
                `[${task.completed ? "✔" : " "}] ${task.task} (ID: ${task.id})`
            )
        );
    }
}

// Example usage
const myTodoList = new TodoList();
myTodoList.addTask("Learn JavaScript");
myTodoList.addTask("Write a random JS code generator");
myTodoList.showTasks();
myTodoList.completeTask(myTodoList.tasks[0].id);
myTodoList.showTasks();
