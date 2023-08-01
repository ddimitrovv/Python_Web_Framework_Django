window.addEventListener('DOMContentLoaded', () => {
    const items = document.querySelectorAll('.item-details')
    items.forEach(element => {
        const price = Number(element.querySelector('.item-price')
            .textContent.replace('Price: ', ''));
        const button = element.querySelector('button')
        const heroGold = Number(button.id)
        if (heroGold < price) {
            button.style.background = '#f3efec'; // Change the color from red to gray when not enough money
            button.style.pointerEvents = 'none'; // Prevent clicking on the link when not enough money
        }
    });
});