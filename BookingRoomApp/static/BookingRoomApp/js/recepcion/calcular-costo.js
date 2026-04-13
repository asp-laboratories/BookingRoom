// Calcula y actualiza dinamicamente el costo de la reservacion
// Se actualiza cada vez que el usuario selecciona algo

document.addEventListener("DOMContentLoaded", function() {
    const IVA_RATE = 0.16; // 16% IVA

    // Elementos del resumen
    const subtotalEl = document.querySelector('.reservacion-fila:nth-child(1) span:last-child');
    const ivaEl = document.querySelector('.reservacion-fila:nth-child(2) span:last-child');
    const totalEl = document.querySelector('.reservacion-fila.reservacion-total span:last-child');

    // Cache de costos para evitar llamadas repetidas al servidor
    const costosCache = {
        salones: {},
        montajes: {}
    };

    // Observar cambios en todos los selects que afectan el precio
    const observables = [
        '#select-salon',
        '#select-montaje',
        '.mobiliario-select',
        '.mobiliario-tipo',
        'input[name*="mobiliario_cantidad"]',
        '.servicio-select',
        '.servicio-tipo',
        '.equipamiento-select',
        '.equipamiento-tipo',
        'input[name*="equipamiento_cantidad"]'
    ];

    // Agregar event listeners a todos los elementos observables
    observables.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
            el.addEventListener('change', calcularCostoReservacion);
            el.addEventListener('input', calcularCostoReservacion);
        });
    });

    // tambien observar cuando se agregan nuevos selects dinamicamente
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length > 0) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        // Agregar listeners a nuevos elementos
                        node.querySelectorAll?.('.mobiliario-select, .mobiliario-tipo, input[name*="mobiliario_cantidad"], .servicio-select, .servicio-tipo, .equipamiento-select, .equipamiento-tipo, input[name*="equipamiento_cantidad"]').forEach(el => {
                            el.addEventListener('change', calcularCostoReservacion);
                            el.addEventListener('input', calcularCostoReservacion);
                        });
                    }
                });
            }
        });
    });

    // Observar contenedores de selects dinamicos
    const contenedores = [
        document.getElementById('mobiliarios-selects'),
        document.getElementById('servicios-selects'),
        document.getElementById('equipamientos-selects')
    ];

    contenedores.forEach(contenedor => {
        if (contenedor) {
            observer.observe(contenedor, { childList: true, subtree: true });
        }
    });

    // Funcion principal para calcular el costo
    async function calcularCostoReservacion() {
        let subtotal = 0;

        mostrarCalculando();

        try {
            // 1. Costo del salon
            const salonSelect = document.getElementById('select-salon');
            if (salonSelect && salonSelect.value) {
                const costoSalon = await obtenerCostoSalon(salonSelect.value);
                subtotal += costoSalon;
            }

            // 2. Costo del montaje
            const montajeSelect = document.getElementById('select-montaje');
            if (montajeSelect && montajeSelect.value) {
                const costoMontaje = await obtenerCostoMontaje(montajeSelect.value);
                subtotal += costoMontaje;
            }

            // 3. Costo de mobiliarios
            document.querySelectorAll('.mobil-pair').forEach(pair => {
                const mobiliarioSelect = pair.querySelector('.mobiliario-select');
                const cantidadInput = pair.querySelector('input[type="number"]');
                
                if (mobiliarioSelect && mobiliarioSelect.value && cantidadInput) {
                    const cantidad = parseInt(cantidadInput.value) || 0;
                    const costoMobiliario = obtenerCostoOpcion(mobiliarioSelect);
                    subtotal += costoMobiliario * cantidad;
                }
            });

            // 4. Costo de servicios
            document.querySelectorAll('.servicio-select').forEach(select => {
                if (select && select.value) {
                    const costoServicio = obtenerCostoOpcion(select);
                    subtotal += costoServicio;
                }
            });

            // 5. Costo de equipamientos
            document.querySelectorAll('.equipamiento-select').forEach(select => {
                const pair = select.closest('.equipo-pair');
                const cantidadInput = pair?.querySelector('input[type="number"]');
                
                if (select && select.value && cantidadInput) {
                    const cantidad = parseInt(cantidadInput.value) || 0;
                    const costoEquipamiento = obtenerCostoOpcion(select);
                    subtotal += costoEquipamiento * cantidad;
                }
            });

            // Calcular IVA y total
            const iva = subtotal * IVA_RATE;
            const total = subtotal + iva;

            // Actualizar UI
            actualizarResumen(subtotal, iva, total);

        } catch (error) {
            console.error('Error al calcular costo:', error);
        } finally {
            ocultarCalculando();
        }
    }

    // Mostrar indicador visual de calculo
    function mostrarCalculando() {
        if (subtotalEl) {
            subtotalEl.textContent = 'Calculando...';
            subtotalEl.style.opacity = '0.5';
        }
    }

    function ocultarCalculando() {
        if (subtotalEl) {
            subtotalEl.style.opacity = '1';
        }
    }

    // Obtener costo desde el texto de la opcion del select
    function obtenerCostoOpcion(select) {
        const option = select.options[select.selectedIndex];
        if (!option) return 0;

        // Intentar obtener el costo desde dataset
        if (option.dataset.costo) {
            return parseFloat(option.dataset.costo) || 0;
        }

        // Extraer costo del texto (formato: "Nombre - $100.00")
        const texto = option.textContent;
        const match = texto.match(/\$([0-9]+\.?[0-9]*)/);
        if (match) {
            return parseFloat(match[1]) || 0;
        }

        return 0;
    }

    // Obtener costo del salon desde el servidor
    async function obtenerCostoSalon(salonId) {
        // Verificar cache primero
        if (costosCache.salones[salonId]) {
            return costosCache.salones[salonId];
        }

        try {
            const response = await fetch(`/api/salon/${salonId}/`);
            if (response.ok) {
                const data = await response.json();
                const precio = parseFloat(data.precio || 0);
                // Guardar en cache
                costosCache.salones[salonId] = precio;
                return precio;
            }
        } catch (error) {
            console.error('Error al obtener costo del salon:', error);
        }
        return 0;
    }

    // Obtener costo del montaje desde el servidor
    async function obtenerCostoMontaje(montajeId) {
        // Verificar cache primero
        if (costosCache.montajes[montajeId]) {
            return costosCache.montajes[montajeId];
        }

        try {
            // El montaje ya incluye el costo en la respuesta de cargarMontajesSalon
            const montageSelect = document.getElementById('select-montaje');
            const option = montageSelect?.options[montageSelect?.selectedIndex];
            if (option && option.dataset.costo) {
                const costo = parseFloat(option.dataset.costo) || 0;
                // Guardar en cache
                costosCache.montajes[montajeId] = costo;
                return costo;
            }
        } catch (error) {
            console.error('Error al obtener costo del montaje:', error);
        }
        return 0;
    }

    // Actualizar el resumen en la UI
    function actualizarResumen(subtotal, iva, total) {
        if (subtotalEl) {
            subtotalEl.textContent = `$${subtotal.toFixed(2)}`;
        }
        if (ivaEl) {
            ivaEl.textContent = `$${iva.toFixed(2)}`;
        }
        if (totalEl) {
            totalEl.textContent = `$${total.toFixed(2)}`;
        }
    }

    // Calcular al cargar la pagina
    calcularCostoReservacion();
});
