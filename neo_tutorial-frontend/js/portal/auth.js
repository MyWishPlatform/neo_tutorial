$(function() {
    const authForm = $('#auth-form');
    const authMenu = $('#modal-menu');
    const backLink = $('#back-to-form');
    const authFormMenuItems = $('.custom-modal_menu_item a', authForm);



    const fields = {};


    let activeForm;

    const showForm = (event) => {

        const element = $(event.target).is('[data-form-link]') ? $(event.target) : $(event.target).parents('[data-form-link]').first();

        const formName = element.data('form-link');

        const allLinks = $('[data-form-link="' + formName + '"]').addClass('active');

        if (activeForm && (activeForm.name !== formName)) {
            activeForm.links.removeClass('active');
            activeForm.form.hide();
        }

        const form = $('[data-form="' + formName + '"]');

        form.show();

        if (formName === 'forgot') {
            authMenu.hide();
            backLink.show();
        } else {
            authMenu.show();
            backLink.hide();
        }

        activeForm = {
            links: allLinks,
            form: form,
            name: formName
        };
    };
    authFormMenuItems.on('click', showForm);
    authFormMenuItems.eq(0).click();


    const validateForm = function(formFields) {
        let isValid = true;
        for (let k in formFields.fields) {
            const field = formFields.fields[k];

            formFields.errors[k].all.hide();

            switch(k) {
                case 'email':
                    if (field.get(0).validity.valueMissing) {
                        formFields.errors['email'].required ?
                            formFields.errors['email'].required.show() : false;
                    } else if (field.get(0).validity.typeMismatch) {
                        formFields.errors['email'].email ?
                            formFields.errors['email'].email.css({display: 'block'}) : false;
                    }
                    break;

                case 'password1':
                    if (field.get(0).validity.valueMissing) {
                        formFields.errors['password1'].required.show();
                    } else if (field.get(0).validity.tooShort) {
                        formFields.errors['password1'].minlength.show();
                    }
                    break;

                case 'password2':
                    if (formFields.fields['password2'].val() !== formFields.fields['password1'].val()) {
                        formFields.fields['password2'].get(0).setCustomValidity("Invalid");
                        if (formFields.fields['password2'].val()) {
                            formFields.errors['password2'].match.show();
                        }
                    } else {
                        formFields.fields['password2'].get(0).setCustomValidity("");
                    }
                    break;
            }

            if (!field.get(0).validity.valid) {
                isValid = false;
            }
        }
        if (!isValid) {
            formFields.button.attr('disabled', 'disabled');
        } else {
            formFields.button.removeAttr('disabled');
        }
    };

    $('form', authForm).each(function() {
        const form = $(this);
        const formFields = fields[form.attr('name')] = {
            button: $('button[type="submit"]', form),
            form: form,
            fields: {},
            errors: {}
        };

        $('input', form).each(function() {
            const _this = $(this);
            const fieldName = _this.attr('name');
            formFields.fields[fieldName] = _this;

            formFields.errors[fieldName] = {
                all: $('.form-control_errors[data-field="' + fieldName + '"]', form)
            };

            formFields.errors[fieldName].all.each(function() {
                const _thisError = $(this);
                formFields.errors[fieldName][_thisError.data('error')] = _thisError;
            });

            _this.on('keydown keyup change paste', function() {
                setTimeout(function() {
                    _this.addClass('touched');
                    validateForm(formFields);
                });
            });
        });

        validateForm(formFields);
    });

    $('[data-open-form]').each(function() {
        const _th = $(this);
        _th.on('click', showForm);
    });


    $('[data-open-modal]').each(function() {
        const _th = $(this);
        _th.on('click', function() {
            $('[data-modal="' + $(this).data('open-modal') + '"]').show();
        });
    });


    $('[data-close-modal]').each(function() {
        const _th = $(this);
        _th.on('click', function() {
            $('[data-modal="' + $(this).data('close-modal') + '"]').hide();
        });
    });


});

