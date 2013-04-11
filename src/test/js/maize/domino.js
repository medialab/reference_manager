( function( $, w, undefined ){
	/*


		Application dedicated domino
		configuration and modules
		Support Handlebars for template rendering.

	*/
	var maize = w.maize || {};
	maize.domino = {};
	maize.domino.api = {};
	maize.domino.urls = {};


	/*


		JsonRPC implementation
		======================

		Note: Require jsonRPC lib
		Thanks to:
		https://raw.github.com/datagraph/jquery-jsonrpc/master/jquery.jsonrpc.js

	*/
	maize.domino.JsonRPCBuilder = function( model, ns ){
		var _this = this;
		_this.model = model;
		_this.ns = ns;

		/*
			Print out the pseudo identifier for this jsonrpc wrapper
			
		*/
		this.label = function(){
			return typeof _this.ns == "undefined"? _this.model: [_this.ns, _this.model].join(".")
		}

		/*
			Execute the call, with jsonrpc params (usually a list) and a callback function.
			A proceed adn a fault arguments are available (but not necessary) to hook json response validation.
			Proceed function valudate the json result even if a "success" has been received.
			Cfr the default proceed and fault function.

			@param params -	list
			@param callback - function
			@param proceed - function (optional, override the existing one)
			@param fault - funciton (optional, override the existing one)
		*/
		this.execute = function( params, callback, proceed, fault ){ maize.log( '<maize.domino.JsonRPCBuilder:' + _this.label() +'> execute]' , params );
			$.jsonRPC.request( _this.model,{ 
				params : params,
				success: function( result ){ typeof proceed == "undefined"? _this.proceed( result, callback ):proceed( result, callback); }, 
				error: typeof fault == "undefined"?  _this.fault: fault });
		};

		/*
			Verify

		*/
		this.proceed = function( result, callback ){ maize.log( '<maize.domino.JsonRPCBuilder:' + _this.label() +'> proceed]' , result );
			// proceed to callback, check result.status == 'ok' or similar @todo !
			callback( result );
		}

		/*
			REAL FAULT
			(server not responding)
		*/
		this.fault =function( result ){ maize.log( '<maize.domino.JsonRPCBuilder:' + _this.label() +'> jsonrpc fault]' , data );
			maize.fault( result.error );
		}

		maize.log( '<maize.domino.JsonRPCBuilder:' + _this.label() +'> init]', model );
	};


	/*


		Domino properties dummy properties compiler
		===========================================

	*/
	maize.domino.compile = function( urls, ns ){ maize.log( '[maize.domino.compile]', typeof ns == "undefined"? "" :[ns, i].join(".") );
		var _api = {}; for (var i in urls ){ _api[ i ] = typeof urls[i] == 'string'? new maize.domino.JsonRPCBuilder( i, ns ): maize.domino.compile ( urls[i], typeof ns == "undefined"? i :[ns, i].join(".") );}
		return _api;
	}

	maize.domino.ready = function(){ maize.log( '[maize.domino.ready]' );
		$.jsonRPC.setup({ endPoint : 'http://localhost:8080', namespace : ''});
		maize.domino.api = maize.domino.compile( maize.domino.urls );

		$("#test-json").on("click", function(){ maize.domino.api.echo.execute([$("#echo_input").val()], function(data){maize.log(data); maize.toast( data.result, "received");}) });

		maize.d = new domino({
			properties: [
				
			], hacks:[

			]
		});

	};

	
	/*


			Domino Wrapper
			==============


	maize.domino = new domino({
		properties: [
		]
	});	
	*/
})( jQuery, window );
