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

		this.label = function(){
			return typeof _this.ns == "undefined"? _this.model: [_this.ns, _this.model].join(".")
		}
		this.execute = function(params, callback){ maize.log( '<maize.domino.JsonRPCBuilder:' + _this.label() +'> execute]' , params );
			$.jsonRPC.request( _this.model,{ params : params, success: callback, error: maize.fault });
		};

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
