    let listHedingThree = document.querySelectorAll(".article-left-description h3");
    let index = 0;
    listHedingThree.forEach(element => {
        index++;
        element.setAttribute('id', 'h' + index);
        let cannibalizationList = document.getElementsByClassName("article-left-cannibalization-list")[0];
        let childItem = document.createElement("li");
        childItem.classList.add("article-left-cannibalization-item");
        let childLink = document.createElement("a");
        childLink.setAttribute("href", "#h" + index);
        childLink.innerHTML = element.innerHTML;
        childItem.appendChild(childLink);
        cannibalizationList.appendChild(childItem);
        childLink.onclick = function(e) {
            if (this.hash !== "") {
                e.preventDefault();
                let hash = this.hash;
                $('html, body').animate({
                    scrollTop: $(hash).offset().top - 80
                }, 800);
            }
        }
    });