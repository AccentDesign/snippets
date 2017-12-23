function cloneFormsetRow(selector, type) {
    var $newElement = $(selector).clone(true, true).removeClass('empty-form');
    var $total = $('#id_' + type + '-TOTAL_FORMS').val();

    $newElement.find(':input, select, a, span, label').each(function() {
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

    $('#id_' + type + '-TOTAL_FORMS').val($total);

    // if there is a markdownx re initialize it
    markdownx = $($newElement).find('.markdownx');
    if (markdownx) {
        new window.MarkdownX(
            markdownx[0],
            markdownx[0].querySelector('.markdownx-editor'),
            markdownx[0].querySelector('.markdownx-preview')
        );
    }

    $(selector).before($newElement);
}

$(document).on('change', '.formset input[id*="-DELETE"]', function () {
    if ($(this).is(':checked')) {
        $(this).closest('.formset').addClass('deleted');
    } else {
        $(this).closest('.formset').removeClass('deleted');
    }
});

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
