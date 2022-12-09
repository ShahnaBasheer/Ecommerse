$(document).ready(function(){  
    
   $("#clicksort").click(function(){
       $("#sortby").toggle();
   });

   $(document).on('click','.filter-radio,.filter-checkbox,#sortby input', function(){   
        let _filterObj = {};
        let _filterGender = $(this).data('gender');
          _filterObj['search'] = $('#searchvalue').val()
        console.log(_filterObj)
        function keyvalue(){
          $(".filter-radio,.filter-checkbox,#sortby input").each(function(index,ele){
             let _filterKey = $(this).data('filter');
             _filterObj[_filterKey] = Array.from($("input[data-filter="+_filterKey+"]:checked")) 
                .map(function(el){return el.value;});
             });
         }
         keyvalue();
         $.ajax({
            type:'GET',
            url:'filter_data',
            data: _filterObj,
            dataType:'json',
            success:function(response){
               $(".products").html(response.details);
               $("#categorybox").html(response.filter.category);
               $("#agebox").html(response.filter.age);
               $("#brandbox").html(response.filter.brand);
               $("#discountbox").html(response.filter.discount);
               $("#sizebox").html(response.filter.size);
               $("#colorbox").html(response.filter.color);
               $("#materialbox").html(response.filter.material);
               $("#patternbox").html(response.filter.pattern);
               $("#occasionbox").html(response.filter.occasion);
               $("#neckbox").html(response.filter.neck);
               $("#pocketbox").html(response.filter.pocket);
               $("#sleevebox").html(response.filter.sleeve);  
               $("#risebox").html(response.filter.rise);
               $("#stretchablebox").html(response.filter.stretchable);
               $(".all_filters input").attr("data-gender",response.gender);                          
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

});
     
  
