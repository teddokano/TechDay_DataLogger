function ajaxUpdate( url, func, timeout = 5000 ) {
	url			= url + '?ver=' + new Date().getTime();
	
	if ( (timeout < 1000) && reqCount )
			return;	//	ignore since this is low priority request (avoid to disturb server response time)
		
	reqCount++;
	
	fetch( url, { signal: AbortSignal.timeout( timeout ) } )
		.then( response => {
		/*
			console.log( "response.ok = " + response.ok )
			console.log( "response.headers = " + response.ok )
			console.log( "Content-Type = " + response.headers.get( "Content-Type" ) )
		 */
			return response.text();
		} )
		.then( ( data ) => {
			func && func( data );
			if ( reqCount )
				reqCount--;
		} )
		.catch( ( error ) => {
			if ( reqCount )
				reqCount--;
			console.log( 'ajaxUpdate - fetch timeout ' + error )
		} );
}

function allSettingLoad() {
	let url	= REQ_HEADER + 'allreg='
	ajaxUpdate( url, allRegLoadDone );
}

function allRegLoadDone( data ) {
	let obj = JSON.parse( data );

	 for ( let i = 0; i < obj.reg.length; i++ ) {
		 setSliderAndRegisterlistValues( obj.reg[ i ], "register", i, allreg_loading = true )
	 }
}
window.addEventListener( 'load', function () {
	allSettingLoad();
} );
