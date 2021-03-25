//Comment Slider
let commentsSwiper = new Swiper('.comments-swiper-container', {
    slidesPerView: 2,
    spaceBetween: 30,
    pagination: {
        el: '.comments-swiper-pagination',
        clickable: true,
    },
    navigation: {
        nextEl: '.comments-swiper-button-next',
        prevEl: '.comments-swiper-button-prev',
    },
    autoplay: {
        delay: 8000,
    },
    breakpoints: {
        0: {
            slidesPerView: 1,
        },

        992: {
            slidesPerView: 2,
        },

    }
});

//Article Slider
let articlesSwiper = new Swiper('.articles-swiper-container', {
    slidesPerView: 2,
    spaceBetween: 30,
    pagination: {
        el: '.articles-swiper-pagination',
        clickable: true,
    },
    navigation: {
        nextEl: '.articles-swiper-button-next',
        prevEl: '.articles-swiper-button-prev',
    },
    autoplay: {
        delay: 8000,
    },
    breakpoints: {
        0: {
            slidesPerView: 1,
        },
        600: {
            slidesPerView: 2,

        },
        1000: {
            slidesPerView: 3,
        },
    }
});

// let search = document.getElementById("search"); 
// search.onmousemove = function(e){
//     let box = document.getElementById("box");

//     box.style.top = e.clientY -search.scrollHeight + 40 + "px";
//     document.getElementById("box").style.left = e.pageX + "px";
// }

let headerList = document.getElementsByClassName("common-questions-header");
for (let index = 0; index < headerList.length; index++) {
    const element = headerList[index];
    element.addEventListener("click",function(){
        let parent = element.parentElement;
        let content = parent.getElementsByClassName("common-questions-content")[0];
        let iconList = document.getElementsByClassName("common-questions-header-icon");
        for (let i = 0; i < iconList.length; i++) {
            if(iconList[i].classList.contains("fa-minus")){
                iconList[i].classList.remove("fa-minus");
                iconList[i].classList.add("fa-plus");
            }
        }
        let icon = parent.getElementsByClassName("common-questions-header")[0].getElementsByClassName("common-questions-header-icon")[0];
        if(!content.classList.contains("show")){
            icon.classList.remove("fa-plus");
            icon.classList.add("fa-minus");
        }
        else{
            icon.classList.remove("fa-minus");
            icon.classList.add("fa-plus");
        }
    })
}
new WOW().init();
