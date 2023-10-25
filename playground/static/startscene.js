// 开场
let start_scene = new THREE.Scene();
let start_camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
let renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('sceneContainer').appendChild(renderer.domElement);

let start_gridHelper = new THREE.GridHelper(20, 30); // 这会创建一个大小为10x10的网格，总共有10个分割
start_scene.add(start_gridHelper);
start_gridHelper.position.y -= 1

let geometry = new THREE.BoxGeometry(1, 1, 1);

// 创建三个材质
let materials = [
    new THREE.MeshBasicMaterial({ color: 0xff0000 }),
    new THREE.MeshBasicMaterial({ color: 0x00ff00 }),
    new THREE.MeshBasicMaterial({ color: 0x0000ff })
];

// 创建三个方块并设置不同的位置
let cubes = materials.map(material => {
    let cube = new THREE.Mesh(geometry, material);
    start_scene.add(cube);
    return cube;
});
cubes[0].position.x -= 3;
cubes[0].position.y += 0;
cubes[0].position.z -= 1;
cubes[1].position.x += 2;
cubes[1].position.y += 1;
cubes[1].position.z -= 2;
cubes[2].position.x += 1.2;
cubes[2].position.y += 0.5;
cubes[2].position.z += 1.5;

// 设置相机的位置
start_camera.position.x = 2; // 从X轴的正方向移动
start_camera.position.y = 2; // 从Y轴的正方向移动
start_camera.position.z = 5; // 从Z轴的正方向移动
start_camera.lookAt(start_scene.position);

//渲染函数
let is_start_scence = true;
function animate() {
    if(is_start_scence){
        requestAnimationFrame(animate);
    cubes.forEach(cube => {
        cube.rotation.x += 0.01;
        cube.rotation.y += 0.01;
    });

    renderer.render(start_scene, start_camera);
    }
}
animate();

// function switch_scene() {
//     const echartsContainer = document.getElementById('echartsContainer');
//     const playButton = document.getElementById('playButton');
//     const title = document.querySelector('h1');
//     // 切换Echarts图表的可见性
//     echartsContainer.style.display = 'block';
//     setTimeout(() => {
//         initRadarChart();
//         initBarChart();
//     }, 100);

//     // 隐藏playButton和标题
//     playButton.style.display = 'none';
//     title.style.display = 'none';
//     is_start_scence = false;
//     renderer.render(playground_scene,playground_camera);
//     renderer.domElement.addEventListener( 'pointermove', onPointerMove );
//     renderer.domElement.addEventListener( 'pointerdown', onPointerDown );
// }

function switch_scene() {
    window.location.href = "/playground";
}

document.getElementById('playButton').addEventListener('click', function() {
    switch_scene()
});

window.addEventListener( 'resize', onWindowResize );
function onWindowResize() {
    //renderer resize
    renderWidth = window.innerWidth*0.8;
    renderHeight = window.innerHeight;
    //camera reset
    start_camera.aspect = renderWidth / renderHeight;
    start_camera.updateProjectionMatrix();
    renderer.setSize( renderWidth, renderHeight );
}
