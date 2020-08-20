var api_host = "http://127.0.0.1:5000"
var web_host = "http://localhost/GDApp/frontend"
var STORAGE_LANG = "gd_language"


function init(container_id,footer_container_id,floating_view_id){
	// Loading Footer
	$("#"+footer_container_id).load("templates/footer_main.html #footer-container")
	// setting up container
    try{
        $("#"+container_id).css("top",document.getElementById(floating_view_id).getBoundingClientRect().bottom+"px");
    }
	catch{
        $("#"+container_id).css("top",0+"px");
    }
	//Logo gradient pos
	$("#logo-grad").css("right","0"+"px")
}

function main_loop(){
    // topNotificationHandler("top_notification")
}


var isNotificationRunning = true
function setupNotification(top_notification){
    $("#top-notification-close").click(function(){
        isNotificationRunning = false
        $("#"+top_notification).css("display","none")
    })
}

var notificationIndex = 0;
function topNotificationHandler(top_notification){
    
    if(isNotificationRunning){
        var width = document.getElementById(top_notification).getBoundingClientRect().width
        $("#"+top_notification).css("left",($(window).width()-width/4)+"px")
        gsap.to("#"+top_notification, {duration: 0.5, left: $(window).width()-width })
        var notification_data = ["পণ্য 5% কম দাম","আমাদের বিশেষজ্ঞদের সাথে দেখা করুন","পণ্য পেজ দেখুন"]
    // var r=Math.random()
    // if(r<0.1){
        if(notificationIndex>=notification_data.length){
            notificationIndex = 0
        }
        $("#top-notification-data").html(notification_data[notificationIndex++])
    // }
        setTimeout(function(){
            topNotificationHandler("top-notification")
            },1*3000)
    }
}


function startFloatingOffer(floating_view_id, following_container_id){
	var floatOfferAnim = true;

	$("#top-floating-close").css("top",document.getElementById(floating_view_id).getBoundingClientRect().top+"px")

	// Floting Offer
	$("#top-floating-close").hover(function(){
		$(this).css("transform","scale("+1.2+")")
	},function(){
		$(this).css("transform","scale("+1+")")
	})
	$("#top-floating-close").click(function(){
		$(this).css("display","none")
		$("#"+floating_view_id).css("display","none")
		$("#"+following_container_id).css("top",0+"px");
		floatOfferAnim = false
	})


	var top_view_colors = [[255, 70, 33],[128, 44, 245],[255, 28, 126]]
	cIndex=-1;
	function floatGsap(){
		cIndex = cIndex+1;
		if(cIndex%3==0){
			cIndex=0;
		}
		if(floatOfferAnim){
			var t1 = gsap.to("#"+floating_view_id,{
				duration: 3,
				backgroundColor: "rgb("+top_view_colors[cIndex][0]+","+top_view_colors[cIndex][1]+","+top_view_colors[cIndex][2]+")",
				onComplete: floatGsap
			})
		}
	}
	floatGsap()
}

