
document.addEventListener("DOMContentLoaded", function () {
  const loginForm = document.getElementById("loginForm");
  const emailInput = document.getElementById("email");
  const senhaInput = document.getElementById("senha");

  loginForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const email = emailInput.value;
    const senha = senhaInput.value;

    fetch("http://localhost:5000/funcionarios/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, senha })
    })
      .then(res => res.json())
      .then(data => {
        console.log(data);
        if (data.mensagem && data.mensagem.includes("Login bem-sucedido")) {
          // Redireciona para a home.html
          localStorage.setItem('usuario', JSON.stringify(data));
          window.location.href = "home.html";
        } else {
          alert("Usuário ou senha inválidos.");
        }
      })
      .catch(err => {
        alert("Erro ao conectar com o servidor: " + err.message);
      });
  });
});
