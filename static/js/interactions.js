$(document).ready(function(){  
   let sortby =  $("#sortby");
   
   function modelFunction(){
      if(window.matchMedia("(max-width: 768px)").matches){   
         $(".all_filters").wrap('<div class="modal fade" id="modalFilter" tabindex="-1"'+
          'aria-labelledby="ModelLabel" aria-hidden="true">'+
          '<div class="modal-dialog modal-dialog-centered">'+
          '<div class="modal-content modalContent p-3">'+  
          '<div class="modal-body"></div></div></div></div></div>');
          $(".modalContent").prepend('<div class="modal-header" id="ModelLabel">'+
          '<h5 class="modal-title fw-bolder text-center w-100">FILTERS</h5>'+
          '<button type="button" class="btn-close" data-bs-dismiss="modal"'+
          'aria-label="Close"></button></div>')
     }
   }
   modelFunction(); 
 
   window.addEventListener("resize",function(){
      if($("#modalFilter").length == 0){
           modelFunction()
         }
      if($("#modalFilter").length){
         if(window.matchMedia("(min-width: 769px)").matches){
            $(".all_filters").unwrap()
            $("#ModelLabel").remove()
            $(".all_filters").unwrap()
            $(".all_filters").unwrap()
            $(".all_filters").unwrap()
      }}
   });
    
   $("#clicksort").click(function(){
       sortby.toggle();
   });

   $(document).mouseup(function(e){
       if(!sortby.is(e.target) && !(e.target).closest('h5') && !sortby.has(e.target).length){
         sortby.hide();
     }
   });

   $(document).on('click','.filter-radio,.filter-checkbox,#sortby input', function(){   
        let _filterObj = {};
        let check_lists = {};
        _filterObj['search'] = $('#searchvalue').val()
        _filterObj['slct_brand'] = $('#brandvalue').val()
        _filterObj['searchType'] = $('#searchtype').val()
        keyvalue();
         _filterObj['_checked'] = ($(this).is(':checked')) ? $(this).data('filter'): " ";
        delete check_lists.sort;
        delete check_lists.gender;
        function keyvalue(){
          $(".filter-radio,.filter-checkbox,#sortby input").each(function(index,ele){
            let _filterKey = $(this).data('filter');
            console.log(_filterKey)
                  
            _filterObj[_filterKey] = check_lists[_filterKey] = Array.from($("input[data-filter="+_filterKey+"]:checked")) 
                .map(function(el){return el.value;});
            });
         }

         $.ajax({
            type:'GET',
            url:'filter_data',
            data: _filterObj,
            dataType:'json',
            success:function(response){
               $(".products").html(response.details);
               $(".ruler h3 span").text('('+response.count+')');
               
               for(i in response.filter){
                  $("#"+i+"box").html(response.filter[i])
               }
      

               for(x in check_lists){
                  if(check_lists[x].length > 0){
                     for(i of check_lists[x]){
                        $("input[value='"+i+"']").attr('checked',true);   
                        $("#filter_"+x).addClass("show");
                        $("#"+x+"_heading button").addClass("acc-buttons");
                     }
                  }                  
               }
               }
         });
   });   
   $("input#brandsearch").keyup(function(){
      let inputvalue = $(this).val().toLowerCase();
      $(".brand li a").filter(function() {
         $(this).toggle($(this).text().toLowerCase().startsWith(inputvalue))
       });
   });
   $(".searchall input").keyup(function(){
      let inputvalue = $(this).val().toLowerCase();
      $(".searchmenu li a").filter(function() {
         $(this).toggle($(this).text().toLowerCase().replace('-',"").indexOf(inputvalue)>-1)
       });
   });

   $("form#login").on('submit',function(e){
      e.preventDefault(); 
      $.ajax({
         type:'POST',
         url:'accounts/login/',
         data: $(this).serialize(),
         dataType:'json',
         success:function(response){
            if(response.status == 200){
               window.location.reload()
            }
            else if(response.status == 400){
            $("#errormess").html(
               '<div class="alert alert-danger alert-dismissible p-1 fade show mb-3"><strong>'
               +response.login+'</strong><button type="button" class="btn-close p-2"'+
               'data-bs-dismiss="alert"></button></div>')
         }}
      });
   });
    /*$(".clickfilter").click(function(){
      $(".filterscontainer").toggle();
    })*/
});


  
