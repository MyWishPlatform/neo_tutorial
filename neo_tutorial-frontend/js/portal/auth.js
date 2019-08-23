$(document).ready(function() {
    const getCookie = function(c_name) {
        if(document.cookie.length > 0) {
            c_start = document.cookie.indexOf(c_name + "=");
            if(c_start != -1) {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if(c_end == -1) c_end = document.cookie.length;
                return unescape(document.cookie.substring(c_start,c_end));
            }
        }
        return "";
    };

    $(document).ajaxSend(function(elm, xhr, s) {
        if (s.type === "POST") {
            xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"));
        }
    });
});



const registrationUser = (data) => {
    data.username = data.email;
    return new Promise((resolve, reject) => {
        const ajax = $.ajax({
            method: "POST",
            url: '/api/rest-auth/registration/',
            data: data
        });
        ajax.done(function(result) {
            resolve(result);
        }).fail(function(error) {
            reject(error);
        });
    });
};

const authUser = (data) => {
    return new Promise((resolve, reject) => {
        const ajax = $.ajax({
            method: "POST",
            url: '/api/rest-auth/login/',
            data: data
        });
        ajax.done(function(result) {
            resolve(result);
        }).fail(function(error) {
            reject(error);
        });
    });
};

const forgotPassword = (data) => {
    return new Promise((resolve, reject) => {
        const ajax = $.ajax({
            method: "POST",
            url: '/api/rest-auth/password/reset/',
            data: data
        });
        ajax.done(function(result) {
            resolve(result);
        }).fail(function(error) {
            reject(error);
        });
    });
};




$(function() {
    const authForm = $('#auth-form');
    const authMenu = $('#modal-menu');
    const backLink = $('#back-to-form');
    const authFormMenuItems = $('.custom-modal_menu_item a', authForm);


    const regForm = $('#registration-form');
    const loginForm = $('#login-form');
    const forgotPasswordForm = $('#forgot-password-form');


    forgotPasswordForm.on('submit', function(event) {
        event.preventDefault();
        const data = {};
        for (let k in fields.forgot.fields) {
            data[k] = fields.forgot.fields[k].val();
        }
        forgotPassword(data).then(function(response) {
            openModal('success-reset-password');
        }, function(error) {
            const errors = error.responseJSON;
            for (let i in errors) {
                let fieldName = i === 'non_field_errors' ? 'email': i;
                fields.forgot.errors[fieldName].server.show();
                fields.forgot.errors[fieldName].server.html(errors[i].join("<br/>"));
            }
        });
        return false;
    });


    regForm.on('submit', function(event) {
        event.preventDefault();
        const data = {};
        for (let k in fields.register.fields) {
            data[k] = fields.register.fields[k].val();
        }
        registrationUser(data).then(function(response) {
            openModal('confirm-email');
        }, function(error) {
            const errors = error.responseJSON;
            for (let i in errors) {
                let fieldName = i === 'username' ? 'email': i === 'non_field_errors' ? 'password2': i;
                fields.register.errors[fieldName].server.show();
                fields.register.errors[fieldName].server.html(errors[i].join("<br/>"));
            }
        });
        return false;
    });


    loginForm.on('submit', function(event) {
        event.preventDefault();
        const data = {};
        for (let k in fields.signin.fields) {
            data[k === 'email' ? 'username' : k] = fields.signin.fields[k].val();
        }
        authUser(data).then(function() {
            window.location = window.location.href;
        }, function(error) {
            const errors = error.responseJSON;
            for (let i in errors) {
                let fieldName = i === 'username' ? 'email': 'non_field_errors' ? 'password': i;
                fields.signin.errors[fieldName].server.show();
                fields.signin.errors[fieldName].server.html(errors[i].join("<br/>"));
            }
        });
        return false;
    });


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


    let openedModal;

    const openModal = function(name) {
        if (openedModal) {
            closeModal(openedModal);
        }
        openedModal = name;
        $('[data-modal="' + name + '"]').show();
    };

    const closeModal = function(name) {
        if (openedModal === name) {
            openedModal = false;
        }
        $('[data-modal="' + name + '"]').hide();
    };

    $('[data-open-modal]').each(function() {
        const _th = $(this);
        _th.on('click', function() {
            openModal($(this).data('open-modal'));
        });
    });


    $('[data-close-modal]').each(function() {
        const _th = $(this);
        _th.on('click', function() {
            closeModal($(this).data('close-modal'));
        });
    });


});

