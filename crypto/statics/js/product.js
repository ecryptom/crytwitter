let gallerySwiper = new Swiper('.product-features-picture-gallery-swiper-container', {
    slidesPerView: 2,
    spaceBetween: 30,
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
    autoplay: {
        delay: 1000,
    },
});