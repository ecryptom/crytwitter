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


let sendReplyIcon = document.querySelectorAll(".fa.fa-reply.product-comments-footer-icon");
let sendReplyBox = document.querySelectorAll(".product-comments-send-reply");


sendReplyIcon.forEach(element => {
    element.addEventListener("click", function (e) {
        let firstParent = e.target.parentElement.parentElement;
        let replyBox = firstParent.querySelector(".product-comments-send-reply");
        if (replyBox == null) {
            let replyComments = firstParent.querySelector(".product-comments-reply");
            let replyElement = document.createElement("div");
            replyElement.classList.add("product-comments-send-reply");
            replyElement.innerHTML = "  <form action='' method=''><textarea placeholder='متن دیدگاه' class='product-comments-send-reply-text-area'></textarea><button type='submit' class='product-comments-send-reply-submit'>ارسال پاسخ</button></form>";
            firstParent.insertBefore(replyElement, replyComments);
            replyElement.style.height = replyElement.scrollHeight + "px";
            e.target.classList.add("product-comments-footer-icon-close");
        } else if (getComputedStyle(replyBox).height == "0px") {
            replyBox.style.height = replyBox.scrollHeight + "px";
            e.target.classList.add("product-comments-footer-icon-close");
        } else {
            replyBox.style.height = "0px";
            e.target.classList.remove("product-comments-footer-icon-close");
            setTimeout(function(){
                firstParent.removeChild(replyBox);
            },1000);
        }
    })
});
