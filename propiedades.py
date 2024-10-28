import var


class Propiedades():
    def altaTipoPropiedad(self):
        tipo = var.dlgGestion.txtGestTipoProp.text().title()
        print(tipo)

    def altaPropiedad(self):
        try:
            propiedad = [var.ui.txtFechaProp.text(),var.ui.txtDirProp.text(),var.ui.txtFechaBajaProp.text(),
                         var.ui.cmbProvProp.currentText(),var.ui.cmbMuniProp.currentText(),
                         var.ui.cmbTipoProp.currentText(),var.ui.spinHabProp.text(),
                         var.ui.spinBanosProp.text(),var.ui.txtSuperProp.text(),
                         var.ui.txtPrecioAlquilerProp.text(),var.ui.txtPrecioVentaProp.text(),
                         var.ui.txtCPProp.text(),var.ui.areatxtDescripProp.toPlainText(),
                         var.ui.txtNomeProp.text(),var.ui.txtMovilProp.text()]
            print(propiedad)
        except Exception as error:
            print("Error en alta propiedad: ", error)