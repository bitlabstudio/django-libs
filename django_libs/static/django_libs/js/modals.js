// Helper functions to load Twitter Bootstrap modals
// You have to use https://github.com/jschr/bootstrap-modal/ for this to work
// You also have to use the AjaxRedirectMiddleware that comes with django-libs
//
// You must place <div id="ajax-modal" class="modal hide fade" tabindex="-1"></div>
// at the end of your base.html

function renderModal($modal, data, textStatus, jqXHR) {
    // Helper function that either executes the redirect or renders the modal
    if (jqXHR.status == 278) {
        window.location.href = jqXHR.getResponseHeader("Location");
    } else {
        $('body').modalmanager('loading');
        $modal.html(data);
        $modal.modal();
    }
}


function getModal(url, get_data) {
    // Calls the modal with a GET request.
    //
    // :param url: The url that should return the modal's template
    // :param get_data: Either {} or something like {next: '/'}
    var $modal = $('#ajax-modal');
    $('body').modalmanager('loading');
    $.get(url, get_data, function(data, textStatus, jqXHR) {
        renderModal($modal, data, textStatus, jqXHR);
    });
    return false;
}


function postModal(url, $form) {
    // Calls the modal with a POST request.
    //
    // :param url: The url that should return the modal's template
    // :param $form: The form to be posted as a jQuery object
    var $modal = $('#ajax-modal');
    $('body').modalmanager('loading');
    $.post(url, $form.serializeArray(), function(data, textStatus, jqXHR) {
        renderModal($modal, data, textStatus, jqXHR);
    });
}
