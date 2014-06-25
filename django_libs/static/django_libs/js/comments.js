/*
 * Comment fetching and pagination utilities.
 *
 */

// TODO Security is not optimal. A user could find out how to ping the view and
// fetch the comments without being allowed to.
// We could add some kind of security token like the csrf_token, that enables
// the user to fetch the comments and otherwise it is refused.

function showLoader() {
    var $comments_container = $('[data-id=ajaxComments]');
    var $ajaxloader = $comments_container.find('[data-class=ajaxloader]');
    if ($ajaxloader.length) {
        $ajaxloader.show();
    }
}

function hideLoader() {
    var $comments_container = $('[data-id=ajaxComments]');
    var $ajaxloader = $comments_container.find('[data-class=ajaxloader]');
    if ($ajaxloader.length) {
        $ajaxloader.hide();
    }
}

function fetchComments($comments_container, new_page, comment_pk) {
    /*
     * Fetches the comments from the specified url and populates the comment
     * container with them
     */
    var comment_view_url = $comments_container.attr('data-comments-url');
    var ctype = $comments_container.attr('data-ctype');
    var object_pk = $comments_container.attr('data-object-pk');
    var full_url = (
        comment_view_url + '?ctype=' + ctype + '&object_pk=' + object_pk);

    if (!(comment_view_url && ctype && object_pk)) {
        console.warn('Comments wrapper missing important data.');
    } else {
        if (!new_page) {
            new_page = 1;
        }

        if (new_page) {
            full_url = full_url + '&page=' + new_page;
        }

        if (comment_pk) {
            full_url = full_url + '&comment_pk=' + comment_pk;
        }

        showLoader();

        $.ajax({
            url: full_url
            ,success: function(response) {
                $comments_container.html(response.data);
                $comments_container.attr('data-page', response.page);
                $comments_container.attr('data-has-previous', response.has_prev);
                $comments_container.attr('data-has-next', response.has_next);
                hideLoader();
            }
            ,error: function() {
                hideLoader();
            }
        });
    }
}

function getCommentId() {
    var comment_pk;
    var split_query = window.location.search.substring(1).split('&');

    for (var i=0; i<split_query.length; i++) {
        if (split_query[i].indexOf('c=') === 0) {
            comment_pk = split_query[i].substring(2);
        }
    }

    return comment_pk;
}

$(document).ready(function() {
    var $comments_container = $('[data-id=ajaxComments]');
    var comment_pk = getCommentId();

    // only proceed if a comment element is on this page. It could be hidden
    // for permission purposes
    if ($comments_container.length) {
        fetchComments($comments_container, 0, comment_pk);
    }
});

$(document).on('click', 'a[data-class=comment-page-next]', function(e) {

    e.preventDefault();

    var $comments_container = $('[data-id=ajaxComments]');
    var has_next = $comments_container.attr('data-has-next') === "true";
    var new_page = parseInt($comments_container.attr('data-page')) + 1;

    if (has_next) {
        fetchComments($comments_container, new_page);
    }

});

$(document).on('click', 'a[data-class=comment-page-previous]', function(e) {

    e.preventDefault();

    var $comments_container = $('[data-id=ajaxComments]');
    var has_previous = $comments_container.attr('data-has-previous') === "true";
    var new_page = parseInt($comments_container.attr('data-page')) - 1;

    if (has_previous) {
        fetchComments($comments_container, new_page);
    }

});

$(document).on('click', 'a[data-class=comment-page-direct]', function(e) {

    e.preventDefault();

    var $comments_container = $('[data-id=ajaxComments]');
    var current_page = parseInt($comments_container.attr('data-page'));
    var new_page = parseInt($(this).attr('data-page'));

    if (current_page !== new_page) {
        fetchComments($comments_container, new_page);
    }

});
