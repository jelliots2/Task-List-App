import React, { useState } from 'react';
import TodoList from './components/TodoList';
import TodoForm from './components/TodoForm';

const App = () => {
    const [editingTodo, setEditingTodo] = useState(null);

    return (
        <div>
            <h1>Todo App</h1>
            <TodoForm
                editingTodo={editingTodo}
                onSave={() => setEditingTodo(null)}
            />
            <TodoList onEdit={setEditingTodo} />
        </div>
    );
};

export default App;
