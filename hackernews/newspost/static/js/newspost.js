
        $('#upvotes').click(function(event){
            console.log("Hi clicked")
    event.preventDefault();
    var catid;
    console.log(event);
    console.log(this.value);
    catid = this.value;
        // $.ajax({
        //     type:"POST",
        //     url:"/newspost:upvote_p/",
        //     data:{post_id: catid},
        //     success:function(data){
        //        $('#upvote_count').html(data);
        //        console.log("lol");
        //        $('#upvotes').hide();
        //    }
        // });
        jQuery.get('/newspost/upvote_p/', {post_id: catid}, function(data){
            console.log(document.getElementById('upvote_count'));
            document.getElementById('upvote_count').innerHTML=data;
               // $('#upvote_count').html(data);
            document.getElementById('upvotes').style.visibility ='hidden';
           });


});

$('.votearrow').click(function(e){
            console.log("Hi clicked")
    e.preventDefault();
    var cid;
    console.log(event);
    console.log(this.value);
     cid = this.value;
        // $.ajax({
        //     type:"POST",
        //     url:"/newspost:upvote_p/",
        //     data:{post_id: catid},
        //     success:function(data){
        //        $('#upvote_count').html(data);
        //        console.log("lol");
        //        $('#upvotes').hide();
        //    }
        // });
        jQuery.get('/newspost/upvote_c/', {comment_id: cid}, function(data){
            document.getElementById('comment-count'+cid).innerHTML=data;
               // $('#upvote_count').html(data);
            // document.getElementById('upvote'+cid).style.visibility ='hidden';
           });


});


// $(document).ready(function(){ $("#upvotes").on('click',function(e){ e.preventDefault(); $.ajax({type: "POST", url: "/newspost/upvote_p/", data: { post_id: $("#upvotes").val()   }, success:function(result){ $("#upvote_count").html(data); }}); }); });
     // $.get('/newspost/upvote_p/', {post_id: postid}, function(data){
     //           $('#upvote_count').html(data);
     //           console.log("lol");
     //           $('#upvotes').hide();
     //       });

