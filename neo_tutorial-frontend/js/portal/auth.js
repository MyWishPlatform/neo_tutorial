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
    data.username = data.email = data.email.toLowerCase();
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
    data.username = data.username.toLowerCase();
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

const resetPasswordConfirm = (data) => {
    return new Promise((resolve, reject) => {

        const ajax = $.ajax({
            method: "POST",
            url: `/api/rest-auth/password/reset/confirm/${data.uid}/${data.token}/`,
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
    const resetPasswordForm = $('#new-password-form');


    resetPasswordForm.on('submit', function(event) {
        event.preventDefault();
        const parsedPath = location.pathname.replace(/^\//, '').split('/').slice(1, 3);
        const data = {
            uid: parsedPath[0],
            token: parsedPath[1]
        };

        for (let k in fields['new-password'].fields) {
            data[k] = fields['new-password'].fields[k].val();
        }
        resetPasswordForm.addClass('in-progress');
        resetPasswordConfirm(data).then(function() {
            window.history.replaceState(null, null, '/login/');
            openModal('auth');
        }, function(error) {
            const errors = error.responseJSON;
            for (let i in errors) {
                let fieldName = ((i === 'non_field_errors') || (i === 'token')) ? 'new_password2': i;
                if (!fields['new-password'].errors[fieldName]) return;
                fields['new-password'].errors[fieldName].server.show();
                fields['new-password'].errors[fieldName].server.html(errors[i].join("<br/>"));
            }
        }).finally(() => {
            resetPasswordForm.removeClass('in-progress');
        });
        return false;
    });

    forgotPasswordForm.on('submit', function(event) {
        event.preventDefault();
        const data = {};
        for (let k in fields.forgot.fields) {
            data[k] = fields.forgot.fields[k].val();
        }
        forgotPasswordForm.addClass('in-progress');
        forgotPassword(data).then(function(response) {
            openModal('success-reset-password');
        }, function(error) {
            const errors = error.responseJSON;
            for (let i in errors) {
                let fieldName = i === 'non_field_errors' ? 'email': i;
                fields.forgot.errors[fieldName].server.show();
                fields.forgot.errors[fieldName].server.html(errors[i].join("<br/>"));
            }
        }).finally(() => {
            forgotPasswordForm.removeClass('in-progress');
        });
        return false;
    });

    regForm.on('submit', function(event) {
        event.preventDefault();
        const data = {};
        for (let k in fields.register.fields) {
            data[k] = fields.register.fields[k].val();
        }
        regForm.addClass('in-progress');
        registrationUser(data).then(function(response) {
            openModal('confirm-email');
        }, function(error) {
            const errors = error.responseJSON;
            for (let i in errors) {
                let fieldName = i === 'username' ? 'email': i === 'non_field_errors' ? 'password2': i;
                fields.register.errors[fieldName].server.show();
                fields.register.errors[fieldName].server.html(errors[i].join("<br/>"));
            }
        }).finally(() => {
            regForm.removeClass('in-progress');
        });
        return false;
    });

    loginForm.on('submit', function(event) {
        event.preventDefault();
        const data = {};
        for (let k in fields.signin.fields) {
            data[k === 'email' ? 'username' : k] = fields.signin.fields[k].val();
        }
        loginForm.addClass('in-progress');
        authUser(data).then(function() {
            window.location.reload();
        }, function(error) {
            const errors = error.responseJSON;
            for (let i in errors) {
                let fieldName = i === 'username' ? 'email': 'non_field_errors' ? 'password': i;
                fields.signin.errors[fieldName].server.show();
                fields.signin.errors[fieldName].server.html(errors[i].join("<br/>"));
            }
        }).then(() => {
            loginForm.removeClass('in-progress');
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
                case 'new_password1':
                    if (field.get(0).validity.valueMissing) {
                        formFields.errors[k].required.show();
                    } else if (field.get(0).validity.tooShort) {
                        formFields.errors[k].minlength.show();
                    }
                    break;

                case 'password2':
                case 'new_password2':
                    const pass1Name = k === 'new_password2' ? 'new_password1' : 'password1';
                    if (formFields.fields[k].val() !== formFields.fields[pass1Name].val()) {
                        formFields.fields[k].get(0).setCustomValidity("Invalid");
                        if (formFields.fields[k].val()) {
                            formFields.errors[k].match.show();
                        }
                    } else {
                        formFields.fields[k].get(0).setCustomValidity("");
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


    $('[data-form]').each(function() {
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
        switch (name) {
            case 'auth':
                authFormMenuItems.eq(0).click();
                $('input', authForm).val('').removeClass('touched');
                $('[data-error]', authForm).hide('');
                break;
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

    if (resetPasswordForm) {
        openModal('reset-password');
    }
});

