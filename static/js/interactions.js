$(document).ready(function(){  
    
   $("#clicksort").click(function(){
       $("#sortby").toggle();
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
            _filterObj[_filterKey] = check_lists[_filterKey] = Array.from($("input[data-filter="+_filterKey+"]:checked")) 
                .map(function(el){return el.value;});
            });
         }
         
         console.log(_filterObj);
         console.log(_filterObj._checked)
         
         $.ajax({
            type:'GET',
            url:'filter_data',
            data: _filterObj,
            dataType:'json',
            success:function(response){
               $(".products").html(response.details);
               $(".ruler h3 span").text('('+response.count+')');
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
               

               for(x in check_lists){
                  if(check_lists[x].length > 0){
                     for(i of check_lists[x]){
                        $("input[value='"+i+"']").attr('checked',true);
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

});
     
  
