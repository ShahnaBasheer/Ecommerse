
function sortclick(){
  let x = document.getElementById("sortby");
  if (x.style.display === 'block'){
    x.style.display = 'none';
  } else {
    x.style.display = 'block';
  }
}

function formsubmit(clickid){
  let form = document.getElementById("formsubmit");
  let y = document.getElementById(clickid);
  if(y.checked == true){
    form.submit();
  }
}