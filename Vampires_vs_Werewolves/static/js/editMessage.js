window.addEventListener('DOMContentLoaded', () => {
    const editButtons = document.querySelectorAll('.fa-pencil');
    const messageForm = document.querySelector('form');

    editButtons.forEach((editButton) => {
        editButton.addEventListener('click', event => {
            if (event) {
                editButtons.forEach(editButton => {
                    editButton.style.pointerEvents = 'none'
                    editButton.style.cursor = 'auto'
                });
            }
            const currentDiv = event.target.parentElement.parentElement.parentElement;
            const messageId = event.target.parentElement.parentElement.id;
            const messageElement = currentDiv.querySelector('.message-content');
            const messageTextArea = messageForm.querySelector('textarea');
            messageTextArea.value = messageElement.textContent.trim();
            const sendButton = messageForm.querySelector('.item-button');
            sendButton.textContent = 'Edit message';
            const BASE_URL = `http://127.0.0.1:8000/messages/edit-message/${messageId}/`;

            sendButton.addEventListener('click', (event) => {
                event?.preventDefault();
                const updatedMessage = messageTextArea.value.trim();
                const csrfToken = getCSRFToken();

                fetch(BASE_URL, {
                     method: 'PUT',
                     headers: {
                         'Content-Type': 'application/json',
                         'X-CSRFToken': csrfToken
                     },
                     body: JSON.stringify({
                         "content": updatedMessage,
                     })
                })
                .then((response) => response.json())
                .then((data) => {
                    messageTextArea.value = '';
                    sendButton.textContent = 'Send ';
                    const iElement = document.createElement('i');
                    iElement.classList.add('fa-solid', 'fa-envelope');
                    sendButton.innerHTML = 'Send ';
                    sendButton.appendChild(iElement);
                    messageElement.textContent = data['updated_message'].content;
                    editButtons.forEach(editButton => {
                    editButton.style.pointerEvents = 'auto';
                });

                })
                .catch((error) => {
                    console.log(error);
                });
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
