var alert = document.getElementById('alert');

window.onclick = function(event) {
  if (event.target == alert) {
    alert.style.display = "none";
  }
}

function deleteNote(noteId) {
  fetch('/delete-note', {
    method: 'POST',
    body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
    });
}
