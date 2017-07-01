$(function() {
	

	
		if ($("#cargoType").val() == "TiresWheels"){
		tiresWheels();
		}
		if ($("#cargoType").val() == "Pallet"){
		$("#tyres").empty();
			pallet();}
		if ($("#cargoType").val() == "Cargo"){
		$("#tyres").empty();
			cargo();}				
		if ($("#cargoType").val() == "Documents"){
		$("#tyres").empty();
			documents();}	
	
	$("#cargoType").change(function(){
		if ($(this).val() == "TiresWheels"){
		tiresWheels();
		}
		if ($(this).val() == "Pallet"){
		$("#tyres").empty();
			pallet();}
		if ($(this).val() == "Cargo"){
		$("#tyres").empty();
			cargo();}				
		if ($(this).val() == "Documents"){
		$("#tyres").empty();
			documents();}				
		
	});
	$("#plus").click(function(){
	if ($("#cargoType").val() == "Pallet"){
		pallet();	}
	/*if ($("#cargoType").val() == "Cargo"){
			cargo();}
	if ($("#cargoType").val() == "Documents"){
			documents();}	*/	
	});
	
	
	$("form").submit(function(e){
		e.preventDefault();
		if ($("#ajax_form").valid()){
			$("#loading").addClass("loading");
			$.ajax({
				type: "POST",
				
				url: Flask.url_for("show_entries"),
				Type : "json",
				data :$(this).serializeArray(),
				success : function(result){
				$("#loading").removeClass("loading");	
				$("#result").html(result);
				$('html, body').animate({ scrollTop: $("#result").offset().top }, 500);
				},
				error : function(result){
					$("#loading").removeClass("loading");
					$(".container").load(Flask.url_for("error"));
					console.log(result);
					}
				});
			
	      	}
		else {
			return false;
		}
		});	
});	



function tiresWheels(){
		$("#plus").hide();
		var parameters =         
			{
			"modelName": "Common",
			"calledMethod": "getTiresWheelsList",
			"apiKey": "8c4d695c530e963968190af84ded7bc8"
			};
			
		$.ajax({
			type: 'POST',
			contentType: 'application/json',
			url: "https://api.novaposhta.ua/v2.0/json/",
			dataType : 'json',
			data : JSON.stringify(parameters),
			success : function(result) {
			content='';
			for(var i=0;i<result.data.length;i++){
			
			content+="<li class=\"form-inline\"><label for="+result.data[i].Ref+">"+result.data[i].Description+"</label><input class=\"form-control input-sm\" type=\"text\" name=\""+result.data[i].Ref+"\"/><small>ед.</small></li>";
			}
			content="<ul>"+content+"</ul>";
			$("#tyres").html(content);
			
				},error : function(result){
					
				console.log(result);
				}
			});	
};

function pallet(){
			$("#plus").show();
			$("#tyres").append("<div>");
			$("#tyres > div").addClass("form-inline");
			var s = $( "#tyres > div" ).length;
			if (s <=4){
			var arr = {"weight":"Вага палети, кг",
			"volumetricLength":"Довжина палети, см",
			"volumetricWidth":"Ширина палети, см",
			"volumetricHeight":"Висота палети, см",
			"seats_amount":"Кількість, шт"}
			
			var i = 0;
			
			for(code in arr){
			$("#tyres > div:last").append("<input>");
			$("#tyres > div:last > input:eq({i})".replace("{i}", i)).addClass("form-control").attr({"type":"text", "size":30, "name":code,"placeholder":arr[code]});
			$("#tyres > div:last").append("<span>");
			$("#tyres > div:last > span:eq({i})".replace("{i}", i)).addClass("help-block").attr({"id":"helpBlock"}).html(arr[code]);
			i++;
			}
			$("#tyres > div > input").wrap("<dt>");
			$("#tyres > div > dt").addClass("form-group  myform");
			}
};

function cargo(){
			$("#plus").hide();
			var arr = {"weight":"Загальна вага, кг","volumetricLength":"Загальна довжина, см","volumetricWidth":"Загальна ширина, см","volumetricHeight":"Загальна висота, см","seats_amount":"Кількість місць, шт"}
			var i = 0;
			
			$("#tyres").append("<div>");
			$("#tyres > div").addClass("form-inline");
			
			for(code in arr){
				
			$("#tyres > div:last").append("<input>");
			$("#tyres > div:last > input:eq({i})".replace("{i}", i)).addClass("form-control").attr({"type":"text", "size":30, "name":code,"placeholder":arr[code]});
			$("#tyres > div:last").append("<span>");
			$("#tyres > div:last > span:eq({i})".replace("{i}", i)).addClass("help-block").attr({"id":"helpBlock"}).html(arr[code]);
			i++;
			}
			$("#tyres > div > input").wrap("<dt>");
			$("#tyres > div > dt").addClass("form-group  myform");

};
function documents(){
			$("#plus").hide();
			var arr = {"Вага від 0,5 до 1 кг":1, "Вага від 0,1 до 0,5 кг":0.5, "Вага до 0,1 кг":0.1};
			var i = 0;
			
			$("#tyres").append("<div>");
			$("#tyres > div").addClass("form-group").attr({"id":"docblock"});
			
			
			
			$("#tyres > div:last").append("<input>");
			$("#tyres > div:last > input").addClass("form-control").attr({"type":"text", "size":30, "name":"seats_amount","placeholder":"Кількість, шт"});
			$("#tyres > div:last").append("<span>");
			$("#tyres > div:last > span").addClass("help-block").attr({"id":"helpBlock"}).html("Кількість, шт");
			
			$("#tyres > div > inputб #tyres > div:last > span").wrapAll("<dt>");
			$("#tyres > div > dt").addClass("form-group   myform");
			$("#tyres > div:last").append("<select>");
			$("#tyres > div:last > select").addClass("form-control").attr({"name":"weight","id":"docweight"});
			for (value in arr){
				$("#tyres > div:last > select").append("<option>");
				$("#tyres > div:last > select > option:eq({i})".replace("{i}", i)).attr({"value":arr[value]}).html(value);
				i++;
			}
};
