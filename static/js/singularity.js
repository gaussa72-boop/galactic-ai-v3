const singularity = document.getElementById("singularity")

singularity.onclick = function(){

singularity.classList.add("explode")

setTimeout(()=>{

document.getElementById("singularity-container").style.display="none"

document.getElementById("portal").style.display="block"

},1500)

}