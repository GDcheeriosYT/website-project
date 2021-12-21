function test(num){
    const img = document.querySelector("img[test='" + num + "']")
    if (img.getAttribute("did-init")) return;
    setTimeout(function(){
        img.setAttribute("did-init", true)
        startGallery(img, window.currentMatches[num], num, true)
        
    }, getRandomInt(30) * 100)
}

function startGallery(img, imgArray, num, useRandom){
    img.setAttribute("current-index", 0)
    setInterval(function(){
        let myParent = document.querySelector("div[test='" + num + "']")
        //index managing
        let currentIndex = parseFloat(img.getAttribute("current-index"))
        let nextIndex 
        if (!useRandom){
            nextIndex = currentIndex + 1
            if (imgArray.length - 1 < nextIndex){
                nextIndex = 0
            }
        }
        else{
            nextIndex = getRandomInt(imgArray.length)
        }
        //instantiate new image
        let newImage = document.createElement("img")
        newImage.setAttribute("did-init", true)
        newImage.setAttribute("current-index", nextIndex)
        newImage.src = imgArray[nextIndex]
        myParent.appendChild(newImage)
        img.classList.add("fade");
        setTimeout(function(){
            img.remove()
            img = newImage
        }, 3000)
        
    }, 4000)
}

function getRandomInt(max){
    return Math.floor(Math.random() * max);
}

function randomizeGallery(){

}
  
window.currentMatches = []