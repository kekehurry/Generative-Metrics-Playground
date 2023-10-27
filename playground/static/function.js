
let genButton = document.getElementById('genButton')
genButton.addEventListener('click', map_unit);

function map_unit(){
    let unitGeo = new THREE.BoxGeometry( box_size, box_size/3, box_size );
    let unitMaterial;
    for(let i=1;i<objects.length;i++){
        for(let j=-1;j<2;j++){
            height = objects[i].position.y+box_size/3*j
            if(height >=10*box_size/3){
                unitMaterial = new THREE.MeshLambertMaterial( { color: 0x08599C} );
            }else if(height <= 2*box_size/3){
                unitMaterial = new THREE.MeshLambertMaterial( { color: 0xff0000} );
            }else{
                unitMaterial = new THREE.MeshLambertMaterial( { color: 0x9C5D08} );
            }
            let voxel_ = new THREE.Mesh( unitGeo, unitMaterial);
            voxel_.position.set(objects[i].position.x,objects[i].position.y+box_size/3*j,objects[i].position.z);
            let unitEdges = new THREE.EdgesGeometry(unitGeo);
            let unitlineMaterial = new THREE.LineBasicMaterial({ color: 0x000000, linewidth: 10 });
            let unitWireframe = new THREE.LineSegments(unitEdges, unitlineMaterial);
            unitWireframe.position.copy(voxel_.position)
            playground_scene.add(voxel_);
            playground_scene.add(unitWireframe);
            playground_scene.remove(objects[i]);
            playground_scene.remove(suggestMesh);
            playground_scene.remove(rollOverMesh);
            renderer.domElement.removeEventListener( 'pointerdown', onPointerDown );
            render();
        }
    }
}
