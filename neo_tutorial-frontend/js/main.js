
(function() {
    $(function() {
        var openedMenu = false;
        var profileBtn = $('#profile-btn');

        var closeProfileMenu = function() {
            toggleDisplayingMenu(false);
        };

        var toggleDisplayingMenu = function(val, event) {
            openedMenu = (val !== undefined) ? val : !openedMenu;
            profileBtn[openedMenu ? 'addClass' : 'removeClass']('opened');

            if (openedMenu) {
                $(window).on({
                    click: closeProfileMenu
                });
            } else {
                $(window).off({
                    click: closeProfileMenu
                });
            }

            event ? event.stopPropagation() : false;
        };

        profileBtn.on({
            'click': function(event) {
                toggleDisplayingMenu(undefined, event);
            },
            'mousedown': function(e) {
                e.preventDefault();
            }
        });
    });

    let visibilityEvent;
    let visibilityAttr;

    if (typeof document.hidden !== 'undefined') {
        visibilityAttr = 'hidden';
        visibilityEvent = 'visibilitychange';
    } else if (typeof document['msHidden'] !== 'undefined') {
        visibilityAttr = 'msHidden';
        visibilityEvent = 'msvisibilitychange';
    } else if (typeof document['webkitHidden'] !== 'undefined') {
        visibilityAttr = 'webkitHidden';
        visibilityEvent = 'webkitvisibilitychange';
    }

    if (typeof document.addEventListener === 'undefined' || visibilityAttr === undefined) {
        console.log('This demo requires a browser, such as Google Chrome or Firefox, that supports the Page Visibility API.');
    } else {
        document.addEventListener(visibilityEvent, () => {
            if (!document[visibilityAttr]) {
                window.location.reload();
            }
        }, false);
    }

})();



