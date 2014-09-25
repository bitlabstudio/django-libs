// Helper functions to load Twitter Bootstrap modals
// You have to use https://github.com/jschr/bootstrap-modal/ for this to work
// You also have to use the AjaxRedirectMiddleware that comes with django-libs
//
// You must place <div id="ajax-modal" class="modal hide fade" tabindex="-1"></div>
// at the end of your base.html

function renderModal($modal, data, textStatus, jqXHR, isNormalDiv) {
    // Helper function that either executes the redirect or renders the modal
    if (jqXHR.status == 278) {
        window.location.href = jqXHR.getResponseHeader("Location");
    } else {
        $('body').modalmanager('loading');
        $modal.html(data);
        if (isNormalDiv) {
           // do nothing
        } else {
            $modal.modal();
        }
    }
}

function getModalB3(modal_url, headline_text, callback) {
    // calls the modal for Bootstrap v3
    var $modal = $('#ajax-modal')
        ,$header;

    if (headline_text) {
        $header = $('<h4>' + headline_text + '</h4>');
    } else {
        $header = $('<span>&nbsp;</span>')
    }

    $('body').modalmanager('loading');
    $.get(modal_url, {}, function(data) {
        $('body').modalmanager('loading');
        $modal.find('.modal-header').prepend($header);
        $modal.find('.modal-body').html(data);
        $modal.modal('show');
        if (callback) {
            callback();
        }
    });
}

function getModal(url, get_data, $wrapper, isNormalDiv) {
    // Calls the modal with a GET request.
    //
    // :param url: The url that should return the modal's template
    // :param get_data: Either {} or something like {next: '/'}
    var $modal;
    if ($wrapper) {
        $modal = $wrapper;
    } else {
        $modal = $('#ajax-modal');
    }
    $('body').modalmanager('loading');
    $.get(url, get_data, function(data, textStatus, jqXHR) {
        renderModal($modal, data, textStatus, jqXHR, isNormalDiv);
    });
    return false;
}


function postModal(url, $form, $wrapper, isNormalDiv) {
    // Calls the modal with a POST request.
    //
    // :param url: The url that should return the modal's template
    // :param $form: The form to be posted as a jQuery object
    var $modal;
    if ($wrapper) {
        $modal = $wrapper;
    } else {
        $modal = $('#ajax-modal');
    }
    $('body').modalmanager('loading');
    $.post(url, $form.serializeArray(), function(data, textStatus, jqXHR) {
        renderModal($modal, data, textStatus, jqXHR, isNormalDiv);
    });
}
