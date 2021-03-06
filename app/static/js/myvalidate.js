$(function() {
	$.validator.addMethod( "lettersonly", function( value, element ) {
		return this.optional( element ) || /^[А-Яа-яёЁЇїІіЄєҐґ', .-\s]+$/i.test( value );
	}, "Лише українські літери" );
	$.validator.addMethod( "serchon", function( value, element ) {
		return this.optional( element ) || /^[А-Яа-яёЁЇїІіЄєҐґ'-\s]{1,},\s[А-Яа-яёЁЇїІіЄєҐґ'-\s]{1,},\s[А-Яа-яёЁЇїІіЄєҐґ'-\s]{1,}$/i.test( value );
	}, "Виберіть назву міста з випадаючого списку" );
	
	var global = {
		
		rules: {
        	city_out: {
                required: true,
                lettersonly:true,
                serchon:true
            },
            city_in: {
                required: true,
                lettersonly:true,
                serchon:true
            },
            seats_amount: {
                required: true,
                digits: true,
                minlength: 1,
                min: 1
            },
            cost:{
                required: true,
                digits: true,
                minlength: 1,
                min: 1
            }
		},
		messages: {
        	city_out: {
                required: "Введіть назву міста"
            },
            city_in: {
                required: "Введіть назву міста"
            },
			seats_amount: {
            	required: "Не менше 1 шт."
            },
            cost:{
            	required: "Не менше 1 грн."
            }
		},
		errorClass: "form-input_error",
        validClass: "form-input_success"
		
		};
	var cargo = {
	    	
	    	
	        rules: {
	        	
	            weight: {
	                required: true,
	                digits: true,
	                minlength: 1,
	                min: 1,
	                max: 9999
	                
	            },
	            volumetricLength: {
	                required: true,
	                digits: true,
	                minlength: 1,
	                min: 1,
	                max: 5000
	            },
	            volumetricWidth: {
	                required: true,
	                digits: true,
	                minlength: 1,
	                min: 1,
	                max: 2000
	            },
	            volumetricHeight: {
	                required: true,
	                digits: true,
	                minlength: 1,
	                min: 1,
	                max: 2000
	            }
	        },
	        messages: {
	        	weight: {
		         	required: "Вага не менше 1 кг"
			 	},           
	           
	            volumetricLength: {
	            	required: "Не менше 1 см",
	            		max:"Не більше 9000 см"
	            },
	            volumetricWidth: {
	            	required: "Не менше 1 см",
	            	max:"Не більше 2000 см"
	            },
	            volumetricHeight: {
	            	required: "Не менше 1 см",
	            	max:"Не більше 2000 см"
	            }
	            
	        },
	       
	    };
	    $.extend(true, cargo, global);
	    $("#ajax_form").validate(cargo);
	    	
	
	$("#cargoType").change(function(){
   if ($("#cargoType").val() == "Cargo"){
    $( "#ajax_form" ).validate().destroy();
	
    $.extend(true, cargo, global);
    $("#ajax_form").validate(cargo);
    	
    }
	   
    
    	if ($(this).val() == "Pallet"){
    	$( "#ajax_form" ).validate().destroy();
    	var pallet = {
			rules: {
				weight: {
	                required: true,
	                digits: true,
	                minlength: 1,
	                min: 200,
	                max: 1000
	                     },
	                     volumetricLength: {
	                         required: true,
	                         digits: true,
	                         minlength: 1,
	                         min: 50,
	                         max: 150
	                     },
	                     volumetricWidth: {
	                         required: true,
	                         digits: true,
	                         minlength: 1,
	                         min: 50,
	                         max: 150
	                     },
	                     volumetricHeight: {
	                         required: true,
	                         digits: true,
	                         minlength: 1,
	                         min: 50,
	                         max: 200,
	                     },       
					},
			messages: {
			    weight: {
			    	min: "Вага 1-ї палети не менше 200 кг",
			    	max: "Вага 1-ї палети не більше 1000 кг"
			 		},
					 volumetricLength: {
						 required: "Не менше 50 см",
						 min: "Не менше 50 см",
						 max: "Не більше 150 см"
			            },
			            volumetricWidth: {
			            	required: "Не менше 50 см",
			            	min: "Не менше 50 см",
			            	max: "Не більше 150 см"
			            },
			            volumetricHeight: {
			            	required: "Не менше 50 см",
			            	min: "Не менше 50 см",
			            	max: "Не більше 200 см"
			            },		
		 		}
			};
     $.extend(true, pallet, global);
    $("#ajax_form").validate(pallet);
		}
    
    
    
    
    	if ($(this).val() == "Documents"){
    	$( "#ajax_form" ).validate().destroy();
    	var Documents = {
						
			};
     $.extend(true, Documents, global);
    $("#ajax_form").validate(Documents);
		}
   
    

    
    	if ($(this).val() == "TiresWheels"){
    	$( "#ajax_form" ).validate().destroy();
    	var TiresWheels = {
			
			};
     $.extend(true, TiresWheels, global);
    $("#ajax_form").validate(TiresWheels);
		}
    });
    
    

});


$.extend( $.validator.messages, {
	required: "Це поле необхідно заповнити.",
	remote: "Будь ласка, введіть правильне значення.",
	email: "Будь ласка, введіть коректну адресу електронної пошти.",
	url: "Будь ласка, введіть коректний URL.",
	date: "Будь ласка, введіть коректну дату.",
	dateISO: "Будь ласка, введіть коректну дату у форматі ISO.",
	number: "Будь ласка, введіть число.",
	digits: "Вводите потрібно лише цілі цифри.",
	creditcard: "Будь ласка, введіть правильний номер кредитної карти.",
	equalTo: "Будь ласка, введіть таке ж значення ще раз.",
	extension: "Будь ласка, виберіть файл з правильним розширенням.",
	maxlength: $.validator.format( "Будь ласка, введіть не більше {0} символів." ),
	minlength: $.validator.format( "Будь ласка, введіть не менше {0} символів." ),
	rangelength: $.validator.format( "Будь ласка, введіть значення довжиною від {0} до {1} символів." ),
	range: $.validator.format( "Будь ласка, введіть число від {0} до {1}." ),
	max: $.validator.format( "Будь ласка, введіть число, менше або рівно {0}." ),
	min: $.validator.format( "Будь ласка, введіть число, більше або рівно {0}." )
} );