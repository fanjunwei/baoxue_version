/**
 * Created with PyCharm.
 * User: fanjunwei003
 * Date: 14-1-30
 * Time: 14:13
 * To change this template use File | Settings | File Templates.
 */
var pageIndex=1;
var pageCount=1;

function onePageHtml(previous,next,index)
{
    txt=index.toString();
    if ((pageIndex<=1 && previous) || pageIndex>=pageCount && next) {
        if(previous)
        {
            return '<span class="disabled"> &lt; </span>';
        }
        else if(next)
        {
            return '<span class="disabled"> &gt; </span>';
        }
    } else if(index==pageIndex) {
        return '<span class="current">'+txt+'</span>';
    } else if(previous) {
        return '<a href="javascript:previousPage()"> &lt; </a>';
    } else if(next) {
        return '<a href="javascript:nextPage()"> &gt; </a>';
    } else {
        return '<a href="javascript:toPage('+index+')">'+txt+'</a>';
    }
}
function showSplitPages()
{

    if(pageCount>1)
    {
        html=[];
        var i=1;
        html.push(onePageHtml(true,false,-1));
        for (;i<=5 && i<=pageIndex-5;i++)
        {
            html.push(onePageHtml(false,false,i));
        }
        if(i<=pageIndex-5)
        {
            html.push('...');
            i=pageIndex-5+1;
        }
        for (; i<=pageIndex+5 && i<=pageCount-5;i++)
        {
            html.push(onePageHtml(false,false,i));
        }

        if(i<=pageCount-5)
        {
            html.push('...');
            i=pageCount-5+1;
        }

        for (; i<=pageCount;i++)
        {
            html.push(onePageHtml(false,false,i));
        }
        html.push(onePageHtml(false,true,-1));
        $('#pages').html(html.join(''));
    }
    else
    {
        $('#pages').html('');
    }
}
function previousPage()
{
    pageIndex--;
    if(pageIndex>pageCount){
        pageIndex=pageCount;
    }
    if(pageIndex<1){
        pageIndex=1;
    }
    toPage(pageIndex);
}
function nextPage()
{
    pageIndex++;
    if(pageIndex>pageCount){
        pageIndex=pageCount;
    }
    if(pageIndex<1){
        pageIndex=1;
    }
    toPage(pageIndex);
}
