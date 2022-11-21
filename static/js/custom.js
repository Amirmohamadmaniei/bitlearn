function reply(comment_id) {
    const parent = document.getElementById('parent')
    location.href = "#text_comment"
    parent.setAttribute('value', comment_id)
}


// function filter(f) {
//     window.location.href = `https//localhost:8000/course/filter/?f=${f}`;
// }

function category(c) {
    window.location.href = `category?c=${c}`;
}



function PlayVideo(srcVideo) {
    var video = document.getElementById('video1');
    video.setAttribute('src', srcVideo);
    video.play();
}

