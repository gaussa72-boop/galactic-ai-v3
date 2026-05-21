window.addEventListener('load', () => { 
    const images = ['nebula1.jpg','galaxy2.jpg','singularity3.jpg']; // Bilder im static/images Ordner
    const bg = document.getElementById('background');
    let i=0;
    setInterval(()=>{
        bg.style.backgroundImage='url("/static/images/'+images[i]+'")';
        i=(i+1)%images.length;
    }, 10000); // alle 10s Bildwechsel

    setTimeout(()=>{
        document.getElementById('loader').style.display='none';
        document.getElementById('interface').style.display='block';
    },2500); 
});

async function sendMessage(aiType){
    const msg = document.getElementById('userMessage').value;
    if(!msg) return;
    const response = await fetch('/chat',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ai: aiType, message: msg})
    });
    const data = await response.json();
    const log = document.getElementById('chatLog');

    // Goldene Partikel
    const particle = document.createElement('span');
    particle.className='gold-particle';
    particle.style.left = Math.random()*80 + '%';
    particle.style.top = Math.random()*80 + '%';
    log.appendChild(particle);
    setTimeout(()=>{particle.remove();},1500);

    log.innerHTML += '<div><b>Du:</b> '+msg+'</div><div><b>'+aiType.toUpperCase()+':</b> '+data.reply+'</div>';
    document.getElementById('userMessage').value='';
    log.scrollTop=log.scrollHeight;

    // Wunderland Charakter sprechen lassen
    const wonderlandChar = document.getElementById('wunderland-character');
    wonderlandChar.innerText = '🐇 "'+data.reply+'"';
    speak(data.reply);
}

function speak(text){
    if('speechSynthesis' in window){
        const utter = new SpeechSynthesisUtterance(text);
        utter.lang='de-DE';
        utter.voice=speechSynthesis.getVoices()[0];
        speechSynthesis.speak(utter);
    }
}
