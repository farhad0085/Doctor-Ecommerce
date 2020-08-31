function initAdminPanel(){
	// Panel Sidebar button click
	$(".panel-side-bar-btn").click(function(){
        $(".panel-side-bar-btn").each(function(ind,obj){
            $(obj).css("background-color","#100b1f")  
        })
        $(this).css("background-color","#244bc9")

        if($(this).attr("id")=="add-product-btn"){ // Add product main area setup
			$("#add-product-main-area").show()
			$("#add-specialist-main-area").hide()
			addProductPanelSetup() // product panel setup
        }
        else if($(this).attr("id")=="add-specialist-btn"){ // Add product main area setup
			$("#add-product-main-area").hide()
			$("#add-specialist-main-area").show()
            addSpecialistPanelSetup() // specialist panel setup
        }
    })

    function addProductPanelSetup(){
    	$("#add-product-upload").click(function(){
	        var pics = []
	        var max_pics = 3
	        var pic_ind = 0
	        var name = $("#add-product-main-area").find("#product-name").val()
	        var des = $("#add-product-main-area").find("#description-textarea").val()
	        var price = $("#add-product-main-area").find("#price").val()
	        var quantity = $("#add-product-main-area").find("#quantity").val()
	        var pic1 = $("#add-product-main-area").find("#pic-1").get()[0]
	        var pic2 = $("#add-product-main-area").find("#pic-2").get()[0]
	        var pic3 = $("#add-product-main-area").find("#pic-3").get()[0]
	        
	        readFileAsDataURL(pic1.files[0])
	        readFileAsDataURL(pic2.files[0])
	        readFileAsDataURL(pic3.files[0])
	                        
	        function readFileAsDataURL(file){
	            var fileReader = new FileReader();
	            if (fileReader) {
	                try{
	                    fileReader.readAsDataURL(file);
	                    fileReader.onload = function () {
		                     var imageData = fileReader.result;
		                     pics.push(imageData)
		                     pic_ind++
	                    }.bind(this)
	                }catch(e){
	                    tag("error","couldn't read file as readAsDataURL")
	                    pic_ind++
	                }
	                if(pic_ind==max_pics){
	                    sendJSON()
	                }
	            }
	        }
	        function sendJSON(){
	            var str = JSON.stringify({
	                "name": name,
	                "description": des,
	                "price": price,
	                "quantity": quantity,
	                "pictures": pics
	            })
	            // tag(str)

	            var xhr = new XMLHttpRequest();
	            xhr.open("POST", api_host+'/api/add/product', true);
	            xhr.setRequestHeader('Content-Type', 'application/json');
	            xhr.onreadystatechange = function() {
	                if (xhr.readyState == XMLHttpRequest.DONE) {
	                    print(xhr.responseText);
	                    // $("#dummy").html(xhr.responseText)
	                }
	            }
	            xhr.send(str);
	        }               
	        
	    })
    }

    function addSpecialistPanelSetup(){
    	$("#add-specialist-upload").click(function(){
	        var pics = []

	        var full_name = $("#add-specialist-main-area").find("#name").val()
	        var email = $("#add-specialist-main-area").find("#email").val()
	        var date_of_birth = $("#add-specialist-main-area").find("#date_of_birth").val()
	        var password = $("#add-specialist-main-area").find("#password").val()
	        var address = $("#add-specialist-main-area").find("#address").val()
			var contact_no = $("#add-specialist-main-area").find("#contact_no").val()
			var age = $("#add-specialist-main-area").find("#age").val()

	        var pic1 = $("#add-specialist-main-area").find("#pic-1").get()[0]
	        
	        readFileAsDataURL(pic1.files[0])
	                        
	        function readFileAsDataURL(file){
	            var fileReader = new FileReader();
	            if (fileReader) {
	                try{
	                    fileReader.readAsDataURL(file);
	                    fileReader.onload = function () {
	                      var imageData = fileReader.result;
	                      pics.push(imageData)
	                      sendJSON()
	                      // tag('result',pics[0])
	                    }.bind(this)
	                }catch(e){
	                    tag("error","couldn't read file as readAsDataURL")
	                }	                
	            }
	        }
	        function sendJSON(){
	        	if(pics.length>0){
		        	var str = JSON.stringify({
	                        "email": email,
	                        "date_of_birth": date_of_birth,
	                        "password": password,
	                        "full_name": full_name,
	                        "address" : address,
	                        "contact_no" : contact_no,
	                        "age" : age,
	                        "role" : "doctor",
	                        "profile_pic":pics[0]
	                });
		        } else {
		        	var str = JSON.stringify({ // Without profile pic
	                        "email": email,
	                        "date_of_birth": date_of_birth,
	                        "password": password,
	                        "full_name": full_name,
	                        "address" : address,
	                        "contact_no" : contact_no,
	                        "age" : age,
	                        "role" : "doctor",
	                });
		        }
	            tag(str)

	            var xhr = new XMLHttpRequest();
	            xhr.open("POST", api_host+'/api/add/user', true);
	            xhr.setRequestHeader('Content-Type', 'application/json');
	            xhr.onreadystatechange = function() {
	                if (xhr.readyState == XMLHttpRequest.DONE) {
	                    print(xhr.responseText);
	                    // $("#dummy").html(xhr.responseText)
	                }
	            }
	            xhr.send(str);
	        }               
	        
	    })
    }
}

