// Firebase SDK
const firebaseConfig = {
    apiKey: "AIzaSyB-v8HrhdF50mO1l2PV6FskAB1qVfLXEEY",
    authDomain: "eventos-en-hoteles-aspl.firebaseapp.com",
    projectId: "eventos-en-hoteles-aspl",
    storageBucket: "eventos-en-hoteles-aspl.firebasestorage.app",
    messagingSenderId: "629559071896",
    appId: "1:629559071896:web:973e545113eba9fa9baced",
    measurementId: "G-4P81G4GYEV"
};

firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const btnSubmit = document.getElementById('btnSubmit');
    
    btnSubmit.disabled = true;
    btnSubmit.textContent = 'Cargando...';

    try {
        const userCredential = await auth.signInWithEmailAndPassword(email, password);
        const idToken = await userCredential.user.getIdToken();

        const response = await fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({ token: idToken })
        });

        if (response.ok) {
            window.location.href = '/home/';
        } else {
            const data = await response.json();
            mostrarToastExito(data.error || 'Error al iniciar sesión', 'error');
        }
    } catch (error) {
        let mensaje = 'Error al iniciar sesión';
        if (error.code === 'auth/user-not-found') {
            mensaje = 'Usuario no encontrado';
        } else if (error.code === 'auth/wrong-password') {
            mensaje = 'Contraseña incorrecta';
        } else if (error.code === 'auth/invalid-email') {
            mensaje = 'Email inválido';
        }
        mostrarToastExito(mensaje, 'error');
    } finally {
        btnSubmit.disabled = false;
        btnSubmit.textContent = 'Ingresar';
    }
});
