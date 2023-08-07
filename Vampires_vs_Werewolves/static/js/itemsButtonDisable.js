window.addEventListener('DOMContentLoaded', () => {
    const items = document.querySelectorAll('.item-details')
    items.forEach(element => {
        const priceElement = element.querySelector('.item-price')
        const price = Number(priceElement.textContent.replace('Price: ', ''));
        const button = element.querySelector('button')
        const heroGold = Number(priceElement.id)
        const requiredLevel = Number(element.querySelector('.required-level')
            .textContent.replace('Required level: ', ''));
        const heroLevel = Number(element.querySelector('.required-level').id)
        if ((heroGold < price) || (requiredLevel > heroLevel)) {
            button.style.background = '#f3efec'; // Change the color from red to gray when not enough money
            button.style.pointerEvents = 'none'; // Prevent clicking on the link when not enough money
        }
    });
});