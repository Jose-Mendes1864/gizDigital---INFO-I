let divPerguntas = document.querySelectorAll('.perguntaContainer');

// Esconde todas, menos a primeira
for (let i = 1; i < divPerguntas.length; i++) {
    divPerguntas[i].style.display = 'none';
}

let btn_proximo = document.getElementById("btn-proximo");
let cont = 0;
if (btn_proximo) {
    
    btn_proximo.addEventListener('click', () => {
        
        let input = document.querySelector('.inputQuiz')
        
        if(input.value == '' || input.value == 'none'){
            alert('Digite um valor válido ' + input.value)

        }
        else if (cont +  1 >= divPerguntas.length) {
            let form = document.getElementById('form')
            form.submit()
         
        } else {
            cont += 1;

            

            divPerguntas[cont].style.display = 'block';
            divPerguntas[cont - 1].style.display = 'none';
        }
    });
}

