
const scene = new THREE.Scene()

const camera = new THREE.PerspectiveCamera(75,window.innerWidth/window.innerHeight,0.1,1000)

const renderer = new THREE.WebGLRenderer()

renderer.setSize(window.innerWidth,window.innerHeight)

document.body.appendChild(renderer.domElement)

const starsGeometry = new THREE.BufferGeometry()

const starsCount = 5000

const posArray = new Float32Array(starsCount * 3)

for(let i=0;i<starsCount*3;i++){

posArray[i]=(Math.random()-0.5)*1000

}

starsGeometry.setAttribute('position',new THREE.BufferAttribute(posArray,3))

const starsMaterial = new THREE.PointsMaterial({color:0xffffff})

const starsMesh = new THREE.Points(starsGeometry,starsMaterial)

scene.add(starsMesh)

camera.position.z = 5

function animate(){

requestAnimationFrame(animate)

starsMesh.rotation.y += 0.0005

renderer.render(scene,camera)

}

animate()

