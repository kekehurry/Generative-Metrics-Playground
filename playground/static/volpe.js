// 开场
import * as THREE from 'https://threejsfundamentals.org/threejs/resources/threejs/r119/build/three.module.js';
import { OBJLoader } from 'https://threejsfundamentals.org/threejs/resources/threejs/r119/examples/jsm/loaders/OBJLoader.js';
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.127.0/examples/jsm/controls/OrbitControls.js';

let start_scene = new THREE.Scene();
let start_camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
let renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('sceneContainer').appendChild(renderer.domElement);

let start_gridHelper = new THREE.GridHelper(20, 30);
start_scene.add(start_gridHelper);
start_gridHelper.position.y -= 1

//light
const ambientLight = new THREE.AmbientLight( 0xffffff );
start_scene.add( ambientLight );
const pointLight = new THREE.PointLight( 0xffffff, 1);
start_scene.add( pointLight );

// loader
const loader = new OBJLoader();
let objModel;
loader.load( "/static/volpe.obj", function ( object ) {
    object.position.y -=  0.5;
    object.scale.setScalar( 0.01 );
    var material = new THREE.MeshPhongMaterial({
        color: 0x282828,
        transparent: true,
        opacity: 0.8
    });
    object.traverse(function (child) {
        if (child.isMesh) {
            child.material = material;
        }
    objModel = object;
    });
    start_scene.add( object );
    render();
});

function switch_scene() {
    window.location.href = "/playground";
}

document.getElementById('playButton').addEventListener('click', function() {
    switch_scene()
});

function render() {
    renderer.render( start_scene, start_camera );
}

window.addEventListener( 'resize', onWindowResize );
function onWindowResize() {
    //renderer resize
    renderWidth = window.innerWidth*0.8;
    renderHeight = window.innerHeight;
    //camera reset
    start_camera.aspect = renderWidth / renderHeight;
    start_camera.updateProjectionMatrix();
    renderer.setSize( renderWidth, renderHeight );
    render();
}


// let geometry = new THREE.BoxGeometry(1, 1, 1);

// // 创建三个材质
// let materials = [
//     new THREE.MeshBasicMaterial({ color: 0xff0000 }),
//     new THREE.MeshBasicMaterial({ color: 0x00ff00 }),
//     new THREE.MeshBasicMaterial({ color: 0x0000ff })
// ];

// // 创建三个方块并设置不同的位置
// let cubes = materials.map(material => {
//     let cube = new THREE.Mesh(geometry, material);
//     start_scene.add(cube);
//     return cube;
// });
// //红色
// cubes[0].position.x -= 1;
// cubes[0].position.y += 0.3;
// cubes[0].position.z -= 8;
// //绿色
// cubes[1].position.x -= 1.5;
// cubes[1].position.y += 1;
// cubes[1].position.z -= 3;
// //蓝色
// cubes[2].position.x += 2.5;
// cubes[2].position.y += 0.5;
// cubes[2].position.z -= 5;

// //渲染函数
// function animate() {
//         requestAnimationFrame(animate);
//     cubes.forEach(cube => {
//         cube.rotation.x += 0.01;
//         cube.rotation.y += 0.01;
//     });

//     renderer.render(start_scene, start_camera);
// }
// animate();

