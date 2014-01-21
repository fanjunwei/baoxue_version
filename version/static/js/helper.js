	function deleteConfim(callback)
	{
        $( "#dialog-confirm" ).dialog('open');
	}
    function checkUnique(id)
    {
        if($('#'+id).val().length<=0)
        {
            $('#'+id+'Msg').show();
            $('#'+id+"Msg").text('*');
            return false;
        }
        else
        {
            $('#'+id+"Msg").hide();
            return true;
        }

    }
    function showMessage(msg)
    {
        $("#msg1").text(msg);
        $("#msg1").show();
        $('#msg1').delay(3000).hide(0);
    }
    $(function(){
        $( "#dialog-confirm" ).dialog({
            resizable: false,
            height:165,
            modal: true,
            autoOpen:false,
            title:"删除确认",
            buttons: {
                "删除": function() {
                    callback();
                    $( this ).dialog( "close" );
                },
                "取消": function() {
                    $( this ).dialog( "close" );
                }
            }
        });
    });
    function htmlEncode(str) {
        var s = "";
        if (str.length == 0) return "";
        s = str.replace(/&/g, "&amp;");
        s = s.replace(/</g, "&lt;");
        s = s.replace(/>/g, "&gt;");
        s = s.replace(/'/g, "&apos;");
        s = s.replace(/"/g, "&quot;");
        s = s.replace(/[\n]/g, "<br/>");
        return s;
    }
