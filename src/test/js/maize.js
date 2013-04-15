( function( $, w, undefined ){

	maize = w.maize || {};
	maize.vars = maize.vars || {};
	maize.urls = maize.urls || {};

	/*


	    Logs
	    ====

	*/
	maize.log = function(){
		try{
			var args = ['maize:'].concat( Array.prototype.slice.call(arguments) );
			console.log.apply(console, args );
		} catch(e){
				
		}
	}

	/*


		WINDOW On / Trigger helpers
		===========================
	*/
	maize.on = function( eventType, callback ){
		$(window).on( eventType, callback );
	};

	maize.trigger = function ( eventType, data ){
		$(window).trigger( eventType, data );
	};


	/*


	    Restful API
	    ===========

	*/
	maize.api = { 
		settings:{
			'get':{dataType:"Json",type:"GET",fault:maize.fault } ,
			'post':{dataType:"Json",type:"POST",fault:maize.fault }
		}
	};

	maize.api.init = function(){
		maize.vars.csrftoken = maize.fn.get_cmaizekie('csrftoken');
		$.ajaxSetup({
			crossDomain: false, // obviates need for sameOrigin test
			beforeSend: function(xhr, settings) { if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type))){ xhr.setRequestHeader("X-CSRFToken", maize.vars.csrftoken);}}
		});maize.log("[maize.api.init]");
	}

	maize.api.process = function( result, callback, namespace ){
		if( result.status == 'ok'){
			if (typeof callback == "object"){
				maize.toast( callback.message, callback.title );
			} else return callback( result );
		} else if( result.code == 'IntegrityError' ){
			$("#"+namespace+"_slug").addClass("invalid");
			maize.toast(  maize.i18n.translate("this slug is already used") , maize.i18n.translate("error"), {stayTime:3000, cleanup: true});
		} else if( typeof result.error == "object" ){
			maize.invalidate( result.error, namespace );
			maize.toast(  maize.i18n.translate("invalid form") , maize.i18n.translate("error"), {stayTime:3000, cleanup: true});
		} else {
			maize.toast( result.error , maize.i18n.translate("error"), {stayTime:3000, cleanup: true});
		}
	}

	maize.api.urlfactory = function( url, factor, pattern ){
		if( typeof factor == "undefined" ){ ds.log("[ds.m.api.urlfactory] warning'"); return url; };
		pattern = typeof pattern == "undefined"? "/0/":pattern ;
		return url.replace( pattern, ["/",factor,"/"].join("") )
	}

	/*
		Handle with care. 
		This function add a add+edit+remove+get function to maize.api.<your model>
		E.g to add a filter to maize.api.serie.get:

			maize.api.compile('serie');
			
			maize.magic.serie.list = function( result ){
				alert('list');
			}

			maize.api.serie.list({
				'filters': JSON.stringify({
					"language":"fr"
				})
			});

		Cfr. maize.api.Builder

		@param model	- your model, a.k.a maize.api namespace
	 	
	*/
	maize.api.compile = function( model ){ maize.log( '[maize.api.compile ]', model );
		maize.api[ model ] = new maize.api.Builder( model )
	}



	maize.api.Builder = function( model ){

		var instance = this;
		
		this.methods = [ 'get', 'list', 'add', 'remove', 'edit' ];
		this.model = model;

		this.get = function( params, callback ){

			instance.ajax( 'get', 'get', params, maize.api.urlfactory( maize.urls[ 'get_' + instance.model ], params.id ), callback  );
		}

		this.edit = function( params, callback ){

			instance.ajax( 'post', 'edit', params, maize.api.urlfactory( maize.urls[ 'edit_' + instance.model ], params.id ), callback  );
		}

		this.list = function( params, callback ){
			instance.ajax( 'get', 'list', params, maize.urls[ 'list_' + instance.model ], callback );
		}

		this.add = function( params ){
			instance.ajax( 'post', 'add', params, maize.urls[ 'add_' + instance.model ] );
		}

		this.remove = function( params ){
			params['method'] = 'DELETE'
			instance.ajax( 'delete', 'remove', params, maize.api.urlfactory( maize.urls[ 'remove_' + instance.model ], params.id ) );
		}

		this.ajax = function( http_method, method, params, url, callback ){
			maize.log( '[maize.api.' + instance.model + '.' + method + '] url :', url, ", params :",params );
			$.ajax( $.extend( maize.api.settings[ http_method ],{
				url: url,
				data: params,
				success:function(result){ maize.log( '[maize.api.' + instance.model + '.' + method + '] result :', result );
					maize.api.process( result, typeof callback == "undefined" ? maize.magic[ instance.model ][ method ]: callback, typeof params.auto_id == "undefined"? "id_" + method + "_" + instance.model: params.auto_id );
			}}));
		}

		// check urls availability
		for( i in instance.methods ){
			maize.log('[maize.api.Builder:' + instance.model +']', 'urls ', instance.methods[i] + '_' + instance.model, ":", typeof maize.urls[ instance.methods[i] + '_' + instance.model ] != "undefined" )
		}

	}


	/*


	    Modals (Bmaizetstrap)
	    ==================

	*/
	maize.modals = {}
	maize.modals.init = function(){ 
		$(".modal").each( function( i, el ){ var $el = $(el); $(el).css("margin-top",- Math.round( $(el).height() / 2 )); }); maize.log("[maize.modals.init]");
	};


	/*


	    Tmaizeltip
	    =======

	*/
	maize.tmaizeltip = {}
	maize.tmaizeltip.init = function(){
		$('body').tmaizeltip({ selector:'[rel=tmaizeltip]', animation: false, placement: function( tmaizeltip, caller ){ var placement = $(caller).attr('data-tmaizeltip-placement'); return typeof placement != "undefined"? placement: 'top'; } }); maize.log("[maize.tmaizeltip.init]");};


	/*


	    Toast
	    =====

	*/
	maize.toast = function( message, title, options ){
		if(!options){options={}}if(typeof title=="object"){options=title;title=undefined}if(options.cleanup!=undefined)$().toastmessage("cleanToast");var settings=$.extend({text:"<div>"+(!title?"<h1>"+message+"</h1>":"<h1>"+title+"</h1><p>"+message+"</p>")+"</div>",type:"notice",position:"middle-center",inEffectDuration:200,outEffectDuration:200,stayTime:3e3},options);$().toastmessage("showToast",settings)
	};


	/*


	    Invalidate, Fault
	    =================

	*/
	maize.invalidate = function( errors, namespace ){ if (!namespace){ namespace = "id";} maize.log("[maize.invalidate] namespace:",namespace, " errors:",errors );
		for (var i in errors){
			if( i.indexOf("_date") != -1  ){
				$("#"+namespace+"_"+i+"_day").parent().addClass("invalid");	
				continue;
			} else if (i.indexOf("_type") != -1 ){
				$("#"+namespace+"_"+i).parent().addClass("invalid");
				continue;
			} else if( i.indexOf("_hours") != -1 || i.indexOf("_minutes") != -1  ) {
				$("#"+namespace+"_"+i).parent().addClass("invalid");
				continue;	
			} else if(i.indexOf("captcha") != -1 ) {
				$("#recaptcha_response_field").addClass("invalid");
				continue;
			}
			$("#"+namespace+"_"+i).addClass("invalid");
		}
	}

	maize.fault = function( message ){ maize.log("[maize.fault] message:", message );	
		message = typeof message == "undefined"? "": message;
		maize.toast( message, maize.i18n.translate("connection error"), {stayTime:3000, cleanup: true});
	}


	/*


	    Common function
	    ===============

	*/
	maize.fn = {};
	maize.fn.slug = function( sluggable ){
		return sluggable.replace(/[^a-zA-Z 0-9-]+/g,'').toLowerCase().replace(/\s/g,'-');
	};

	maize.fn.get_cmaizekie = function (e){
		var t=null;if(document.cmaizekie&&document.cmaizekie!=""){var n=document.cmaizekie.split(";");for(var r=0;r<n.length;r++){var i=jQuery.trim(n[r]);if(i.substring(0,e.length+1)==e+"="){t=decodeURIComponent(i.substring(e.length+1));break}}}return t
	};

	maize.fn.wait = function( fn, delay ){
		var timer = md5( fn.toString() + delay );
		clearTimeout( maize.vars[  timer ] );
		maize.vars[  timer ] = setTimeout( fn, delay ); 

	}

	/*


	    I18n
	    ====

	*/
	maize.i18n = { lang:'fr-FR'};
	maize.i18n.translate = function( key ){
		var l = maize.i18n.lang;
		if ( maize.i18n.dict[l][key] == undefined	)
			return key;
		return 	maize.i18n.dict[l][key];
	}

	maize.i18n.dict = {
		'fr-FR':{
			"connection error":"Connection error",
			"warning":"Attention",
			"delete selected absence":"Voulez-vous supprimer cette absence?",
			"offline device":"Échec de la connexion.",
			"check internet connection":"Veuillez vérifier la connexion internet de la tablette.",
			"welcome back":"welcome back",
			"loading":"chargement en cours…",
			"form errors":"Erreurs dans le formulaire",
			"error":"Erreur",
			"invalid form":"Veuillez vérifier les champs en rouge.",
			"empty dates":"Les dates de dé en rouge.",
			"empty message field":"Le message est vide.",
			"message sent":"Message envoyé",
			"timeout device":"Connexion trop lente.",
			"try again later": "Veuillez réessayer dans quelques instants.",
			"saving":"enregistrement en cours…",
			"changes saved":"Modifications Sauvegardées",
			"changes saved successfully":"Modifications Sauvegardées",
			"password should be at least 8 chars in length":"Le mot de passe doit faire au moins 8 caractères.",
			"password tmaize short":"Le mot de passe est trop court",
			"password changed":"Le mot de passe a été changé",
			"new passwords not match":"Saisissez à nouveau le nouveau mot de passe.",
			"invalid password":"Veuillez vérifier votre ancien mot de passe en respectant les minuscules et les majuscules.",
			"sms message sent":"SMS envoyé(s) avec succès.",
			"sms message sent failed":"Le SMS n'a pas pu être envoyé.",
			"sms invalid message":"Le texte du SMS est invalide.",
			"sms invalid phone numbers":"Numéro(s) de téléphone invalide(s)",
			"list numbers sms failure":"Certains SMS n'ont pu être envoyés.",
			"to change password": "Veuillez changer votre <br/> <b>mot de passe</b>",
			"please check accepted terms": "Veuillez accepter les conditions d'utilisation",

		}
	};


	/*


	    Bibtex
	    ======

	*/
	maize.fn.bibtex = function ( bibtex ){
		var bibjson = bibtex.replace(/^\s+|\s+$/g,'')
			.replace(/(\w+)\s*=\s*\{+/g,"\"$1\": \"")
			.replace(/\}+(?=\s*[,\}+])/g,"\"")
			.replace(/@(\w+)\s*\{([^,]*)/,"{\"bibtext_key\":\"$1\",\"$1\": \"$2\"");
		maize.log( bibjson )
		return JSON.parse(bibjson);
	}

})( jQuery, window.maize || {} );

