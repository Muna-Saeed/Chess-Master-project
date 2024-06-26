fetch('/getOnlineUsers')
  .then(response => response.json())
  .then(data => {
    data.online.forEach(user => {
      console.log(user.username); // Accessing each user's username property
    });
  })
  .catch(error => {
    console.error('Error:', error);
  });
