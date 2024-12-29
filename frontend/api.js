const API_URL = 'http://localhost:5000/api/todos';

export async function fetchTodos() {
    const response = await fetch(API_URL);
    return response.json();
}

export async function createTodo(todo) {
    const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(todo),
    });
    return response.json();
}

export async function updateTodo(id, updates) {
    const response = await fetch(`${API_URL}/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updates),
    });
    return response.json();
}

export async function deleteTodo(id) {
    await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
}
