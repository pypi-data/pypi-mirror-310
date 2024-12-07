from django import forms
from django.conf import settings


def hide_model_form_fields(form, model, user=None):
    """
    Dynamically hide fields based on user groups.
    Can work with both class-based forms and form instances.

    Args:
        form (forms.ModelForm or Type[forms.ModelForm]): A form instance or class to modify.
        model (models.Model): The model class associated with the form.
        user (User, optional): The current user for whom the form is being customized.
    """
    # Get hidden fields configuration from settings
    hidden_fields_config = getattr(settings, 'PLUGINS_CONFIG', {}).get('netbox_hidebox', {}).get('HIDDEN_FIELDS', {})

    # Determine the full model identifier
    model_identifier = f"{model._meta.app_label}.{model._meta.model_name}"

    # Check if this model has any hidden fields configured
    if model_identifier in hidden_fields_config:
        field_groups = hidden_fields_config[model_identifier]

        # Choose whether we are dealing with a class or an instance
        if isinstance(form, type) and issubclass(form, forms.ModelForm):
            # Form is a class
            base_fields = form.base_fields
        else:
            # Form is an instance
            base_fields = form.fields

        # Iterate over the fields that need to be hidden
        for field_name, excluded_groups in field_groups.items():
            if field_name in base_fields:
                field = base_fields[field_name]

                # Determine if the field should be hidden
                should_hide = True

                # Check user's groups, if user is provided
                if excluded_groups and user:
                    # Hide if user is NOT in any of the excluded groups
                    should_hide = not any(
                        user.groups.filter(name=group).exists()
                        for group in excluded_groups
                    )

                # Apply hiding if necessary
                if should_hide:
                    field.widget = forms.HiddenInput()
                    field.required = False
                    field.label = ''
                    field.help_text = ''

    return form
