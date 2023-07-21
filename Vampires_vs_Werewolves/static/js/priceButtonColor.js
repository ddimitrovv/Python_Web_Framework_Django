window.addEventListener('DOMContentLoaded', () => {
    const heroGold = Number(document.getElementsByClassName('hero-gold')[0]
        .textContent.replace('Gold: ', ''));
    const costElements = document.querySelectorAll('.cost');

    costElements.forEach(element => {
        const cost = Number(element.textContent.replace('Cost: ', ''));
        if (heroGold < cost) {
            element.previousElementSibling.
                querySelector('.profile-upgrade .fa-solid.fa-square-plus').
                style.color = '#f3efec'; // change the color from red to gray when not enough money
            element.previousElementSibling.children[0].
                style.pointerEvents = 'none'; // Prevent clicking on the link when not enough money
        }
    });
});