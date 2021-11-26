const burger = document.querySelector('.header__burger');
burger.addEventListener('click', () => {
    const navbar = document.querySelector('.header__navbar');
    const body = document.querySelector('body')
    burger.classList.toggle('active');
    navbar.classList.toggle('active');
    body.classList.toggle('lock');

})
