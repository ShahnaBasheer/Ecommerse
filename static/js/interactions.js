$(document).ready(function(){
    $("#clicksort").click(function(){
       $("#sortby").toggle();
    });
    
    $(".filter-checkbox").on('click', function () {
        let _filterObj = {};
        let _filterGender = $(this).data('gender');
        $(".filter-checkbox").each(function (index,ele) {
           let _filterValue = $(this).val();
           let _filterKey = $(this).data('filter');

           _filterObj[_filterKey] = Array.from(document.querySelectorAll(
              'input[data-filter='+_filterKey+']:checked'))
              .map(function(el){return el.value;});
           });
           $.ajax({
            url:'/' + _filterGender + '/' + 'categories',
            data: _filterObj,
            dataType:'json',
            success:function(response){
               $(".products").html(response.details);

            }    
         });
      });
   });
   

   



