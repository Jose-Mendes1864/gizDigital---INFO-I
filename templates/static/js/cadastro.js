
const form = document.getElementById('form');

form.addEventListener('submit', validaLogin);
function validaLogin(event){
    

    let senha = document.querySelector('.senha').value.trim();
    let confSenha = document.querySelector('.senhaAgain').value.trim();
 
    if (senha != confSenha){
        event.preventDefault()
        let message = document.querySelector('.message')
        message.innerHTML = 'As senhas não conincidem';
    }
    else{
        alert('iu')
    }

   
}

document.querySelector(".imagem").addEventListener("change", function (event) {
    const file = event.target.files[0]; // pega o arquivo selecionado
    if (file) {
      const reader = new FileReader();

      reader.onload = function (e) {
        // cria a tag <img> e coloca na div
        document.getElementById("circulo-foto").innerHTML = 
          `<img src="${e.target.result}" alt="Pré-visualização">`;
      };

      reader.readAsDataURL(file); // lê o arquivo como URL base64
    }
  });
