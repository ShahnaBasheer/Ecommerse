$(document).ready(function(){
  let sizetag = $(".selected-size")
  let radio = $('input[type="radio"]')
  sizetag.click(function(){
    $(this).toggleClass('selectedsize');
    sizetag.not(this).removeClass('selectedsize');
  });

  $(".addtocart").click(function(){
    let size = $('.selectedsize').data('size');
    let gender = $('.hiddengender').data('gender');
    let pro_id = $('.hiddenid').data('pro_id');
    let seller = false;

    if(radio.length){
      seller = $('input[type="radio"]:checked').val();
    }else{
      seller = $('.seller').text();
    }

    if(sizetag.hasClass('selectedsize') && seller){   
        let product={'info':gender,'size':size,'seller':seller}
        $.ajax({
          url:'/add_to_cart/' + pro_id,
          data: product,
          dataType:'json',
          success:function(response){  
            $('.cart-qnty').text(response.cart_qnty);
          } 
        });
    }else{
        if(!sizetag.hasClass('selectedsize')){
          $('#sizealert').text("please select size to proceed");
        }
        if(!seller){
          $('#selleralert').text("please select seller to proceed");
        }         
      } 
  });
});


