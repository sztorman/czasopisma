jQuery(document).ready(function($) {
    
    var data = false
    
    $('#exPage').click(function() {
        data = !data;
    });
    
    $("#downloadButton").click(function(){        
        if ($('[value=page]').attr("checked") == "checked") {
	        $('input[name=file]').each(function(event) {
	            if (data)
	                window.open('/stWeb/download/?obId='+$('[name=obId]').val()+'&exportType=page&file='+$(this).val());
	        });
	        return false;
        }
    });
});