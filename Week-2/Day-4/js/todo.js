let todos = getTodos();

function addTodo(text) {
  const todo = {
    id: Date.now(),
    text,
  };
  todos.push(todo);
  saveTodos(todos);
}

function deleteTodo(id) {
  todos = todos.filter(todo => todo.id !== id);
  saveTodos(todos);
}

function editTodo(id, newText) {
  const todo = todos.find(t => t.id === id);
  if (todo) {
    todo.text = newText;
    saveTodos(todos);
  }
}

function getAllTodos() {
  return todos;
}
