function store_order(items, url) {
    var order = new Array();
    for(var i = 0; i < items.length; i++) {
        order[i] = items[i].id;
    }
    $.ajax({
        type: "POST",
        url: url + '/@@reorder',
        data: 'items=' + order
    });
    
}

$(document).ready(function() { 
    $("ul.sortable").sortable({
        placeholder: 'ui-state-highlight',
        update : function () {
            var container = $(this).closest('.container');
            store_order($('.item', container), this.id);
        }
    });
    
    $("button.up").click(function() {
        var container = $(this).closest('.container');
        var item = $(this).closest('.item');
        var items = $(item).parent().children('.item');
        if(items.index(item) > 0) {
            $(item).insertBefore(items[items.index(item)-1]);
            store_order($(item).parent().children('.item'), container[0].id);
        }
    });
    
    $("button.down").click(function() {
        var container = $(this).closest('.container')[0];
        var item = $(this).closest('.item');
        var items = $(item).parent().children('.item');
        if(items.index(item) < items.length) {
            $(item).insertAfter(items[items.index(item)+1]);
            store_order($(item).parent().children('.item'), container.id);
        }
    });
    
});