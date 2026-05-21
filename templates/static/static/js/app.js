const canvas = document.getElementById('nebulaCanvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let stars = [];
for(let i=0;i<200;i++){
    stars.push({x:Math.random()*canvas.width, y:Math.random()*canvas.height, r:Math.random()*1.5, dx:(Math.random()-0.5)*0.5, dy:(Math.random()-0.5)*0.5});
}

function drawStars(){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    for(let s of stars){
        ctx.beginPath();
        ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
        ctx.fillStyle='rgba(200,200,255,0.8)';
        ctx.fill();
        s.x+=s.dx; s.y+=s.dy;
        if(s.x>canvas.width)s.x=0;
        if(s.x<0)s.x=canvas.width;
        if(s.y>canvas.height)s.y=0;
        if(s.y<0)s.y=canvas.height;
    }
    requestAnimationFrame(drawStars);
}
drawStars();

setTimeout(()=>{
    document.getElementById('loader').style.display='none';
    document.getElementById('mainPortal').style.display='block';
}, 3000);

function callIonos(){
    fetch('/call_ionos', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({message:'Hi'})})
    .then(res=>res.json())
    .then(data=>document.getElementById('output').innerText=data.response);
}

function callUrspirit(){
    fetch('/call_urspirit', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({message:'Hallo'})})
    .then(res=>res.json())
    .then(data=>document.getElementById('output').innerText=data.response);
}