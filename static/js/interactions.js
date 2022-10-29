
$(document).ready(function(){
    $("#clicksort").click(function(){
       $("#sortby").toggle();
    });
    $(".filter-radio,.filter-checkbox").on('click', function () {   
        let _filterObj = {};
        let _filterGender = $(this).data('gender');
        function keyvalue(){
          $(".filter-radio,.filter-checkbox").each(function (index,ele) {
             let _filterValue = $(this).val();
             let _filterKey = $(this).data('filter');
             _filterObj[_filterKey] = Array.from(document.querySelectorAll(
                'input[data-filter='+_filterKey+']:checked'))
                .map(function(el){return el.value;});
             });
         }
        keyvalue();
        
        $.ajax({
            url:'/' + _filterGender + '/' + 'filter_data',
            data: _filterObj,
            dataType:'json',
            success:function(response){
               $(".products").html(response.details);
               $("#catbox").html(response.allcategory);
               $("#agebox").html(response.allages);
               $("#sizebox").html(response.allsizes);
               $("#offerbox").html(response.alloffers);
               
               if(_filterGender=='girls'|| _filterGender=='boys'){
                  $(".filter-checkbox").click(function(){ 
                    keyvalue();
                    $.ajax({
                      url:'/' + _filterGender + '/' + 'filter_data',                     
                      data: _filterObj,
                      dataType:'json',
                      success:function(response){
                       $(".products").html(response.details);
                      }
                    });  
                    
                  });  
               }
            }    
         });  
        });
      });
   
   
