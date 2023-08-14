window.addEventListener('DOMContentLoaded', () => {
    const deleteButtons = document.querySelectorAll('.fa-trash');

    deleteButtons.forEach((deleteButton) => {
        deleteButton.addEventListener('click', event => {
            event?.preventDefault();
            const currentDiv = event.target.parentElement.parentElement.parentElement;
            const messageId = event.target.parentElement.parentElement.id;
            const BASE_URL = `http://127.0.0.1:8000/messages/delete-message/${messageId}/`;

            const csrfToken = getCSRFToken();

            fetch(BASE_URL, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => {
                if (response.status === 204) {
                    currentDiv.remove()
                } else {
                    console.log('Message not found!')
                }
            })

            .catch(error => {
                console.log(error);
            });
        });
    });
});


function getCSRFToken() {
    const cookies = document.cookie.split('; ');
    for (const cookie of cookies) {
        const [name, value] = cookie.split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return null; // CSRF token not found
}
