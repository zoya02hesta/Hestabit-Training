const input = document.getElementById("todo-input");
const addBtn = document.getElementById("add-btn");
const list = document.getElementById("todo-list");

function renderTodos() {
  list.innerHTML = "";

  getAllTodos().forEach(todo => {
    const li = document.createElement("li");

const textSpan = document.createElement("span");
textSpan.textContent = todo.text;


    const editBtn = document.createElement("button");
    editBtn.textContent = "Edit";
    editBtn.onclick = () => {
      const newText = prompt("Edit todo:", todo.text);
      if (newText) {
        editTodo(todo.id, newText);
        renderTodos();
      }
    };

    const delBtn = document.createElement("button");
    delBtn.textContent = "Delete";
    delBtn.onclick = () => {
      deleteTodo(todo.id);
      renderTodos();
    };

    li.append(textSpan, editBtn, delBtn);

    list.appendChild(li);
  });
}

addBtn.addEventListener("click", () => {
  if (!input.value.trim()) return;
  addTodo(input.value);
  input.value = "";
  renderTodos();
});

// Initial load
renderTodos();
