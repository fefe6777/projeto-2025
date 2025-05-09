const usuario = JSON.parse(localStorage.getItem('usuario'));

console.log(usuario);

document.getElementById('nome').innerHTML = "Olá, " + usuario.nome;
document.getElementById('foto').innerHTML = `<img src="../IMGS/${usuario.foto1}" alt="Usuário" class="user-photo"></img>`


// Iniciar a câmera ao carregar a página
window.addEventListener('load', () => {
  const video = document.getElementById('video');

  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      video.srcObject = stream;
      video.play();
    })
    .catch(err => {
      console.error("Erro ao acessar a câmera:", err);
      document.getElementById('status').textContent = "Erro ao acessar a câmera.";
    });
});



function tirarFoto() {
  const video = document.getElementById('video');
  const canvas = document.getElementById('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  const imagemBase64 = canvas.toDataURL('image/jpeg');

  document.getElementById('status').textContent = "Verificando reconhecimento facial...";

  navigator.geolocation.getCurrentPosition(pos => {
    const latitude = pos.coords.latitude;
    const longitude = pos.coords.longitude;

    const geolocation = "[" + latitude + "," + latitude + "]";

    const id_funcionario = usuario.id;

    fetch("http://localhost:5000/reconhecer_face", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id_funcionario: id_funcionario,
        imagem: imagemBase64
      })
    })
    .then(res => res.json())
    .then(reconhecimento => {
      if (reconhecimento.reconhecido) {
        document.getElementById('status').textContent = "Reconhecimento facial bem-sucedido. Registrando ponto...";

        fetch("http://localhost:5000/registros_ponto", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            id_funcionario: id_funcionario,
            latitude: latitude,
            geolocalizacao: geolocation
          })
        })
        .then(res => res.json())
        .then(data => {
          if (data.mensagem && data.mensagem.includes("sucesso")) {
            document.getElementById('status').textContent = "Ponto registrado com sucesso!";
            document.getElementById('relatorioConteudo').innerHTML = "<p>Marcado às " + new Date().toLocaleTimeString() + "</p>";
          } else {
            document.getElementById('status').textContent = "Erro ao registrar ponto.";
          }
        });
      } else {
        document.getElementById('status').textContent = "Reconhecimento facial falhou.";
      }
    })
    .catch(err => {
      document.getElementById('status').textContent = "Erro no reconhecimento: " + err.message;
    });

  }, erro => {
    document.getElementById('status').textContent = "Erro ao obter localização.";
  });
}
