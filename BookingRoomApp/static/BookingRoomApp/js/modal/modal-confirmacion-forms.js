document.addEventListener('DOMContentLoaded', function() {
    
    function getFormValue(name) {
        const el = document.querySelector(`[name="${name}"]`);
        return el ? el.value : '';
    }

    function setHiddenValue(id, value) {
        const el = document.getElementById(id);
        if (el) el.value = value;
    }

    if (document.getElementById('form-servicio')) {
        window.mostrarConfirmacion = function() {
            const nombre = getFormValue('nameServicio');
            const tipo = getFormValue('tipo_servicio');
            const descripcion = getFormValue('descripcion');
            const costo = getFormValue('costoServicio');

            if (!nombre || !tipo || !descripcion || !costo) {
                alert('Por favor, complete todos los campos');
                return;
            }

            abrirModalConfirmar(
                'Confirmar registro',
                `¿Deseas registrar el servicio "${nombre}"?`,
                function() {
                    setHiddenValue('hidden-nombre', nombre);
                    setHiddenValue('hidden-tipo', tipo);
                    setHiddenValue('hidden-descripcion', descripcion);
                    setHiddenValue('hidden-costo', costo);
                    document.getElementById('form-servicio').submit();
                }
            );
        };
    }

    if (document.getElementById('form-equipamiento')) {
        window.mostrarConfirmacion = function() {
            const nombre = getFormValue('nameEquipamiento');
            const tipo = getFormValue('tipo_equipa');
            const descripcion = getFormValue('descripcion');
            const costo = getFormValue('costoEquipamiento');
            const stock = getFormValue('stockEquipamiento');

            if (!nombre || !tipo || !descripcion || !costo || !stock) {
                alert('Por favor, complete todos los campos');
                return;
            }

            abrirModalConfirmar(
                'Confirmar registro',
                `¿Deseas registrar el equipamiento "${nombre}"?`,
                function() {
                    setHiddenValue('hidden-nombre', nombre);
                    setHiddenValue('hidden-tipo', tipo);
                    setHiddenValue('hidden-descripcion', descripcion);
                    setHiddenValue('hidden-costo', costo);
                    setHiddenValue('hidden-stock', stock);
                    document.getElementById('form-equipamiento').submit();
                }
            );
        };
    }

    if (document.getElementById('form-mobiliario')) {
        window.mostrarConfirmacion = function() {
            const nombre = getFormValue('nameMobiliario');
            const tipo = getFormValue('tipo_mobil');
            const descripcion = getFormValue('descripcion');
            const costo = getFormValue('costoMobiliario');
            const stock = getFormValue('stockTotal');
            const cantidadCaract = getFormValue('cantidad_caracteristicas');

            if (!nombre || !tipo || !descripcion || !costo || !stock) {
                alert('Por favor, complete todos los campos');
                return;
            }

            abrirModalConfirmar(
                'Confirmar registro',
                `¿Deseas registrar el mobiliario "${nombre}"?`,
                function() {
                    setHiddenValue('hidden-nombre', nombre);
                    setHiddenValue('hidden-tipo', tipo);
                    setHiddenValue('hidden-descripcion', descripcion);
                    setHiddenValue('hidden-costo', costo);
                    setHiddenValue('hidden-stock', stock);
                    setHiddenValue('hidden-caracteristicas', cantidadCaract);

                    const caracteristicasDiv = document.querySelectorAll('[name^="caracteristica_"]');
                    const form = document.getElementById('form-mobiliario');
                    caracteristicasDiv.forEach(input => {
                        const inputClone = input.cloneNode();
                        inputClone.name = input.name;
                        form.appendChild(inputClone);
                    });

                    document.getElementById('form-mobiliario').submit();
                }
            );
        };
    }

    if (document.getElementById('form-salon')) {
        window.mostrarConfirmacion = function() {
            const nombre = getFormValue('nameSalon');
            const costo = getFormValue('costoSalon');
            const ubicacion = getFormValue('ubicacionSalon');
            const altura = getFormValue('alturaSalon');
            const anchoVal = getFormValue('anchoSalon');
            const largoVal = getFormValue('largoSalon');
            const mCuadrados = getFormValue('meCuadra');

            if (!nombre || !costo || !ubicacion || !altura || !anchoVal || !largoVal || !mCuadrados) {
                alert('Por favor, complete todos los campos');
                return;
            }

            abrirModalConfirmar(
                'Confirmar registro',
                `¿Deseas registrar el salón "${nombre}"?`,
                function() {
                    setHiddenValue('hidden-nombre', nombre);
                    setHiddenValue('hidden-costo', costo);
                    setHiddenValue('hidden-ubicacion', ubicacion);
                    setHiddenValue('hidden-altura', altura);
                    setHiddenValue('hidden-ancho', anchoVal);
                    setHiddenValue('hidden-largo', largoVal);
                    setHiddenValue('hidden-metros', mCuadrados);
                    document.getElementById('form-salon').submit();
                }
            );
        };
    }

    if (document.getElementById('form-trabajador')) {
        window.mostrarConfirmacion = function() {
            const nombre = getFormValue('nombre');
            const apellidoPaterno = getFormValue('apellido_paterno');
            const apellidoMaterno = getFormValue('apellido_materno');
            const telefono = getFormValue('telefono');
            const rfc = getFormValue('rfc');
            const noEmpleado = getFormValue('no_empleado');
            const rol = getFormValue('rol_id');

            if (!nombre || !apellidoPaterno || !apellidoMaterno || !telefono || !rfc || !noEmpleado || !rol) {
                alert('Por favor, complete todos los campos');
                return;
            }

            abrirModalConfirmar(
                'Confirmar registro',
                `¿Deseas registrar al trabajador "${nombre} ${apellidoPaterno}"?`,
                function() {
                    setHiddenValue('hidden-nombre', nombre);
                    setHiddenValue('hidden-apellido-paterno', apellidoPaterno);
                    setHiddenValue('hidden-apellido-materno', apellidoMaterno);
                    setHiddenValue('hidden-telefono', telefono);
                    setHiddenValue('hidden-rfc', rfc);
                    setHiddenValue('hidden-no-empleado', noEmpleado);
                    setHiddenValue('hidden-rol', rol);
                    document.getElementById('form-trabajador').submit();
                }
            );
        };
    }

});
