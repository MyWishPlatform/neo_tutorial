$(function() {
    var lessonSections = $('#lesson-steps');

    if (!lessonSections.length) return;

    var anchors = [], activeAnchor;
    var lessonTitles = $('.lesson-content h3');



    if (!lessonTitles.length) {
        lessonSections.parent().hide();
    } else {
        lessonTitles.each(function(index) {

            var h3 = $(this);
            var li = $('<li>');
            var a =  $('<a>');
            var anchor = $('<a>');

            anchors.push(anchor);

            li.append(a);
            a.text(h3.text());

            anchor.data('link', a);

            var anchorId = 'section-' + (index + 1);
            a.attr('href', '#' + anchorId);
            anchor.attr('id', anchorId);

            anchor.prependTo(h3);
            lessonSections.append(li);

            if (!index) {
                a.addClass('active');
            }
        });
    }



    var win = $(window);

    var lessonRightSidebar = $('#lesson-right-sidebar');
    var rightSidebarContent = $('#lesson-right-sidebar_wrapper');


    var checkSidebarPosition = function() {
        var sidebarOffset = lessonRightSidebar.offset()['top'];
        var active;
        var indexAnchor = 0;
        var windowScrollTop = win.scrollTop();

        while (indexAnchor < (anchors.length - 1)) {
            if (anchors[indexAnchor].offset()['top'] < (windowScrollTop + win.height())) {
                active = anchors[indexAnchor];
            }
            indexAnchor++;
        }


        if (activeAnchor !==  active) {
            if (activeAnchor) {
                activeAnchor.data('link').removeClass('active');
                activeAnchor = false;
            }
            if (active) {
                activeAnchor = active;
                activeAnchor.data('link').addClass('active');
            }
        }

        if (sidebarOffset <= windowScrollTop) {
            rightSidebarContent.addClass('sidebar-fixed');
        } else {
            rightSidebarContent.removeClass('sidebar-fixed');
        }
    };

    win.on('scroll', checkSidebarPosition);

    var checkSidebarSize = function() {
        rightSidebarContent.width(lessonRightSidebar.width());
    };

    win.on('resize', checkSidebarSize);

    checkSidebarPosition();
    checkSidebarSize();

});
