function runAI(type){

fetch("/"+type)

.then(r=>r.json())

.then(data=>{

document.getElementById("chatbox").innerHTML =
data.reply

})

}