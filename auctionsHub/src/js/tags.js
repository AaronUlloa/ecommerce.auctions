(function (){
  const tagsInput = document.querySelector('#tags_input');

  if (tagsInput){
    const tagsDiv = document.querySelector('#tags');
    const tagsInputHidden = document.querySelector('[name="tagsName"]');

    //Creamos un arreglo de tags
    let tags = [];
    // Escuchar los cambios en el input
    tagsInput.addEventListener('keypress', guardarTags)

    function guardarTags(e){
      if (e.keyCode == 44){
        // Validamos espacios en blanco
        if (e.target.value.trim() === '' || e.target.value < 1){
          return;
        }
        e.preventDefault();
        tags = [...tags, e.target.value.trim()];
        tagsInput.value = '';

        listarTags();
      }
    }
    function listarTags(){
      tagsDiv.textContent = '';
      tags.forEach(tag =>{
        const etiqueta = document.createElement('LI');
        etiqueta.classList.add('forms');
        etiqueta.textContent = tag;
        etiqueta.ondblclick = eliminarTag
        tagsDiv.appendChild(etiqueta);
      })
      actualizarInputHidden();
    }
    function eliminarTag(e){
      e.target.remove();
      tags = tags.filter(tag => tag !== e.target.textContent);
      actualizarInputHidden();
    }
    function actualizarInputHidden(){
      tagsInputHidden.value = tags.toString();
    }
  }
})()
