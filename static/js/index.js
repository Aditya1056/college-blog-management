replies = document.querySelectorAll(".view-replies");

// console.log(replies);

replies.forEach(element =>{
    element.addEventListener('click', (event)=>{
        // console.log(element.nextSibling.nextSibling);
        element.nextSibling.nextSibling.classList.toggle('active');
        childnodes = element.childNodes;
        icons = childnodes[1].childNodes;
        icons[3].classList.toggle('hide');
        icons[5].classList.toggle('hide');
    })
});

