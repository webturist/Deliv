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
	$.ajax({
			type: "POST",
			
			url: Flask.url_for("show_entries"),
			Type : "json",
			data :$(this).serializeArray(),
			success : function(result){
			console.log("OK");
			},
			error : function(result){
				console.log(result);
				}
			});	
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
			var arr = {"weight":"Вага палети",
			"volumetricLength":"Довжина палети",
			"volumetricWidth":"Ширина палети",
			"volumetricHeight":"Висота палети",
			"seats_amount":"Кількість"}
			
			var i = 0;
			
			for(code in arr){
			$("#tyres > div:last").append("<input>");
			$("#tyres > div:last > input:eq({i})".replace("{i}", i)).addClass("form-control").attr({"type":"text", "size":30, "name":code,"placeholder":arr[code]});
			i++;
			}
			$("#tyres > div > input").wrap("<dt>");
			$("#tyres > div > dt").addClass("form-group  myform");
			}
};

function cargo(){
			$("#plus").hide();
			var arr = {"weight":"Загальна вага","volumetricLength":"Загальна довжина, см","volumetricWidth":"Загальна ширина, см","volumetricHeight":"Загальна висота, см","seats_amount":"Кількість місць"}
			var i = 0;
			
			$("#tyres").append("<div>");
			$("#tyres > div").addClass("form-inline");
			
			for(code in arr){
			$("#tyres > div:last").append("<input>");
			$("#tyres > div:last > input:eq({i})".replace("{i}", i)).addClass("form-control").attr({"type":"text", "size":30, "name":code,"placeholder":arr[code]});
			i++;
			}
			$("#tyres > div > input").wrap("<dt>");
			$("#tyres > div > dt").addClass("form-group  myform");

};
function documents(){
			$("#plus").hide();
			var arr = {"weight":"Загальна вага","seats_amount":"Кількість"}
			var i = 0;
			
			$("#tyres").append("<div>");
			$("#tyres > div").addClass("form-inline");
			
			for(code in arr){
			$("#tyres > div:last").append("<input>");
			$("#tyres > div:last > input:eq({i})".replace("{i}", i)).addClass("form-control").attr({"type":"text", "size":30, "name":code,"placeholder":arr[code]});
			i++;
			}
			$("#tyres > div > input").wrap("<dt>");
			$("#tyres > div > dt").addClass("form-group   myform");

};
