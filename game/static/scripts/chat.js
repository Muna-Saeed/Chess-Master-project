const chatContainer = document.querySelector('.container');
const chatBox = document.querySelector('.chatbox');

let initialX = null;
let initialY = null;

chatContainer.addEventListener('mousedown', (event) => {
  initialX = event.clientX;
  initialY = event.clientY;
  chatContainer.classList.add('dragging');
  chatBox.classList.add('dragging');
});

document.addEventListener('mouseup', () => {
  initialX = null;
  initialY = null;
  chatContainer.classList.remove('dragging');
  chatBox.classList.remove('dragging');
});

document.addEventListener('mousemove', (event) => {
  if (initialX === null || initialY === null) return;

  const deltaX = event.clientX - initialX;
  const deltaY = event.clientY - initialY;

  const newLeft = chatContainer.offsetLeft + deltaX;
  const newTop = chatContainer.offsetTop + deltaY;

  // Prevent dragging outside the window (optional)
  chatContainer.style.left = `${Math.max(0, newLeft)}px`;
  chatContainer.style.top = `${Math.max(0, newTop)}px`;

  initialX = event.clientX;
  initialY = event.clientY;
});
