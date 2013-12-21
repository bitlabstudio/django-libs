$(document).ready(function() {
    // showing the correct elements
    $('.libsImageWidgetHidden').hide();
    $('.libsImageWidget').show();

    // TODO styling to be moved into css file
    $('.libsImageWidgetControls').css({
        'display': 'inline-block'
    });
    $('.libsImageWidgetLabel').css('display', 'inline-block');
    $('.libsImageWidgetLabel input').css('margin', '0');
    $('.libsImageWidget a img').css({
        'vertical-align': 'top'
        ,'display': 'inline-block'
    });

    // pass click event to actual hidden file input
    $('.libsImageWidgetButton').on('click', function() {
        var input_id = $(this).attr('data-id');
        $(input_id).click();
        return false;
    })

    // display correct values
    $('.libsImageWidgetHidden input:file').each( function() {
        var fileInput = $(this);
        var input_id = '#' +  fileInput.attr('id');
        if ($('[data-label-for-id=' + input_id + ']').length | fileInput.val()) {
            $('[data-id=' + input_id + ']').text('Change file');
        }
        fileInput.change(function(){
            var value = fileInput.val();
            var filename = '...\\' + value.split('\\').slice(-1)
            $('[data-label-for-id=' + input_id + ']').text(filename);
        })
    });
})
