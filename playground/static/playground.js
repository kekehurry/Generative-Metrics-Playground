// Playground
let box_size = 100;
let width = 10;
let height = 10;
let size = 10;
let state = Array.from({ length: size }, () => Array.from({ length: size }, () => Array(size).fill(0)));
let renderWidth = window.innerWidth*0.7;
let renderHeight = window.innerHeight;
let shift_distance = -150;
let linktoCityMatrix = false;

let isCtrl = false;
//RENDERER
let renderer = new THREE.WebGLRenderer( { antialias: true } );
renderer.setPixelRatio( window.devicePixelRatio );
renderer.setSize( renderWidth,renderHeight);
document.getElementById('sceneContainer').appendChild( renderer.domElement );
//CAMERA
let playground_scene = new THREE.Scene();
let playground_camera = new THREE.PerspectiveCamera( 45, renderWidth / renderHeight, 1, 10000 );
playground_camera.position.set( 100*width, 100*height, -140*height );
playground_camera.lookAt( 0, 0, 0 );
//ROLLOVER CUBE
let rollOverGeo = new THREE.BoxGeometry( box_size, box_size, box_size );
let rollOverMaterial = new THREE.MeshBasicMaterial( { color: 0xff0000, opacity: 0.5, transparent: true } );
let rollOverMesh = new THREE.Mesh( rollOverGeo, rollOverMaterial );
playground_scene.add( rollOverMesh );
// CUBE
let cubeGeo = new THREE.BoxGeometry( box_size, box_size, box_size );
let cubeMaterial1 = new THREE.MeshLambertMaterial( { color: 0x9C5D08} );
let cubeMaterial2 = new THREE.MeshLambertMaterial( { color: 0x08599C} );
let materialList = [];
materialList.push(cubeMaterial1);
materialList.push(cubeMaterial1);
materialList.push(cubeMaterial2);
//SUGGESTION CUBE
let suggestGeo = new THREE.BoxGeometry( box_size, box_size, box_size );
let suggestMaterial1 = new THREE.MeshBasicMaterial( { color: 0xfeb74c, opacity: 0.5, transparent: true } );
let suggestMaterial2 = new THREE.MeshBasicMaterial( { color: 0x559ced, opacity: 0.5, transparent: true } );
let suggestmaterialList = [];
suggestmaterialList.push(suggestMaterial1)
suggestmaterialList.push(suggestMaterial1)
suggestmaterialList.push(suggestMaterial2)
let suggestMesh = new THREE.Mesh( suggestGeo, suggestMaterial1 );
suggestMesh.position.set(0,0,0);
suggestMesh.position.divideScalar( box_size ).floor().multiplyScalar( box_size ).addScalar( box_size/2 );
let edges = new THREE.EdgesGeometry(suggestGeo);
let lineMaterial = new THREE.LineBasicMaterial({ color: 0xff0000, linewidth: 10 });
let suggestWireframe = new THREE.LineSegments(edges, lineMaterial);
playground_scene.add(suggestMesh);
playground_scene.add(suggestWireframe);
get_suggestion();
// GRID
let raycaster = new THREE.Raycaster();
let pointer = new THREE.Vector2();
let playground_gridHelper = new THREE.GridHelper( box_size*width, width );
playground_scene.add( playground_gridHelper );
// GROUND PLANE
let planeGeo = new THREE.PlaneGeometry( box_size*width, box_size*width );
planeGeo.rotateX( - Math.PI / 2 );
let plane = new THREE.Mesh( planeGeo, new THREE.MeshBasicMaterial( { visible: false } ) );
playground_scene.add( plane );
let objects = [];
objects.push(plane);
//LIGHT
let ambientLight = new THREE.AmbientLight( 0x606060,1);
playground_scene.add( ambientLight );
let directionalLight = new THREE.DirectionalLight( 0xffffff,1);
directionalLight.position.set( 1, 0.75, 0.5 ).normalize();
playground_scene.add( directionalLight );
//ORBIT CONTROL
let controls = new THREE.OrbitControls(playground_camera,renderer.domElement);
controls.mouseButtons = {
    MIDDLE: THREE.MOUSE.ROTATE, // 将中键设置为旋转
}

// playground_scene.traverse((object) => {
//     object.position.x += shift_distance;  // 'distance' is how far you want to move it to the left
// });

// loader
const loader = new THREE.OBJLoader();
loader.load( "/static/volpe.obj", function ( object ) {
    object.position.x +=  100;
    object.position.y +=  40;
    object.scale.setScalar( 10 );
    object.rotation.y += 0.5;
    var material = new THREE.MeshPhongMaterial({
        color: 0x282828,
        transparent: true,
        opacity: 0.8
    });
    object.traverse(function (child) {
        if (child.isMesh) {
            child.material = material;
        }
    });
    playground_scene.add( object );
    render();
});

