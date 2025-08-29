
function validaLogin(event){
   

    let senha = document.querySelector('.senha').value.trim();
    let confSenha = document.querySelector('.senhaAgain').value.trim();
 
    if (senha != confSenha){
        event.preventDefault()
        let message = document.getElementById('message')
        message.innerHTML = 'As senhas não conincidem';
        document.getElementById('form-senha-nova').reset()
        senha.focus()
    }
  
}

function uneElemento() {
      let inputs = document.getElementsByClassName('inputCodigo')
      let codigo = ''
      for (let i = 0; i < inputs.length; i++) {
        codigo += inputs[i].value

      }
      document.getElementById('codigo').value = codigo
}