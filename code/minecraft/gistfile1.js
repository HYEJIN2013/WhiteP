var texture = THREE.ImageUtils.loadTexture( file );texture.wrapS = THREE.ClampToEdgeWrapping;texture.wrapT = THREE.ClampToEdgeWrapping;texture.magFilter = THREE.NearestFilter;texture.minFilter = THREE.LinearMipMapLinearFilter;
