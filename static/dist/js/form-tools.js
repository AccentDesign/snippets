$.fn.formset = function () {
    /**
     * Use to dynamically create and reorder new formsets
     */
    var _this = this;
    var formClass = $(this).data('form-class');
    var emptyFormClass = $(this).data('empty-form-class');
    var prefix = $(this).data('form-prefix');
    var firstFormClass = 'first';
    var lastFormClass = 'last';
    var deletedFormClass = 'deleted';

    function makeClone() {
        var $original = $('.' + emptyFormClass);
        var $new = $($original).clone(true, true);
        $($new).removeClass(emptyFormClass);
        $($new).addClass(formClass);

        var $total = $('#id_' + prefix + '-TOTAL_FORMS').val();

        $new.find(':input, select, a, span, label').each(function() {
            if ($(this).attr('id')) {
                var $id = $(this).attr('id').replace('__prefix__', $total);
                $(this).attr({'id': $id});
            }
            if ($(this).attr('name')) {
                var $name = $(this).attr('name').replace('__prefix__', $total);
                $(this).attr({'name': $name});
            }
            if ($(this).attr('for')) {
                var $for = $(this).attr('for').replace('__prefix__', $total);
                $(this).attr({'for': $for});
            }
        });

        $total++;

        $('#id_' + prefix + '-TOTAL_FORMS').val($total);

        // if there is a markdownx re initialize it
        markdownx = $($new).find('.markdownx');
        if (markdownx) {
            new window.MarkdownX(
                markdownx[0],
                markdownx[0].querySelector('.markdownx-editor'),
                markdownx[0].querySelector('.markdownx-preview')
            );
        }

        $($original).before($new);
    }

    function visibleForms() {
        return $(_this).find('.' + formClass + ':visible');
    }

    function updateOrder() {
        visibleForms().each(function(index) {
            $( this ).find('input[id*="-order"]').val(index);
        });
    }

    function updateActions() {
        visibleForms().each(function(index) {
            $(this).removeClass(firstFormClass).removeClass(lastFormClass);
            if (index == 0) {
                $(this).addClass(firstFormClass);
            } else if (index == visibleForms().length - 1) {
                $(this).addClass(lastFormClass);
            }
        });
    }

    // make sortable

    $(_this).sortable({
        forcePlaceholderSize: true,
        cursor: "move",
        update: function(event, ui) {
            updateOrder();
            updateActions();
        }
    });

    // actions

    $(_this).on('click', '.action-up', function(){
        var current = $(this).closest('.' + formClass);
        current.prev().before(current);
        updateOrder();
        updateActions();
    });

    $(_this).on('click', '.action-down', function(){
        var current = $(this).closest('.' + formClass);
        current.next().after(current);
        updateOrder();
        updateActions();
    });

    $(_this).on('click', '.add-row', function(){
        makeClone();
        updateOrder();
        updateActions();
    });

    $(_this).on('change', 'input[id*="-DELETE"]', function () {
        if ($(this).is(':checked')) {
            $(this).closest('.' + formClass).addClass(deletedFormClass);
        } else {
            $(this).closest('.' + formClass).removeClass(deletedFormClass);
        }
    });

    return _this;
};

function slugify(text) {
    return text.toString().toLowerCase()
        .replace(/\s+/g, '-')           // Replace spaces with -
        .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
        .replace(/\-\-+/g, '-')         // Replace multiple - with single -
        .replace(/^-+/, '')             // Trim - from start of text
        .replace(/-+$/, '');            // Trim - from end of text
}

$(document).on('keyup', '#id_title', function () {
    var $slugField = $('#id_slug');
    if ($slugField) {
        var $slug = slugify($(this).val());
        $($slugField).val($slug);
    }
});
