from django import forms
from .models import Prestamo, Abono, Descuento


class DateInput(forms.DateInput):
    input_type = 'date'

class AbonoForm(forms.ModelForm):

    class Meta:
        model = Abono
        fields = ( 'fecha_abono','valor_abono_capital', 'valor_abono_interes','observaciones')
        widgets = {
            'fecha_abono': DateInput(attrs={'type': 'date'}),
            #'recomienda': forms.TextArea(attrs={'required': 'False' })
            #'cliente': forms.HiddenInput(attrs={'class':'clientehidden','required': 'False' })
        }

class PrestamoForm(forms.ModelForm):

	class Meta:
		model = Prestamo
		fields = ('fecha_prestamo', 'capital_prestado','tipo_prestamo', 'meses_plazo','porcentaje_aplicado','observaciones')
		widgets = {
            'fecha_prestamo': DateInput(attrs={'type': 'date'}),
            #'recomienda': forms.TextArea(attrs={'required': 'False' })
            #'cliente': forms.HiddenInput(attrs={'class':'clientehidden','required': 'False' })
        }
		#'cedula', 'nombres',

class DescuentoForm(forms.ModelForm):

    class Meta:
        model = Descuento
        fields = ('valor_descuento',)