//EVENTLISTENER
renderer.domElement.addEventListener( 'pointermove', onPointerMove );
renderer.domElement.addEventListener( 'pointerdown', onPointerDown );
document.addEventListener('keydown', function(event) {
    if (event.ctrlKey) {
        isCtrl = true;
    }
    if (event.key === 'p' || event.key === 'P') {
        autoPlay();
      }
});
document.addEventListener('keyup', function(event) {
    if (!event.ctrlKey) {
        isCtrl = false;
    }
});
window.addEventListener( 'resize', onWindowResize );

render();

// Define an async function to fetch server address
async function fetchServer() {
    try {
        const response = await fetch('/get_server_address', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        if (response.ok) {
            const data = await response.json();
            return data;
        } else {
            console.error('Failed to fetch scores');
        }
    } catch (error) {
        console.error('Error while fetching scores:', error);
    }
    return null;
}

// Define an async function to fetch suggestions
async function fetchSuggestion() {
    try {
        const response = await fetch('/get_suggestion', {
            method: 'POST',
            body: JSON.stringify(state),
            headers: {
                'Content-Type': 'application/json',
            },
        });
        if (response.ok) {
            const data = await response.json();
            return data;
        } else {
            console.error('Failed to fetch suggestion');
        }
    } catch (error) {
        console.error('Error while fetching suggestion:', error);
    }
    return null;
}
// Define an async function to fetch scores
async function fetchScores() {
    try {
        const response = await fetch('/get_score', {
            method: 'POST',
            body: JSON.stringify({'state':state,'link_to_citymatrix':linktoCityMatrix}),
            headers: {
                'Content-Type': 'application/json',
            },
        });
        if (response.ok) {
            const data = await response.json();
            return data;
        } else {
            console.error('Failed to fetch scores');
        }
    } catch (error) {
        console.error('Error while fetching scores:', error);
    }
    return null;
}

async function get_server(){
    const server_address = await fetchServer();
    return server_address.server_address
}

async function get_suggestion(){
    const suggestion = await fetchSuggestion();
    if (suggestion) {
    let action = suggestion.action;
    let t_;
    if(action<100){t_ = 1;}else{t_ = 2;};
    let i_ = Math.floor(action%100/width);
    let j_ = Math.floor(action%100%height);
    let k_ = state[i_][j_].filter(value => value !== 0).length;
    suggestMesh.material = suggestmaterialList[k_]
    suggestMesh.position.set(box_size*(i_-width/2),k_*box_size,box_size*(j_-height/2));
    suggestMesh.position.divideScalar( box_size ).floor().multiplyScalar( box_size ).addScalar( box_size/2 );
    suggestWireframe.position.set(box_size*(i_-width/2),k_*box_size,box_size*(j_-height/2));
    suggestWireframe.position.divideScalar( box_size ).floor().multiplyScalar( box_size ).addScalar( box_size/2 );
    console.log("suggest_location:(",i_,j_,k_,")","suggest_type:",t_)
    }
}

async function get_score(){
    const data = await fetchScores();
    if (data) {
    scoreHistory.push(data.scores);
    indexList = data.indexes;
    console.log(data.scores);
    console.log(data.indexes)
    updateRadarPlot();
    updateBarChart();
    }
}
function onPointerMove(event) {
    // Get the position of the renderer element
    const rendererElement = renderer.domElement;
    const rect = rendererElement.getBoundingClientRect();

    // Calculate the pointer position relative to the renderer's area
    pointer.set(
        ((event.clientX - rect.left) / rendererElement.clientWidth) * 2 - 1,
        -((event.clientY - rect.top) / rendererElement.clientHeight) * 2 + 1
    );

    raycaster.setFromCamera(pointer, playground_camera);
    const intersects = raycaster.intersectObjects(objects);

    if (intersects.length > 0) {
        const intersect = intersects[0];
        if (
            intersect.point.x >= -box_size * width / 2 &&
            intersect.point.x <= box_size * width / 2 &&
            intersect.point.z >= -box_size * height / 2 &&
            intersect.point.z <= box_size * height / 2
        ) {
            rollOverMesh.position.copy(intersect.point).add(intersect.face.normal);
            rollOverMesh.position.divideScalar(box_size).floor().multiplyScalar(box_size).addScalar(box_size / 2);
            
            render();
        }
    }
}

function onPointerDown(event) {
    // Get the position of the renderer element
    const rendererElement = renderer.domElement;
    const rect = rendererElement.getBoundingClientRect();
    
    // Calculate the pointer position relative to the renderer's area
    pointer.set(
        ((event.clientX - rect.left) / rendererElement.clientWidth) * 2 - 1,
        -((event.clientY - rect.top) / rendererElement.clientHeight) * 2 + 1
    );
    
    raycaster.setFromCamera(pointer, playground_camera);
    const intersects = raycaster.intersectObjects(objects);

    if (intersects.length > 0) {
        const intersect = intersects[0];
        // Create cube
        if ((event.button==0|event.button==2) && objects.length <= 100 && !isCtrl) {
            const voxel = new THREE.Mesh(cubeGeo, materialList[event.button]);

            // Set the position of the voxel to the intersection point
            voxel.position.copy(intersect.point).add( intersect.face.normal );;

            // Round the position to the nearest cube size
            voxel.position.divideScalar(box_size).floor().multiplyScalar(box_size).addScalar(box_size / 2);
            // Ensure that the voxel is within the grid bounds
            if (voxel.position.x >= -box_size * width / 2 && voxel.position.x <= box_size * width / 2 &&
                voxel.position.z >= -box_size * height / 2 && voxel.position.z <= box_size * height / 2){
                    let i_ = Math.ceil(voxel.position.x / box_size + width / 2)-1;
                    let j_ = Math.ceil(voxel.position.z / box_size + height / 2)-1;
                    let k_= state[i_][j_].filter(value => value !== 0).length;
                    playground_scene.add(voxel);
                    if (event.button==0){
                        state[i_][j_][k_] = 1
                    }else{
                        state[i_][j_][k_] = 2
                    }
                    objects.push(voxel);
                    get_suggestion();
                    get_score();
                    render();
                    console.log("add_cube_location:", i_, j_, k_, "remain_num:", 100 - objects.length + 1);
            }
        }
        // Delete cube
        if ( isCtrl) {
        if ( intersect.object !== plane ) {
            let i_ = Math.ceil(intersect.object.position.x / box_size + width / 2)-1;
            let j_ = Math.ceil(intersect.object.position.z / box_size + height / 2)-1;
            let z_= state[i_][j_].filter(value => value !== 0).length-1;
            state[i_][j_][z_] = 0;
            playground_scene.remove( intersect.object );
            objects.splice( objects.indexOf( intersect.object ), 1 );
            get_suggestion();
            get_score();
            render();
            console.log("add_cube_location:", i_, j_, z_, "remain_num:", 100 - objects.length + 1);
            }
        }
        }
}

async function autoPlay(){
    if(objects.length<=100){
        const suggestion = await fetchSuggestion();
        if (suggestion) {
        let action = suggestion.action;
        let t_;
        if(action<100){t_ = 1;}else{t_ = 2;};
        let i_ = Math.floor(action%100/width);
        let j_ = Math.floor(action%100%height);
        let k_ = state[i_][j_].filter(value => value !== 0).length;
        const voxel = new THREE.Mesh(cubeGeo, materialList[t_]);
        voxel.position.set(box_size*(i_-width/2),k_*box_size,box_size*(j_-height/2));
        voxel.position.divideScalar( box_size ).floor().multiplyScalar( box_size ).addScalar( box_size/2 );
        state[i_][j_][k_] = t_
        objects.push(voxel);
        playground_scene.add(voxel);
        get_score();
        render();
        console.log("add_cube_location:", i_, j_, k_, "remain_num:", 100 - objects.length + 1);
    }}
}

let linkButton = document.getElementById('linkButton')
linkButton.addEventListener('click', function() {
    linktoCityMatrix = !linktoCityMatrix
    fetchServer().then(maxtrixServerAddr => {
        fetch(maxtrixServerAddr.server_address)
        .then(response => {
            if (response.ok) {
                if(linktoCityMatrix){
                    window.open(maxtrixServerAddr.server_address, '_blank');
                    linkButton.innerText = "Stop Link";
                }else{
                    linkButton.innerText = "Link to City Matrix"
                }
            } else {
                linkButton.innerText = "Server Not working";
            }
        })
        .catch(error => {
            linkButton.innerText = "Error";
        });
   });
});

function onWindowResize() {
    //renderer resize
    renderWidth = window.innerWidth*0.8;
    renderHeight = window.innerHeight;
    //camera reset
    playground_camera.aspect = renderWidth / renderHeight;
    playground_camera.updateProjectionMatrix();
    renderer.setSize( renderWidth, renderHeight );
}

function render() {
    renderer.render( playground_scene, playground_camera );
}