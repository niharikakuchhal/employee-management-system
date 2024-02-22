$(document).ready(function() {
    // Function to add a new row
    function addNewRow() {
        const newRowNumber = $('#experienceSection tr').length + 1;
        const newRow = `
            <tr>
                <td>${newRowNumber}</td>
                <td><input type="text" name="company_name[]" placeholder="Company Name" required></td>
                <td><input type="text" name="role[]" placeholder="Role" required></td>
                <td><input type="date" name="date_of_joining[]"  placeholder="Date of Joining" required></td>
                <td><input type="date" name="last_date[]"  placeholder="Last Date" required></td>
                <td><button type="button" class="removeRow">×</button></td>
            </tr>`;
        $('#experienceSection').append(newRow);
    }

    // Click handler for the 'Add More' button
    $('.addMoreBtn').click(function() {
        addNewRow();
    });

    // Remove row
    $(document).on('click', '.removeRow', function() {
        const row = $(this).closest('tr');
        const experienceId = $(this).data('id');
        if (experienceId) {
            $.ajax({
                url: '/delete_experience/' + experienceId,
                type: 'POST',
                data: {'csrf_token': "{{ csrf_token() }}"}, // Include CSRF token if CSRF protection is enabled
                success: function(response) {
                    row.remove(); // Remove the row from the DOM
                },
                error: function(error) {
                    console.error('Error:', error.responseText || 'Could not delete experience');
                    alert('Error deleting experience');
                }
            });
        } else {
            row.remove(); // For newly added rows which don't have an ID yet
        }
    });
    

    // Save button functionality
    $('.saveBtn').click(function(event) {
        event.preventDefault(); // Prevent default button click behavior

        // Submit the form
        $('#experienceForm').submit();
    });

    // Ensure there's at least one row on page load
    if ($('#experienceSection tr').length === 0) {
        addNewRow();
    }
});
