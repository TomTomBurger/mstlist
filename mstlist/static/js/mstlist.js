//サイドバーの開閉処理 
$(function(){
    $('#js-sidebar').click(function() {
        $('.ui.sidebar').sidebar('toggle');
    });
})

//削除ボタン メッセージ
$('input:visible').first().focus();
$(function(){
  $(".btn_remove").click(function(){
        if(confirm("削除しますか？")){
            //yesの処理（何もぜず進む）
        }else{
            //cancelの処理
            return false;
        }
    });
})

//dropdown
$(function(){
    $('.ui.dropdown').dropdown();
})

$(function(){
    $('.ui.pointing.dropdown.link.item').dropdown();
})
