document.getElementById('publishGame').addEventListener('click', publishGame);

// Сохранение игры как Blob и отправка
function publishGame() {
    // Генерация HTML-кода игры
    const html = `
<!DOCTYPE html>
<html>
<head>
    <title>My Game - Made with T-studio</title>
    <style>
        body { margin: 0; overflow: hidden; }
        #madeBy { position: absolute; top: 20px; left: 20px; background: rgba(0,0,0,0.7); color: white; padding: 10px; z-index: 100; }
    </style>
</head>
<body>
    <div id="madeBy">Made by T-studio</div>
    <canvas id="gameCanvas"></canvas>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        // Тут должен быть код сцены из твоего конструктора
        // Это упрощённый пример
        let scene = new THREE.Scene();
        scene.background = new THREE.Color(0x87CEEB);
        let camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 5, 10);
        let renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('gameCanvas') });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.shadowMap.enabled = true;

        const planeGeometry = new THREE.PlaneGeometry(20, 20);
        const planeMaterial = new THREE.MeshStandardMaterial({ color: 0x2E8B57 });
        const plane = new THREE.Mesh(planeGeometry, planeMaterial);
        plane.rotation.x = -Math.PI / 2;
        plane.receiveShadow = true;
        scene.add(plane);

        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        scene.add(ambientLight);
        const light = new THREE.DirectionalLight(0xffffff, 1);
        light.position.set(10, 20, 10);
        light.castShadow = true;
        scene.add(light);

        function animate() {
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
    `;

    const blob = new Blob([html], { type: 'text/html' });
    const file = new File([blob], 'game.html', { type: 'text/html' });

    const formData = new FormData();
    formData.append('title', prompt('Название проекта:') || 'Без названия');
    formData.append('description', prompt('Описание проекта:') || 'Нет описания');
    formData.append('html_file', file);

    // Для превью можно использовать canvas.toDataURL()
    const previewBlob = dataURLtoBlob(document.getElementById('gameCanvas').toDataURL());
    formData.append('preview', new File([previewBlob], 'preview.png'));

    // Отправляем на Python-бэкенд (предположим, он запущен на localhost:5000)
    fetch('http://localhost:5000/api/publish', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || 'Опубликовано!');
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Ошибка при публикации: ' + error.message);
    });
}

function dataURLtoBlob(dataurl) {
    const arr = dataurl.split(',');
    const mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    while (n--) u8arr[n] = bstr.charCodeAt(n);
    return new Blob([u8arr], { type: mime });
}
