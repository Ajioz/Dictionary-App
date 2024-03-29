window.onload = function(){
  $('#myModal').modal('show');
  $('#word-form').hide();
  $('#logo-form').hide();
  $('.edit-word, .edit-meaning').hide();
  $('.submit, .cancel').parent().hide();

  $('#word-index').click(function(){
    location.reload();
  });

  //Create Operation
  $('#word-form').submit(function(){
    let word = $('#word').val();
    let meaning = $('#meaning').val();

    $.ajax({
      url: '/word',
      type: 'POST',
      dataType: 'json',
      data: JSON.stringify({
        'word': word,
        'meaning':meaning
      }),
      contentType: 'application/json, charset=UTF-8',
      success: function(data) {
        location.reload();
      },
      error: function(err){
        console.log(err);
      }
    });
  });

  $('#word-add').click(function(){
    $('#word-index, #logo-add').removeClass('side-active');
    $(this).addClass('side-active');
    $('#word-form').show();
    $('#logo-form').hide();
  });

  $('#cancel').click(function(){
    location.reload();
  });

  //Logo Add Operation
  $('#logo-add').click(function(){
    $('#word-index, #word-add').removeClass('side-active');
    $(this).addClass('side-active');
    $('#word-form').hide();
    $('#logo-form').show();
  });

  $('#logo-cancel').click(function(){
    location.reload();
  });

  $('#logo-form').submit(function(){
    let data = new FormData();
    data.append('file', $('#logo')[0].files[0]);

    $.ajax({
      url: '/add_logo',
      type: 'POST',
      data: data,
      enctype: 'multipart/form-data',
      processData: false,
      contentType: false,
      success: function(data) {
        location.reload();
      },
      error: function(err){
        console.log(err);
      }
    });
  });


  //Delete Operation
  $('.delete').click(function(){
    let word_id = $(this).attr('id');

    $.ajax({
      url: '/word/' + word_id + '/delete',
      type: 'POST',
      success: function(data) {
        location.reload();
      },
      error: function(err){
        console.log(err);
      }
    });
  });

  //Update Operation
  $('.edit').click(function(){
    let parent = $(this).parents('tr');
    parent.find('.edit-word, .edit-meaning').show();
    parent.find('.word-word, .word-meaning').hide();
    parent.find('.submit, .cancel').parent().show();
    parent.find('.edit, .delete').parent().hide();
  });

  $('.cancel').click(function(){
    location.reload();
  });

  // Submitting Updated Operation
  $('.update-form').submit(function(){
    let parent = $(this).parents('tr');
    let word = parent.find('input').val();
    let meaning = parent.find('textarea').val();
    let word_id =  parent.find('.submit').attr('id');

    $.ajax({
      url: '/word/' + word_id + '/edit',
      type: 'POST',
      dataType: 'json',
      data: JSON.stringify({
        'word': word,
        'meaning':meaning
      }),
      contentType: 'application/json, charset=UTF-8',
      success: function(data) {
        location.reload();
      },
      error: function(err){
        console.log(err);
      }
    });
  });
}