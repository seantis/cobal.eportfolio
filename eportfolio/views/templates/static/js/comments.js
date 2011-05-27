$(document).ready (function() {
    $('.add-comment').live('click', function() {
        $('.comment-panel', $(this).parents('div.journal-entry')).slideToggle('fast');
        $('textarea#comment_text', $(this).parents('div.journal-entry')).focus();
        return false;
    });
});

$(document).ready (function() {
    $('.add_comment').live('click', function() {
        var container = $(this).closest('.comments_container')[0];
        var text = $('.comment_text', container)[0].value;
        $.ajax({
            type: "POST", 
            url : container.id + 'add',
            data : {'comment_text' : text },
            success: function(data) {
                data = $.parseJSON(data);
                $(document.getElementById(data['id'])).html(data['html']);
                
                // Restore button
                $(".remove").button({
                    icons: {
                        primary: 'ui-icon-trash'
                    }
                });
                
            }
        });
        return false;
    });
});