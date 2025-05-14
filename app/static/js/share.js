$(document).ready(function () {
  // Fetch users from the /users API and populate the dropdown
  $.getJSON('/users')
    .done(function (users) {
      const dropdown = $('#userDropdown');
      users.forEach(user => {
        dropdown.append(`<option value="${user.id}">${user.username}</option>`);
      });
    })
    .fail(function () {
      console.error('Error fetching users');
      alert('Failed to load users. Please try again later.');
    });

  // Handle the Share Data button click
  $('#shareButton').on('click', function () {
    const selectedUserId = $('#userDropdown').val();
    if (!selectedUserId) {
      alert('Please select a user to share data with.');
      return;
    }

    // Send the selected user ID to the backend
    $.ajax({
      url: '/share_data',
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({to_user_id: selectedUserId}),
      success: function (response) {
        if (response.exist){
            alert('You have already shared data with this user.');
        }else {
            alert('Data shared successfully!');
        } 
      },
      error: function (xhr) {
        const errorResponse = JSON.parse(xhr.responseText);
        alert('Failed to share data. Please try again.');
      }
    });
  });
});