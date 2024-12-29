import React, { useEffect, useState } from 'react';
import { fetchTodos, deleteTodo } from '../api';

const TodoList = ({ onEdit }) => {
    const [todos, setTodos] = useState([]);

    useEffect(() => {
        async function loadTodos() {
            const fetchedTodos = await fetchTodos();
            setTodos(fetchedTodos);
        }
        loadTodos();
    }, []);

    const handleDelete = async (id) => {
        await deleteTodo(id);
        setTodos(todos.filter(todo => todo.id !== id));
    };

    return (
        <ul>
            {todos.map(todo => (
                <li key={todo.id}>
                    <span>{todo.task}</span>
                    <button onClick={() => onEdit(todo)}>Edit</button>
                    <button onClick={() => handleDelete(todo.id)}>Delete</button>
                </li>
            ))}
        </ul>
    );
};

export default TodoList;