function startHeaderAndCanvasBasic(header_canvas_container_id,logo_id,header_canvas_id,header_bar_id){
	//setting up logo
	$("#"+logo_id).css("top",0+"px")
    $("#"+logo_id).css("min-height",$("#"+header_canvas_id).css("height"))
    $("#"+header_bar_id).load("templates/parts.html #nav-bar-items-a-href-links",function(){
        $("#"+header_bar_id).html($("#nav-bar-items-a-href-links").html())
    })
    
    $("#"+header_canvas_container_id).css("height",$("#"+header_canvas_id).css("height"))
    // console.log($("#"+header_canvas_id).css("height"))
    //setting up canvas
	var c = document.getElementById(header_canvas_id);
    c.width = 1000;
    c.height = $("#"+header_canvas_id).height()/$("#"+header_canvas_id).width()*c.width;

    window.addEventListener("resize",function(){
    	c.height = $("#"+header_canvas_id).height()/$("#"+header_canvas_id).width()*c.width;
    })
    var ctx = c.getContext("2d");



    var particles=[]
    var timestamp=50
    var particle_speed = 1;
    c.addEventListener("mousemove",function(e){
        var x_c = c.width/c.getBoundingClientRect().width*(e.pageX-c.getBoundingClientRect().left)
        var y_c = c.height/c.getBoundingClientRect().height*(e.pageY-c.getBoundingClientRect().top)
        var dir_angle = Math.random()*2*Math.PI
        particles.push([x_c,y_c,timestamp,dir_angle])  
    },false)
    

    var particle_colors = [[255, 70, 33],[128, 44, 245],[255, 28, 126],[67, 235, 52]]
    var color_index = 0;
    var color_index2 = 0;
    
    function updateCanvas(){
        ctx.clearRect(0, 0, c.width, c.height);

        for (var i = 0; i <particles.length; i++) {
            ctx.beginPath();
            ctx.arc(particles[i][0], particles[i][1], 10, 0, 2 * Math.PI);
            
            particles[i][0] = particles[i][0] + particle_speed*Math.cos(particles[i][3])
            particles[i][1] = particles[i][1] + particle_speed*Math.sin(particles[i][3])
            
            particles[i][2] = particles[i][2] - 1

            if(Math.random()<0.1){
                    color_index = Math.floor(Math.random() * Math.floor(particle_colors.length))
            }

            ctx.fillStyle = "rgba(+"+particle_colors[color_index][0]+","+particle_colors[color_index][1]+","+particle_colors[color_index][2]+","+particles[i][2]/timestamp+")";

            ctx.fill();
            // ctx.stroke();

            if(particles[i][2]<=0){
                particles.splice(i,1)
            }
        }

        window.requestAnimationFrame(updateCanvas)
    }
    window.requestAnimationFrame(updateCanvas)
}

function tag(...args){
    var st=args[0]+"---: "
    for(var i=1;i<args.length;i++){
        st = st + args[i] + " "
    }
    console.log(st)
}

function lang_handle(){
    var lang = localStorage.getItem(STORAGE_LANG)
    if(lang=="english"){
        $(".english-static").css("display","inline-block")
        $(".bangla-static").css("display","none")
    }
    else if(lang == "bangla" || lang == null){
        $(".bangla-static").css("display","inline-block")
        $(".english-static").css("display","none")
    }
}

function navbar_login_processes_lt(jData,current_page){
                
    tag("jData",jData[1]["message"])
    if($("#login-btn").get()[0]){ //loop until log-in button is ready through jquery.load()
        
        if(jData[1]["message"]=="success"){
            $("#login-btn").find("#login-text").css("display","none")
            $("#login-btn").find("#logout-text").css("display","block")
            $("#login-btn").attr("href","#")
            $("#login-btn").click(function(){
                localStorage.removeItem(STORAGE_TOKEN)
                localStorage.removeItem(STORAGE_USER_ID)
                window.open(web_host+"/"+current_page+".html","_self")
                return false
            })
        }
    }
    else{
        tag("looping...")
        setTimeout(function(){
            navbar_login_processes_lt(jData,current_page)}
            ,50)
    }
}

function navbar_lang_processes_lt(current_page){
                
    if($("#login-btn").get()[0]){ //loop until log-in button is ready through jquery.load()
        lang_handle()
        // Language Selection Section

        $(".lang-dropdown-item").click(function(){

            $("#lang-dropdownMenuButton").html($(this).html())
            if($(this).html()=="English"){
                localStorage.setItem(STORAGE_LANG,"english")
                window.open(web_host+"/"+current_page+".html","_self")
            }
            else{
                localStorage.setItem(STORAGE_LANG,"bangla")
                window.open(web_host+"/"+current_page+".html","_self")
            }
            return false
        })
        
    }
    else{
        tag("looping...")
        setTimeout(function(){
            navbar_lang_processes_lt(current_page)}
            ,50)
    }
}