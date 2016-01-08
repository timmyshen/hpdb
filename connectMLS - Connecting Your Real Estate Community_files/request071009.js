var _xmlHttp = null;

function getXMLHTTP()
{
	try { return new ActiveXObject("Msxml2.XMLHTTP.6.0"); } catch(e){
	try { return new ActiveXObject("Msxml2.XMLHTTP.3.0"); } catch(e){
	try { return new ActiveXObject("Msxml2.XMLHTTP"); } catch(e){
	try { return new ActiveXObject("Microsoft.XMLHTTP"); } catch(e){
	try { return new XMLHttpRequest() } catch(e){
		throw new Error( "This browser does not support XMLHttpRequest." );
	}}}}}
}

function evaluateResponse(x)
{
	x = x || _xmlHttp;
	return function()
	{
		if(x&&x.readyState==4&&x.responseText) 
		{
	   		eval(x.responseText);
		};
	}
};

function alertResponse(x)
{
	x = x || _xmlHttp;
	return function()
	{
		if(x&&x.readyState==4&&x.status==200) 
		{
			if (x.responseText.length > 0)
				alert(x.responseText);
		};
	}
};

function callResponse(f) 
{
	return function(x)
	{
		x = x || _xmlHttp;
		return function()
		{
			if(x&&x.readyState==4&&x.status==200) 
			{
				f(x.responseText);
			}
		}
	}
}

function initializeAjaxObject(ajaxObject)
{
	x = ajaxObject || _xmlHttp;
	
	if(_xmlHttp&&_xmlHttp.readyState!=0)
	{
		_xmlHttp.abort();
	}
	
	x = x || getXMLHTTP();
	
	if (!ajaxObject)
		_xmlHttp = x;
		
	return x;
}

function getResponse(where, callback, ajaxObject)
{
	x = initializeAjaxObject(ajaxObject);
	
	callback = callback || evaluateResponse;
	  
	if(_xmlHttp)
	{
		x.onreadystatechange = callback(x);
		x.open("GET",where,true);
		x.send(null);
	}	
}

function postParams(where, params, callback, ajaxObject)
{
	if (where && params)
	{
		x = initializeAjaxObject(ajaxObject);
		
		callback = callback || alertResponse;

		if(x)
		{
			x.onreadystatechange = callback(x);
			x.open("POST",where,true);
			x.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
			x.setRequestHeader("Content-length", params.length);
			x.setRequestHeader("Connection", "close");
			x.send(params);
		}
	}
}

function getForm(obj) 
{
	var params = "";
	for (i=0; i < obj.childNodes.length; i++) 
	{
		if (obj.childNodes[i].tagName == "INPUT")
		{
			if (obj.childNodes[i].type == "text")
			{
				params += obj.childNodes[i].name + "=" + escape(encodeURI(obj.childNodes[i].value)) + "&";
			}
			if (obj.childNodes[i].type == "checkbox")
			{
				if (obj.childNodes[i].checked) 
				{
					params += obj.childNodes[i].name + "=" + escape(encodeURI(obj.childNodes[i].value)) + "&";
				}
				else
				{
					params += obj.childNodes[i].name + "=&";
				}
			}
			if (obj.childNodes[i].type == "radio")
			{
				if (obj.childNodes[i].checked)
				{
					params += obj.childNodes[i].name + "=" + escape(encodeURI(obj.childNodes[i].value)) + "&";
				}
			}
		}
		else if (obj.childNodes[i].tagName == "TEXTAREA")
		{
			if (obj.childNodes[i].value.length > 0)
			{
				params += obj.childNodes[i].name + "=" + escape(encodeURI(obj.childNodes[i].value)) + "&";
			}
		}
		else if (obj.childNodes[i].tagName == "SELECT")
		{
			var sel = obj.childNodes[i];
			params += sel.name + "=" + escape(encodeURI(sel.options[sel.selectedIndex].value)) + "&";
		}
		else
		{
			var childParams = getForm(obj.childNodes[i]);
			if (childParams.length > 0)
				params += childParams;
		}
	}
	return params;
}

function postForm(where, formID)
{
	var form = document.getElementById(formID);
	if (where && formID && form)
	{
		var params = getForm(form);
		postParams(where, params);
	}
}
