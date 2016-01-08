
$(function (){
	$("[truncate]").each(function(){
		var $this = $(this), lim = parseInt($this.attr("truncate"));
		var text = $this.text();
		if(text.length > (lim + 3))
			{
				$this.text(text.substring(0,lim));
				$this.append("<span class=\"imghover\" onmouseover=\"$(this).siblings('.hover-container').fadeToggle('fast') \" onmouseout=\"$(this).siblings('.hover-container').fadeToggle('fast') \">&nbsp;<img border=\"0\" height=\"10px\" src=\"/images/icons/ellipsis.png\"></span>");
				var container ="<div class=\"hover-container\" style=\"display:none;position:absolute;z-index:100;\">"
				+ "<fieldset style=\"background-color:#EFEFEF;\">" + "<b>" + text +
				"</b>" + "</fieldset></div>";
				$this.append(container);
			}		
	});
});
		