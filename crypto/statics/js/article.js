    let listHedingThree = document.querySelectorAll(".article-left-description h3");
let index = 0;
listHedingThree.forEach(element => {
    index++;
    element.setAttribute('id','h' + index);
    let cannibalizationList = document.getElementsByClassName("article-left-cannibalization-list")[0];
    let childItem = document.createElement("li");
    childItem.classList.add("article-left-cannibalization-item");
    let childLink = document.createElement("a");
    childLink.setAttribute("href" , "#h" + index);
    childLink.innerHTML = element.innerHTML;
    childItem.appendChild(childLink);
    cannibalizationList.appendChild(childItem);
    childLink.onclick = function(e){
        if (this.hash !== "") {
            e.preventDefault();
            let hash = this.hash;
            $('html, body').animate({
                scrollTop: $(hash).offset().top - 80
            },800);
        }
    }
});

    let sendReplyIcon = document.querySelectorAll(".fa.fa-reply.article-left-comments-footer-icon");
    let sendReplyBox = document.querySelectorAll(".article-left-comments-send-reply");
   
  
    sendReplyIcon.forEach(element => {
        element.addEventListener("click", function (e) {
            let firstParent = e.target.parentElement.parentElement;
            let replyBox = firstParent.querySelector(".article-left-comments-send-reply");
            if (replyBox == null) {
                let replyComments = firstParent.querySelector(".article-left-comments-reply");
                let replyElement = document.createElement("div");
                replyElement.classList.add("article-left-comments-send-reply");
                replyElement.innerHTML = "  <form action='' method=''><textarea placeholder='متن دیدگاه' class='article-left-comments-send-reply-text-area'></textarea><button type='submit' class='article-left-comments-send-reply-submit'>ارسال پاسخ</button></form>";
                firstParent.insertBefore(replyElement, replyComments);
                replyElement.style.height = replyElement.scrollHeight + "px";
                e.target.classList.add("article-left-comments-footer-icon-close");
            } else if (getComputedStyle(replyBox).height == "0px") {
                replyBox.style.height = replyBox.scrollHeight + "px";
                e.target.classList.add("article-left-comments-footer-icon-close");
            } else {
                replyBox.style.height = "0px";
                e.target.classList.remove("article-left-comments-footer-icon-close");
                setTimeout(function(){
                    firstParent.removeChild(replyBox);
                },1000);
            }
        })
    });
