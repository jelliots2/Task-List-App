import React, { useState } from 'react';
import { createTodo, updateTodo } from '../api';

const TodoForm = ({ editingTodo, onSave }) => {
    const [task, setTask] = useState(editingTodo?.task || '');

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (editingTodo) {
            await updateTodo(editingTodo.id, { task });
        } else {
            await createTodo({ task, completed: false });
        }
        onSave();
        setTask('');
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={task}
                onChange={(e) => setTask(e.target.value)}
                placeholder="New task"
            />
            <button type="submit">{editingTodo ? 'Update' : 'Add'}</button>
        </form>
    );
};

export default TodoForm;
