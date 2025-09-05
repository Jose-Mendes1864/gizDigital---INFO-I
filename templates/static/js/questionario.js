let divPerguntas = document.querySelectorAll('.perguntaContainer');

// Esconde todas, menos a primeira
for (let i = 1; i < divPerguntas.length; i++) {
    divPerguntas[i].style.display = 'none';
}

let btn_proximo = document.getElementById("btn-proximo");
let cont = 0;

if (btn_proximo) {
    btn_proximo.addEventListener('click', () => {
        cont += 1;

        if (cont >= divPerguntas.length) {
            let form = document.getElementById('form')
            form.submit()
         
        } else {
            divPerguntas[cont].style.display = 'block';
            divPerguntas[cont - 1].style.display = 'none';
        }
    });
}

