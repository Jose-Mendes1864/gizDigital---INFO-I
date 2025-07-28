
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