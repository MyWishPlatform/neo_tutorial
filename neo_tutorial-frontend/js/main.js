require('./constants');
require('./services/request');
require('./directives');

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
})();


require('./portal/lesson');


