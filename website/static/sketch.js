function deleteEntry(entryId){
    fetch('/delete-entry', {
        method: 'POST',
        body: JSON.stringify({ entryId: entryId })
    }).then((_res) => {
        window.location.href = "/profile";
    })
}

function deleteUser(userId){
    fetch('/delete-user', {
        method: 'POST',
        body: JSON.stringify({ userId: userId })
    }).then((_res) => {
        window.location.href = "/accounts";
    })
}
$('textarea').keyup(function() {
    
  var characterCount = $(this).val().length,
      current = $('#current'),
      maximum = $('#maximum'),
      theCount = $('#the-count');
    
  current.text(characterCount);});