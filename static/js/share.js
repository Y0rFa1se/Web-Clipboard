document.addEventListener('DOMContentLoaded', () => {
    const shareButton = document.querySelector('.share_button');

    shareButton.addEventListener('click', event => {
        console.log("clicked");

        if (navigator.share) { 
        navigator.share({
            title: "share content",
            url: window.location.href
        })}
        else {
            alert("Your browser does not support Web Share API");
        }
    });
});