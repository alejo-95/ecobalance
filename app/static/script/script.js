let btn = document.querySelector('#btn');
let sidebar = document.querySelector('.sidebar');

btn.onclick = function () {
    sidebar.classList.toggle('active');
};

// Animación de puntos
function animatePoints() {
    let currentPoints = 0;
    const targetPoints = 5250;
    const duration = 2000; // 2 segundos
    const interval = 20; // Actualizar cada 20ms
    const increment = targetPoints / (duration / interval);
    const pointsDisplay = document.getElementById('pointsDisplay');

    const timer = setInterval(() => {
        currentPoints += increment;
        if (currentPoints >= targetPoints) {
            clearInterval(timer);
            currentPoints = targetPoints;
        }
        pointsDisplay.textContent = Math.round(currentPoints).toLocaleString();
    }, interval);
}

// Carrusel infinito 
const carousel = document.getElementById('carousel');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
let currentIndex = 0;
let cardWidth;
let carouselWidth;
let totalCards;

function setupCarousel() {
    const cards = carousel.children;
    totalCards = cards.length;
    cardWidth = cards[0].offsetWidth + parseInt(window.getComputedStyle(cards[0]).marginRight);
    carouselWidth = cardWidth * totalCards;

    // Clonar todas las tarjetas y añadirlas al final
    for (let i = 0; i < totalCards; i++) {
        const clone = cards[i].cloneNode(true);
        carousel.appendChild(clone);
    }

    // Ajustar el ancho del carrusel
    carousel.style.width = `${carouselWidth * 2}px`;

    updateCarousel();
}

function updateCarousel() {
    const offset = -currentIndex * cardWidth;
    carousel.style.transform = `translateX(${offset}px)`;

    // reiniciar sin transición
    if (currentIndex >= totalCards) {
        setTimeout(() => {
            carousel.style.transition = 'none';
            currentIndex = 0;
            updateCarousel();
            setTimeout(() => {
                carousel.style.transition = 'transform 0.5s ease';
            }, 50);
        }, 500);
    }
}

function nextSlide() {
    currentIndex++;
    updateCarousel();
}

function prevSlide() {
    if (currentIndex === 0) {
        currentIndex = totalCards - 1;
        carousel.style.transition = 'none';
        updateCarousel();
        setTimeout(() => {
            carousel.style.transition = 'transform 0.5s ease';
            currentIndex--;
            updateCarousel();
        }, 50);
    } else {
        currentIndex--;
        updateCarousel();
    }
}

prevBtn.addEventListener('click', prevSlide);
nextBtn.addEventListener('click', nextSlide);

// Transición automática
setInterval(nextSlide, 5000);

// Iniciar animaciones cuando se carga la página
window.addEventListener('load', () => {
    animatePoints();
    setupCarousel();
});

// Ajustar el carrusel si cambia el tamaño de la ventana
window.addEventListener('resize', setupCarousel);

//Abrir el modal

// $(document).ready(function () {
//     $('#userModal').modal('show');
// });