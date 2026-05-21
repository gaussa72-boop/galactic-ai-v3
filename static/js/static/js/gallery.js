cat > static/js/gallery.js << 'EOF'

async function loadImages(){

let r = await fetch("/images")

let images = await r.json()

let container = document.getElementById("imageGallery")

container.innerHTML=""

images.forEach(img=>{

let el=document.createElement("img")

el.src="/static/images/"+img

el.className="galaxyImage"

container.appendChild(el)

})

}

window.onload = loadImages

EOF}