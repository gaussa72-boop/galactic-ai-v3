cat > static/js/lebensblume.js << 'EOF'

const canvas=document.createElement("canvas")

document.body.appendChild(canvas)

const ctx=canvas.getContext("2d")

canvas.width=window.innerWidth
canvas.height=window.innerHeight

function drawCircle(x,y,r){

ctx.beginPath()
ctx.arc(x,y,r,0,Math.PI*2)
ctx.strokeStyle="gold"
ctx.stroke()

}

function drawFlower(){

ctx.clearRect(0,0,canvas.width,canvas.height)

let centerX=canvas.width/2
let centerY=canvas.height/2

for(let i=0;i<6;i++){

let angle=i*(Math.PI/3)

let x=centerX+Math.cos(angle)*60
let y=centerY+Math.sin(angle)*60

drawCircle(x,y,60)

}

drawCircle(centerX,centerY,60)

}

setInterval(drawFlower,100)

EOF