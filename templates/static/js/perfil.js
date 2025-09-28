 

const inputFoto = document.getElementById('fotoDePerfil');
const preview = document.getElementById('previewFoto');

inputFoto.addEventListener('change', function() {
    if (inputFoto.files && inputFoto.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result; // atualiza a imagem no frontend
        }
        reader.readAsDataURL(inputFoto.files[0]);
    }
});
let inputsForms = Array.from(document.querySelectorAll('input'));
let textAreas = Array.from(document.querySelectorAll('textarea'));
let select = Array.from(document.querySelectorAll('select'))
// Juntar os arrays
inputsForms = inputsForms.concat(textAreas);
inputsForms = inputsForms.concat(select);

  for(let i = 0; i < inputsForms.length; i++){
    inputsForms[i].classList.add('sem_modificacao')
     inputsForms[i].addEventListener('change', (event)=> 
      {
        let alvo = event.target;
        alvo.classList.remove('sem_modificacao');
          
        let parent = alvo.parentElement;
        const siblings = Array.from(parent.children).filter(el => el !== alvo);

        siblings.forEach(sibling => {
            sibling.classList.remove('sem_modificacao');
});

      })
}
function validaCheckBox(checkbox){
 

    let inputs = Array.from(checkbox.children).filter(el => el.tagName === "INPUT");
    
    for(let i =0; i < inputs.length;i++){
       if(inputs[i].checked){
       
         return true
       }

    }
    return false
  }

  function ValidaForm(event){
   let checkbox = document.querySelectorAll('.checkbox')
   for(let i = 0; i < checkbox.length;i++){

      if(validaCheckBox(checkbox[i]) == false){
        alert(`Selecione algum campo do tópico ${checkbox[i].id}`)
        event.preventDefault()
      }
   }
   for(let i = 1; i < inputsForms.length; i++){ // começa em um por causa de eliminar o csrf
   

    if(inputsForms[i].classList.contains('sem_modificacao')) {
        inputsForms[i].name  = ''

    }
     }
   
  }


let form = document.querySelector('.form-section')

form.addEventListener('submit',ValidaForm)
