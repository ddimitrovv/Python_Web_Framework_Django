  // // JavaScript to make the carousel slide when clicked
  // (function() {
  //   const carousel = document.querySelector('.carousel');
  //   const slides = carousel.querySelectorAll('.slide');
  //   const totalSlides = slides.length;
  //   let currentSlide = 0;
  //
  //   function showSlide(slideIndex) {
  //     if (slideIndex < 0 || slideIndex >= totalSlides) {
  //       return;
  //     }
  //
  //     const slideWidth = slides[0].clientWidth;
  //     carousel.style.transform = `translateX(-${slideWidth * slideIndex}px)`;
  //     currentSlide = slideIndex;
  //   }
  //
  //   function showNextSlide() {
  //     currentSlide = (currentSlide + 1) % totalSlides;
  //     showSlide(currentSlide);
  //   }
  //
  //   function showPreviousSlide() {
  //     currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
  //     showSlide(currentSlide);
  //   }
  //
  //   // Add click event listeners to the carousel container
  //   carousel.addEventListener('click', function(event) {
  //     // Calculate the position of the click relative to the carousel container
  //     const clickX = event.clientX - carousel.getBoundingClientRect().left;
  //     const slideWidth = slides[0].clientWidth;
  //
  //     if (clickX < slideWidth / 2) {
  //       // Clicked on the left half of the carousel, show previous slide
  //       showPreviousSlide();
  //     } else {
  //       // Clicked on the right half of the carousel, show next slide
  //       showNextSlide();
  //     }
  //   });
  // })();


const slides = document.querySelectorAll(".slide");
const slideContainer = document.querySelector(".carousel");

// Set the initial slide index and display the first slide
let currentSlide = 0;
slides[currentSlide].classList.remove("hidden");

function showSlide(index) {
    slides.forEach((slide) => slide.classList.add("hidden"));
    slides[index].classList.remove("hidden");
}

function nextSlide() {
    if (currentSlide < slides.length - 1) {
        currentSlide++;
    } else {
        currentSlide = 0;
    }
    showSlide(currentSlide);
}

function prevSlide() {
    if (currentSlide > 0) {
        currentSlide--;
    } else {
        currentSlide = slides.length - 1;
    }
    showSlide(currentSlide);
}

// Event listeners for next and previous buttons
const nextBtn = document.getElementById("nextBtn");
const prevBtn = document.getElementById("prevBtn");
nextBtn.addEventListener("click", nextSlide);
prevBtn.addEventListener("click", prevSlide);

