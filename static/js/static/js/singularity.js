cat > static/js/singularity.js << 'EOF'

let s=document.getElementById("singularity")

s.onclick=function(){

s.classList.add("explode")

setTimeout(()=>{

document.getElementById("singularityScreen").style.display="none"

document.getElementById("portalInterface").style.display="block"

},1500)

}

EOF