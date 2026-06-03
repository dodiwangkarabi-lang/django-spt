from django.contrib import messages


def show_success(request, message):
    messages.success(request, message)

def show_error(request, message):
    messages.error(request, message)


def show_warning(request, message):
    messages.warning(request, message)


def show_info(request, message):
    messages.info(request, message)


def show_form_errors(request, form):

    for field in form:

        for error in field.errors:

            messages.error(
                request,
                f"{field.label}: {error}"
            )

    for error in form.non_field_errors():

        messages.error(request, error)